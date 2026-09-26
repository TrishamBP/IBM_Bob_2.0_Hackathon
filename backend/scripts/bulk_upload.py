"""Bulk-ingest the ACME onboarding library through the running backend.

Files are POSTed one per request to ``/api/v1/rag/upload`` by parallel workers, so they
go through the full semantic pipeline (DeepSeek metadata + segmentation, embeddings)
and all ChromaDB writes stay inside the server process. The department is derived from
each file's YAML front matter (``department:`` / ``owner:``) and the folder.

    uv run python scripts/bulk_upload.py --from 03 --workers 4
    uv run python scripts/bulk_upload.py --from 03 --dry-run
    uv run python scripts/bulk_upload.py --only README.md metadata/glossary.md

Document IDs are derived from department + filename, so two files with the same name in
the same department would overwrite each other. The first (in path order) keeps its
name; later ones are uploaded as ``<folder>-<name>``.
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2] / "docs" / "acme-corp-onboarding"

FRONT_MATTER_DEPARTMENTS = {
    "human-resources": "Human Resources",
    "hr": "Human Resources",
    "information-technology": "IT Operations",
    "it-operations": "IT Operations",
    "information-security": "Information Security",
    "security": "Information Security",
    "engineering": "Software Engineering",
    "cloud-api": "Software Engineering",
    "cloud-frontend": "Software Engineering",
    "workspace": "Software Engineering",
    "intelligence-agents": "AI and Machine Learning",
    "intelligence-ml": "AI and Machine Learning",
    "platform-infrastructure": "Cloud Platform and DevOps",
    "product": "Product Management",
    "cloud-bu": "Product Management",
    "intelligence-bu": "Product Management",
    "workspace-bu": "Product Management",
    "ux-design": "UX and Design",
    "quality-engineering": "Quality Engineering",
    "sales": "Sales",
    "customer-support": "Customer Support",
    "finance": "Finance",
}
# Engineering docs owned by a specific team go to that team's department.
ENGINEERING_OWNERS = {
    "intelligence": "AI and Machine Learning",
    "platform": "Cloud Platform and DevOps",
    "quality": "Quality Engineering",
}
FOLDER_DEFAULTS = {"06-product": "Product Management"}
# Library tooling output, not onboarding content.
EXCLUDED = {"metadata/validation-report.md"}
# Files whose front matter is too generic ("all") or broader than their topic.
OVERRIDES = {
    "11-faq/it-faq.md": "IT Operations",
    "11-faq/security-faq.md": "Information Security",
    "10-training/cloud-platform-fundamentals.md": "Cloud Platform and DevOps",
}


def front_matter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def department_for(path: Path) -> str:
    relative = path.relative_to(ROOT)
    if relative.as_posix() in OVERRIDES:
        return OVERRIDES[relative.as_posix()]
    fields = front_matter(path.read_text(encoding="utf-8"))
    folder = relative.parts[0]
    raw = fields.get("department", "").lower()
    department = FRONT_MATTER_DEPARTMENTS.get(raw)
    if department == "Software Engineering":
        owner = fields.get("owner", "").lower()
        for needle, dept in ENGINEERING_OWNERS.items():
            if needle in owner:
                return dept
    return department or FOLDER_DEFAULTS.get(folder, "Human Resources")


def upload_names() -> dict[Path, str]:
    """Upload filename per library file, unique within each department."""
    names: dict[Path, str] = {}
    taken: set[tuple[str, str]] = set()
    for path in sorted(ROOT.rglob("*.md")):
        department = department_for(path)
        name = path.name
        if (department, name.lower()) in taken:
            name = f"{path.parent.name}-{path.name}"
        taken.add((department, name.lower()))
        names[path] = name
    return names


async def upload(
    client: httpx.AsyncClient, url: str, path: Path, department: str, name: str
) -> tuple[str, str]:
    files = {"files": (name, path.read_bytes(), "text/markdown")}
    response = await client.post(url, data={"department": department}, files=files)
    if response.status_code != 200:
        return "failed", f"HTTP {response.status_code}: {response.text[:200]}"
    body = response.json()
    result = body["results"][0]
    return result["status"], result["message"]


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--from", dest="start", default="03", help="first folder prefix")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--api", default="http://127.0.0.1:8000")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--only", nargs="+", metavar="PATH", help="upload just these library-relative files"
    )
    args = parser.parse_args()

    names = upload_names()
    if args.only:
        paths = [ROOT / p for p in args.only]
        if missing := [p for p in paths if not p.is_file()]:
            print("Not found: " + ", ".join(str(p) for p in missing))
            return 1
        print(f"{len(paths)} selected files")
    else:
        folders = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name >= args.start)
        paths = [
            p
            for f in folders
            for p in sorted(f.rglob("*.md"))
            if p.relative_to(ROOT).as_posix() not in EXCLUDED
        ]
        print(f"{len(paths)} files from {', '.join(f.name for f in folders)}")
    jobs = [(p, department_for(p)) for p in paths]
    if args.dry_run:
        for path, dept in jobs:
            renamed = f"  (as {names[path]})" if names[path] != path.name else ""
            print(f"  {dept:<28} {path.relative_to(ROOT)}{renamed}")
        return 0

    url = f"{args.api}/api/v1/rag/upload"
    queue: asyncio.Queue[tuple[Path, str]] = asyncio.Queue()
    for job in jobs:
        queue.put_nowait(job)
    failures: list[tuple[Path, str]] = []
    done = 0
    started = time.monotonic()

    async def worker(client: httpx.AsyncClient) -> None:
        nonlocal done
        while not queue.empty():
            path, dept = queue.get_nowait()
            try:
                status, message = await upload(client, url, path, dept, names[path])
            except httpx.HTTPError as exc:
                status, message = "failed", f"{type(exc).__name__}: {exc}"
            done += 1
            if status == "failed":
                failures.append((path, message))
            elapsed = time.monotonic() - started
            print(
                f"[{done}/{len(jobs)} {elapsed:5.0f}s] {status:<9} {dept:<26} "
                f"{path.relative_to(ROOT)} — {message}",
                flush=True,
            )

    async with httpx.AsyncClient(timeout=httpx.Timeout(900.0, connect=10.0)) as client:
        await asyncio.gather(*(worker(client) for _ in range(args.workers)))

    print(
        f"\nDone in {time.monotonic() - started:.0f}s: {len(jobs) - len(failures)} ok, "
        f"{len(failures)} failed"
    )
    for path, message in failures:
        print(f"  FAILED {path.relative_to(ROOT)}: {message}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
