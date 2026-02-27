import { useState } from "react"
import { useAuth } from "context/auth"
import { Storage } from "@plasmohq/storage"
import { Layout, Menu, ConfigProvider, Dropdown } from "antd"
import logUrl from "raw:~assets/logo.png"

type DashboardView = "tasks" | "schedules" | "settings"

const headerMenuItems = [
  { key: "tasks", label: "Tasks" },
  { key: "schedules", label: "Schedules" },
]

const settingsDropdownItems = [{ key: "settings", label: "Settings" }]

const storage = new Storage({ area: "local" })

function Dashboard() {
  const { refreshAuth } = useAuth()
  const [view, setView] = useState<DashboardView>("tasks")

  return (
    <ConfigProvider
      theme={{
        token: {
          borderRadius: 8,
          colorBgContainer: "#212121",
          colorText: "#ffffff",
        },
        components: {
          Menu: {
            colorBgContainer: "#212121",
            itemColor: "#ffffff",
            horizontalItemSelectedColor: "#40a9ff",
            horizontalItemHoverColor: "#40a9ff",
          },
          Dropdown: {
            colorBgElevated: "#212121",
            colorText: "#ffffff",
            controlItemBgHover: "#383838",
            controlItemBgActive: "#404040",
          },
        },
      }}>
      <Layout
        style={{
          minHeight: "100%",
          flexDirection: "column",
          background: "#212121",
          color: "#ffffff",
        }}>
        <Layout.Header
          style={{
            height: 64,
            padding: "0 16px",
            display: "flex",
            alignItems: "center",
            gap: 16,
            background: "#212121",
            borderBottom: "1px solid #333333",
          }}>
          <img
            src={logUrl}
            alt="Focus"
            style={{ height: 68, width: "auto" }}
          />
          <Menu
            mode="horizontal"
            selectedKeys={view === "settings" ? [] : [view]}
            items={headerMenuItems}
            onClick={({ key }) => setView(key as DashboardView)}
            style={{
              background: "transparent",
              borderBottom: "none",
              flex: 1,
            }}
          />
          <Dropdown
            menu={{
              items: settingsDropdownItems,
              onClick: ({ key }) => setView(key as DashboardView),
              style: { background: "#212121", minWidth: 120 },
            }}
            trigger={["click"]}
            placement="bottomRight"
            overlayStyle={{ background: "#212121", borderRadius: 8 }}
            overlayClassName="dashboard-settings-dropdown">
            <button
              type="button"
              aria-label="Settings"
              style={{
                background: "transparent",
                border: "none",
                color: "#ffffff",
                cursor: "pointer",
                padding: "4px 8px",
                fontSize: 18,
                lineHeight: 1,
                borderRadius: 4,
              }}>
              ⋮
            </button>
          </Dropdown>
        </Layout.Header>

        <Layout.Content
          style={{
            padding: 16,
            flex: 1,
            overflow: "auto",
            background: "#212121",
          }}>
          {view === "tasks" && (
            <div>Tasks view — your tasks list will go here.</div>
          )}

          {view === "schedules" && (
            <div>Schedules view — your schedules will go here.</div>
          )}

          {view === "settings" && (
            <div>
              <div>Settings</div>
              <button
                style={{ marginTop: 16 }}
                onClick={() => {
                  storage.remove("user_auth")
                  refreshAuth()
                }}>
                Sign Out
              </button>
            </div>
          )}
        </Layout.Content>
      </Layout>
    </ConfigProvider>
  )
}

export default Dashboard