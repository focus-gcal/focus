import { type PlasmoMessaging } from "@plasmohq/messaging"
import { Storage } from "@plasmohq/storage"

import { BackendServer } from "~utils/backend-server"
import { GoogleUtils } from "~utils/google"

const storage = new Storage({ area: "local" })
const handler: PlasmoMessaging.MessageHandler = async (req, res) => {
  const authInProgress = await storage.get("authInProgress")
  if (authInProgress) {
    res.send({ valid: false, isInProgress: true })
    return
  }
  await storage.set("authInProgress", true)
  try {
    const state = crypto.randomUUID()
    const backend_state = await BackendServer.startOAuth(state)
    if (backend_state !== state) {
      throw new Error("State mismatch")
    }

    const AuthURL = GoogleUtils.generateWebAppURL(
      chrome.identity.getRedirectURL(),
      state
    )

    const response = await chrome.identity.launchWebAuthFlow({
      url: AuthURL,
      interactive: true
    })

    const { code, state: returned_state } = GoogleUtils.extractResponse(
      response,
      state
    )
    if (returned_state !== state) {
      throw new Error("State mismatch")
    }
    const { jwt_token, expiry_date } = await BackendServer.callbackOAuth(code, state)
    storage.set("user_auth", {token: jwt_token, expiry_date: expiry_date})


    res.send({ valid: true, isInProgress: false })
  } catch (error) {
    console.error(error)
    res.send({ valid: false, isInProgress: false })
  } finally {
    await storage.set("authInProgress", false)
  }
}

export default handler
