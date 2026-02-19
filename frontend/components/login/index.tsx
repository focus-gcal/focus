import { Button, ConfigProvider } from "antd"
import logoUrl from "raw:~assets/logo.png"

function Login() {
  return (
    <ConfigProvider
      theme={{
        token: {
          borderRadius: 8
          // optional: customize colors
        }
      }}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          minHeight: "100%",
          position: "relative",
          top: 25
        }}>
        <img src={logoUrl} alt="Logo" style={{ width: 200, height: "auto" }} />
        <Button type="primary" size="large" onClick={() => {}}>
          Sign in
        </Button>
      </div>
    </ConfigProvider>
  )
}

export default Login
