export const DEV_TOKEN_KEY = 'careerpilot_dev_token'
export const DEV_AUTH_TOKEN = import.meta.env.VITE_DEV_AUTH_TOKEN || 'careerpilot-dev-local-token'

export function getDevToken(): string | null {
  return localStorage.getItem(DEV_TOKEN_KEY)
}

export function setDevToken(token: string) {
  localStorage.setItem(DEV_TOKEN_KEY, token)
}

export function clearDevToken() {
  localStorage.removeItem(DEV_TOKEN_KEY)
}

export function isDevMode(): boolean {
  return import.meta.env.VITE_DEV_MODE === 'true'
}
