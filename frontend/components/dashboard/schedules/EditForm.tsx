import { useMemo, useState } from "react"
import { Button } from "antd"
import type { ScheduleOut, ScheduleTimeBlock } from "./types/schedule"
import { DAY_LABELS } from "~/utils"

interface ScheduleEditFormProps {
  schedule: ScheduleOut
  dayLabels: string[]
  onSave: (updated: ScheduleOut) => void
  onCancel: () => void
}

export function ScheduleEditForm({
  schedule,
  dayLabels,
  onSave,
  onCancel,
}: ScheduleEditFormProps) {
  const [name, setName] = useState(schedule.name)
  const [timeBlocks, setTimeBlocks] = useState<ScheduleTimeBlock[]>(() => {
    if (schedule.time_blocks && schedule.time_blocks.length > 0) {
      return schedule.time_blocks.map((b) => ({
        ...b,
        start_time: b.start_time.slice(0, 5),
        end_time: b.end_time.slice(0, 5),
      }))
    }
    // Fallback: create one block per selected day using legacy start/end
    return (schedule.days_of_week ?? []).map((day) => ({
      day_of_week: day,
      start_time: schedule.start_time.slice(0, 5),
      end_time: schedule.end_time.slice(0, 5),
    }))
  })

  const isValidBlock = (block: ScheduleTimeBlock) =>
    block.start_time < block.end_time &&
    block.day_of_week >= 0 &&
    block.day_of_week <= 6

  const normalizedBlocks = useMemo(
    () => timeBlocks.filter(isValidBlock),
    [timeBlocks]
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (normalizedBlocks.length === 0) return

    const daysOfWeek = Array.from(
      new Set(normalizedBlocks.map((b) => b.day_of_week))
    ).sort()

    const earliestStart = normalizedBlocks
      .map((b) => b.start_time)
      .sort()[0]
    const latestEnd = normalizedBlocks
      .map((b) => b.end_time)
      .sort()
      .slice(-1)[0]

    onSave({
      ...schedule,
      name: name.trim(),
      days_of_week: daysOfWeek,
      start_time: earliestStart,
      end_time: latestEnd,
      time_blocks: normalizedBlocks,
    })
  }

  return (
    <div
      style={{
        maxWidth: 400,
        width: "100%",
        paddingTop: 0,
      }}>
      <Button
        type="text"
        onClick={onCancel}
        style={{ marginBottom: 16, color: "#40a9ff", padding: 0 }}>
        ← Back
      </Button>
      <form
        onSubmit={handleSubmit}
        style={{
          background: "#262626",
          borderRadius: 16,
          padding: 24,
        }}>
        <label style={{ display: "block", marginBottom: 8, fontSize: 13 }}>Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{
            width: "100%",
            marginBottom: 16,
            padding: 8,
            borderRadius: 8,
            border: "1px solid #404040",
            background: "#212121",
            color: "#fff",
          }}
        />
        <label style={{ display: "block", marginBottom: 8, fontSize: 13 }}>
          Time blocks
        </label>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 8,
            marginBottom: 16,
            padding: 8,
            borderRadius: 8,
            border: "1px solid #404040",
            background: "#212121",
            color: "#fff",
          }}>
          {timeBlocks.length === 0 && (
            <p style={{ margin: 0, fontSize: 13, opacity: 0.7 }}>
              No time blocks yet. Add at least one day and time range.
            </p>
          )}
          {timeBlocks.map((block, index) => (
            <div
              key={index}
              style={{
                display: "grid",
                gridTemplateColumns: "minmax(0, 1.2fr) repeat(2, minmax(0, 1fr)) auto",
                gap: 8,
                alignItems: "center",
              }}>
              <select
                value={block.day_of_week}
                onChange={(e) => {
                  const day = Number(e.target.value)
                  setTimeBlocks((prev) =>
                    prev.map((b, i) =>
                      i === index
                        ? {
                            ...b,
                            day_of_week: day,
                          }
                        : b
                    )
                  )
                }}
                style={{
                  padding: 8,
                  borderRadius: 8,
                  border: "1px solid #404040",
                  background: "#212121",
                  color: "#fff",
                }}>
                {DAY_LABELS.map((label, i) => (
                  <option key={i} value={i}>
                    {label}
                  </option>
                ))}
              </select>
              <input
                type="time"
                value={block.start_time}
                onChange={(e) => {
                  const value = e.target.value
                  setTimeBlocks((prev) =>
                    prev.map((b, i) =>
                      i === index
                        ? {
                            ...b,
                            start_time: value,
                          }
                        : b
                    )
                  )
                }}
                style={{
                  padding: 8,
                  borderRadius: 8,
                  border: "1px solid #404040",
                  background: "#212121",
                  color: "#fff",
                }}
              />
              <input
                type="time"
                value={block.end_time}
                onChange={(e) => {
                  const value = e.target.value
                  setTimeBlocks((prev) =>
                    prev.map((b, i) =>
                      i === index
                        ? {
                            ...b,
                            end_time: value,
                          }
                        : b
                    )
                  )
                }}
                style={{
                  padding: 8,
                  borderRadius: 8,
                  border: "1px solid #404040",
                  background: "#212121",
                  color: "#fff",
                }}
              />
              <button
                type="button"
                onClick={() =>
                  setTimeBlocks((prev) => prev.filter((_, i) => i !== index))
                }
                style={{
                  borderRadius: 999,
                  border: "1px solid #404040",
                  background: "#1f1f1f",
                  color: "rgba(255,255,255,0.85)",
                  padding: "6px 10px",
                  cursor: "pointer",
                }}>
                ✕
              </button>
            </div>
          ))}
          <Button
            type="dashed"
            onClick={() =>
              setTimeBlocks((prev) => [
                ...prev,
                {
                  day_of_week: 0,
                  start_time: "09:00",
                  end_time: "17:00",
                },
              ])
            }
            style={{ marginTop: 4 }}>
            + Add time block
          </Button>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <Button type="primary" htmlType="submit" shape="round">
            Save
          </Button>
          <Button type="default" onClick={onCancel} shape="round">
            Cancel
          </Button>
        </div>
      </form>
    </div>
  )
}

