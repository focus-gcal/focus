interface User {
  id: number
  username: string
  email: string
}

enum AuthState {
  LOADING = "loading",
  AUTHENTICATED = "authenticated",
  UNAUTHENTICATED = "unauthenticated"
}

interface UserAuthStorage {
  token: string
  expiry_date: string
}
export type { User, UserAuthStorage }
export { AuthState }
