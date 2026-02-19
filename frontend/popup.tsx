import { useEffect, useState } from "react"

import { sendToBackground } from "@plasmohq/messaging"

import { Dashboard, Loading, Login } from "~components"
import { AuthState, type User } from "~types/user"

import "./popup.css"

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
        padding: 20,
        minWidth: 320,
        minHeight: 500,
        width: 320,
        height: 500,
        overflow: "hidden"
      }}>
      {authState === AuthState.LOADING && <Loading />}
      {authState === AuthState.AUTHENTICATED && <Dashboard />}
      {authState === AuthState.UNAUTHENTICATED && <Login />}
    </div>
  )
}

export default IndexPopup
