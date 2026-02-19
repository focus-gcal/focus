import { ConfigProvider, Spin } from "antd"

export default function Loading() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#1677ff"
        }
      }}>
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%) scale(2)"
        }}>
        <Spin size="large" />
      </div>
    </ConfigProvider>
  )
}
