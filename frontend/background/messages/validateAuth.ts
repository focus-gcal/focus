import type { PlasmoMessaging } from "@plasmohq/messaging"
import { Storage } from "@plasmohq/storage"

import type { UserAuthStorage } from "~types/user"

const storage = new Storage({ area: "local" })
const handler: PlasmoMessaging.MessageHandler = async (req, res) => {
  const user_auth: UserAuthStorage | null = await storage.get("user_auth")
  if (user_auth) {
    if (user_auth.expiry_date && new Date(user_auth.expiry_date) > new Date()) {
      res.send({ valid: true })
    } else {
      await storage.remove("user_auth")
      res.send({ valid: false })
    }
  } else {
    res.send({ valid: false })
  }
}

export default handler
