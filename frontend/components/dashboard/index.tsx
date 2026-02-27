import { useState } from "react"
import { useAuth } from "context/auth"
import { Storage } from "@plasmohq/storage"
import { Button, ConfigProvider, Dropdown, Layout, Menu } from "antd"
import logUrl from "raw:~assets/logo.png"

type DashboardView = "tasks" | "schedules" | "settings"

const headerMenuItems = [
  { key: "tasks", label: "Tasks" },
  { key: "schedules", label: "Schedules" },
]

const settingsDropdownItems = [
  { key: "settings", label: "Settings" },
  { type: "divider" as const },
  { key: "sign-out", label: "Sign Out" },
]
const storage = new Storage({ area: "local" })

function Dashboard() {
  const { refreshAuth } = useAuth()
  const [view, setView] = useState<DashboardView>("tasks")

  const renderEmptyState = (options: {
    title: string
    description: string
    primaryLabel: string
  }) => (
    <div
      style={{
        background: "#262626",
        borderRadius: 16,
        padding: 24,
        maxWidth: 320,
        width: "100%",
        textAlign: "center",
        boxShadow: "0 16px 40px rgba(0,0,0,0.55)",
      }}>
      <h2
        style={{
          margin: 0,
          marginBottom: 8,
          fontSize: 18,
          fontWeight: 600,
        }}>
        {options.title}
      </h2>
      <p
        style={{
          margin: 0,
          marginBottom: 16,
          fontSize: 13,
          opacity: 0.85,
        }}>
        {options.description}
      </p>
      <Button
        type="primary"
        shape="round"
        style={{
          paddingInline: 24,
        }}>
        {options.primaryLabel}
      </Button>
    </div>
  )

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
            height: 60,
            padding: "0 20px",
            display: "flex",
            alignItems: "center",
            gap: 8,
            background: "#212121",
            borderBottom: "1px solid #333333",
          }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              marginRight: 12,
            }}>
            <img
              src={logUrl}
              alt="Focus"
              style={{ height: 58, width: "auto", marginTop: 2 }}
            />
            <span
              style={{
                fontSize: 16,
                fontWeight: 600,
                color: "rgba(255,255,255,0.92)",
              }}>
              Focus
            </span>
          </div>
          <Menu
            mode="horizontal"
            selectedKeys={view === "settings" ? [] : [view]}
            items={headerMenuItems}
            onClick={({ key }) => setView(key as DashboardView)}
            style={{
              background: "transparent",
              borderBottom: "none",
            }}
          />
          <Dropdown

          menu={{
            items: settingsDropdownItems,
            onClick: ({ key }) => {
              if (key === "sign-out") {
                storage.remove("user_auth")
                refreshAuth()
              } else {
                setView(key as DashboardView)
              }
            },
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
            padding: "80px 32px 40px",
            flex: 1,
            background: "#212121",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "flex-start",
            position: "relative",
          }}>
          {view === "tasks" &&
            renderEmptyState({
              title: "No tasks yet",
              description:
                "Create your first task to start focusing on what matters.",
              primaryLabel: "Create Task",
            })}

          {view === "schedules" &&
            renderEmptyState({
              title: "No schedules yet",
              description:
                "Create your first schedule to control when tasks can be auto-planned.",
              primaryLabel: "Create Schedule",
            })}

          {(view === "tasks" || view === "schedules") && (
            <button
              type="button"
              aria-label="Add"
              style={{
                position: "absolute",
                right: 24,
                bottom: 24,
                width: 44,
                height: 44,
                borderRadius: "50%",
                border: "none",
                background: "#1677ff",
                color: "#ffffff",
                fontSize: 24,
                lineHeight: 1,
                cursor: "pointer",
                boxShadow: "0 12px 32px rgba(0,0,0,0.6)",
              }}>
              +
            </button>
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