import { useAuth } from "context/auth"

import { Storage } from "@plasmohq/storage"

const storage = new Storage({ area: "local" })

function Dashboard() {
  const { refreshAuth } = useAuth()
  return (
    <div>
      {" "}
      ddd
      <button
        onClick={() => {
          storage.remove("user_auth")
          refreshAuth()
        }}>
        Sign Out
      </button>
    </div>
  )
}

export default Dashboard
