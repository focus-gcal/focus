import { useEffect, useState } from "react"

import { sendToBackground } from "@plasmohq/messaging"
import { type User, AuthState } from "~types/user"
import { Dashboard, Login } from "~components"


function IndexPopup() {
  const [authState, setAuthState] = useState<AuthState>(AuthState.LOADING)

  useEffect(() => {
    sendToBackground({ name: "validateAuth" })
      .then((res) => {
        console.log(res)
        setAuthState(res.valid ? AuthState.AUTHENTICATED : AuthState.UNAUTHENTICATED)
      })
      .catch((err) => {
        console.log(err)
        setAuthState(AuthState.LOADING)
      })
  }, [])

  return (
    <div
      style={{
        padding: 16,
        minWidth: 320,
        minHeight: 500,
        width: 320,
        height: 500
      }}>
        {authState === AuthState.LOADING && <div>Loading...</div>}
        {authState === AuthState.AUTHENTICATED && <Dashboard />}
        {authState === AuthState.UNAUTHENTICATED && <Login />}
      </div>
  )
}

export default IndexPopup
