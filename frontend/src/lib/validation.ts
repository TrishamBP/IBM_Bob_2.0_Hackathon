export const HR_DOMAIN = '@hr.com';
export const EMPLOYEE_DOMAIN = '@acmecorp.com';

export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim());
}

export function validateHREmail(email: string): { valid: boolean; error?: string } {
  const trimmed = email.trim();
  if (!trimmed) {
    return { valid: false, error: 'Email address is required.' };
  }
  if (!validateEmail(trimmed)) {
    return { valid: false, error: 'Please enter a valid email address.' };
  }
  if (!trimmed.toLowerCase().endsWith(HR_DOMAIN)) {
    return {
      valid: false,
      error: `HR accounts must use a ${HR_DOMAIN} email address.`,
    };
  }
  return { valid: true };
}

export function validateEmployeeEmail(email: string): { valid: boolean; error?: string } {
  const trimmed = email.trim();
  if (!trimmed) {
    return { valid: false, error: 'Email address is required.' };
  }
  if (!validateEmail(trimmed)) {
    return { valid: false, error: 'Please enter a valid email address.' };
  }
  if (!trimmed.toLowerCase().endsWith(EMPLOYEE_DOMAIN)) {
    return {
      valid: false,
      error: `Employee accounts must use a ${EMPLOYEE_DOMAIN} email address.`,
    };
  }
  return { valid: true };
}
