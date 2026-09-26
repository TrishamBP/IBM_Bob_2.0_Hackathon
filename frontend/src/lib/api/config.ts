/**
 * Backend base URL shared by all API clients (no trailing slash).
 *
 * Set NEXT_PUBLIC_API_BASE_URL to override. Without it, production builds use the
 * deployed Render backend and local development uses http://localhost:8000.
 */

const PRODUCTION_API_BASE = 'https://ibm-bob-2-0-hackathon.onrender.com';
const DEVELOPMENT_API_BASE = 'http://localhost:8000';

export const API_BASE = (
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  (process.env.NODE_ENV === 'production' ? PRODUCTION_API_BASE : DEVELOPMENT_API_BASE)
).replace(/\/$/, '');
