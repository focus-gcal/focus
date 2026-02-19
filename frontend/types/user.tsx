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
export type { User }
export { AuthState }
