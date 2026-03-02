import { DeleteOutlined, EditOutlined } from "@ant-design/icons"
import { Button, Popconfirm } from "antd"
import type { ScheduleListOut } from "./types/schedule"
import { formatDays, formatTime } from "~/utils"

interface DetailViewProps {
  detail: ScheduleListOut
  onBack: () => void
  onUpdate: () => void
  onDelete: () => void
}

export function DetailView({ detail, onBack, onUpdate, onDelete }: DetailViewProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column" }}>
        <Button
          type="text"
          onClick={onBack}
          style={{
            marginBottom: 16,
            marginTop: 0,
            color: "#40a9ff",
            padding: 0,
            alignSelf: "flex-start",
          }}>
          ← Back
        </Button>
        <div
          style={{
            background: "#262626",
            borderRadius: 16,
            padding: 24,
          }}>
          <div
            style={{
              display: "flex",
              alignItems: "flex-start",
              justifyContent: "space-between",
              gap: 12,
              marginBottom: 8,
            }}>
            <h2 style={{ margin: 0, fontSize: 18, fontWeight: 600 }}>
              {detail.name}
            </h2>
            <div style={{ display: "flex", gap: 8 }}>
              <Button
                type="text"
                aria-label="Edit schedule"
                icon={<EditOutlined />}
                onClick={onUpdate}
                style={{ color: "rgba(255,255,255,0.85)" }}
              />
              <Popconfirm
                title="Delete schedule?"
                description="This cannot be undone."
                okText="Delete"
                cancelText="Cancel"
                okButtonProps={{ danger: true }}
                onConfirm={onDelete}>
                <Button
                  type="text"
                  danger
                  aria-label="Delete schedule"
                  icon={<DeleteOutlined />}
                />
              </Popconfirm>
            </div>
          </div>
          <p
            style={{
              margin: 0,
              marginBottom: 16,
              fontSize: 13,
              opacity: 0.85,
            }}>
            {formatDays(detail.days_of_week)} {formatTime(detail.start_time)} –{" "}
            {formatTime(detail.end_time)}
          </p>
          <h3 style={{ fontSize: 14, marginBottom: 8 }}>Tasks</h3>
          {detail.tasks.length === 0 ? (
            <p style={{ margin: 0, fontSize: 13, opacity: 0.7 }}>No tasks</p>
          ) : (
            <ul style={{ margin: 0, paddingLeft: 20 }}>
              {detail.tasks.map((t) => (
                <li key={t.id} style={{ marginBottom: 4 }}>
                  {t.title}
                </li>
              ))}
            </ul>
          )}
        </div>
    </div>
  )
}
