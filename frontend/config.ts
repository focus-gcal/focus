interface Config {
  backend: {
    baseUrl: string
  }
  oauth: {
    clientId: string
    redirectURI: string
  }
}

const config: Config = {
  oauth: {
    clientId: process.env.PLASMO_PUBLIC_OAUTH_CLIENT_ID,
    redirectURI: process.env.PLASMO_PUBLIC_OAUTH_REDIRECT_URI
  },
  backend: {
    baseUrl: process.env.PLASMO_PUBLIC_BACKEND_URL
  }
}

if (!config.oauth.clientId) {
  throw new Error("Missing OAuth client ID")
}

export default config
