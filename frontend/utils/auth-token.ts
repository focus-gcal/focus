import { Storage } from "@plasmohq/storage"

import type { UserAuthStorage } from "~types/user"

const storage = new Storage({ area: "local" })
const AUTH_KEY = "user_auth"

/**
 * Get the JWT from extension storage. Returns null if not signed in or missing.
 */
export async function getAuthToken(): Promise<string | null> {
  const userAuth: UserAuthStorage | null = await storage.get(AUTH_KEY)
  return userAuth?.token ?? null
}