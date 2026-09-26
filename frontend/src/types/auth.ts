export type UserRole = 'hr' | 'employee';

export interface MockSession {
  email: string;
  role: UserRole;
}
