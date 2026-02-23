import config from "~config"

interface StartOAuthResponse {
  ok: boolean
  state: string
  error?: string
}

interface CallbackOAuthResponse {
  ok: boolean
  jwt_token?: string
  expiry_date?: string
  error?: string
}

class BackendServer {
  static baseUrl: string = config.backend.baseUrl

  static async startOAuth(state: string) {
    const response = await fetch(`${this.baseUrl}/auth/google/start`, {
      method: "POST",
      body: JSON.stringify({ state: state }),
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    })
    const data: StartOAuthResponse = await response.json().catch((error) => {
      throw new Error("Failed to parse response")
    })
    if (!response.ok || !data.ok) {
      throw new Error(data.error || "Failed to start OAuth")
    }
    return data.state
  }

  static async callbackOAuth(code: string, state: string) {
    const response = await fetch(`${this.baseUrl}/auth/google/callback`, {
      method: "POST",
      body: JSON.stringify({ code: code, state: state }),
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    })
    const data: CallbackOAuthResponse = await response.json().catch((error) => {
      throw new Error("Failed to parse response")
    })
    if (!response.ok || !data.ok) {
      throw new Error(data.error || "Failed to callback OAuth")
    }
    return {jwt_token: data.jwt_token, expiry_date: data.expiry_date}
  }
}

export { BackendServer }
