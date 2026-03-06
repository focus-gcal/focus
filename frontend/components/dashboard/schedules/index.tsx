import { useState } from "react"
import { toast } from "react-hot-toast"
import type { ScheduleOut, ScheduleListOut } from "./types/schedule"
import { DAY_LABELS } from "~/utils"
import { ScheduleEditForm } from "./EditForm"
import { EmptyState } from "../common/EmptyState"
import { DetailView } from "./DetailView"
import { ScheduleListItem } from "./ScheduleListItem"
import { CreateButton } from "../common/CreateButton"
import { useSchedulesList } from "~/hooks/useSchedulesList"
import { useScheduleDetail } from "~/hooks/useScheduleDetail"
import {
  useCreateSchedule,
  useUpdateSchedule,
  useDeleteSchedule,
} from "~/hooks/useScheduleMutations"

const NEW_SCHEDULE_ID = 0

export default function SchedulesView() {
  const notifySuccess = (message: string) => toast.success(message)
  const notifyError = (message: string) => toast.error(message)

  const { data, isLoading, error } = useSchedulesList()
  const schedules: ScheduleOut[] = (data ?? []).map(
    (s: ScheduleOut & { blocks?: typeof s.time_blocks }) => {
      if (s.blocks && !s.time_blocks) {
        const { blocks, ...rest } = s
        return { ...rest, time_blocks: blocks }
      }
      return s as ScheduleOut
    }
  )

  const [selectedScheduleId, setSelectedScheduleId] = useState<number | null>(null)
  const [editingSchedule, setEditingSchedule] = useState<ScheduleOut | null>(null)
  const [isCreating, setIsCreating] = useState(false)

  const detailQuery = useScheduleDetail(selectedScheduleId)
  const detail: ScheduleListOut | null = detailQuery.data ?? null

  const createSchedule = useCreateSchedule()
  const updateSchedule = useUpdateSchedule()
  const deleteSchedule = useDeleteSchedule()

  const deleteScheduleById = async (scheduleId: number) => {
    try {
      await deleteSchedule.mutateAsync(scheduleId)
      if (selectedScheduleId === scheduleId) setSelectedScheduleId(null)
      if (editingSchedule?.id === scheduleId) {
        setEditingSchedule(null)
        setIsCreating(false)
      }
      notifySuccess("Schedule deleted")
    } catch (e) {
      notifyError(e instanceof Error ? e.message : "Failed to delete schedule")
    }
  }

  const handleDelete = (schedule: ScheduleOut, e: React.MouseEvent) => {
    e.stopPropagation()
    deleteScheduleById(schedule.id)
  }

  const handleEdit = (schedule: ScheduleOut, e: React.MouseEvent) => {
    e.stopPropagation()
    setIsCreating(false)
    setEditingSchedule(schedule)
  }

  const handleCreate = () => {
    const userId = schedules[0]?.user_id ?? 1
    const draft: ScheduleOut = {
      id: NEW_SCHEDULE_ID,
      user_id: userId,
      name: "",
      day_of_week: 0,
      start_time: "09:00",
      end_time: "17:00",
      time_blocks: [
        { day_of_week: 0, start_time: "09:00", end_time: "17:00" },
      ],
    }
    setIsCreating(true)
    setEditingSchedule(draft)
  }

  const handleSave = async (updated: ScheduleOut) => {
    const blocks = updated.time_blocks ?? []
    if (!blocks.length) {
      notifyError("At least one time block is required")
      return
    }
    try {
      if (updated.id === NEW_SCHEDULE_ID) {
        await createSchedule.mutateAsync({
          name: updated.name.trim(),
          blocks,
        })
        notifySuccess("Schedule created")
      } else {
        await updateSchedule.mutateAsync({
          schedule_id: updated.id,
          name: updated.name.trim(),
          blocks,
        })
        notifySuccess("Schedule updated")
      }
      setEditingSchedule(null)
      setIsCreating(false)
    } catch (e) {
      notifyError(e instanceof Error ? e.message : "Failed to save schedule")
    }
  }

  let content
  
  if (isLoading) {
    content = <div style={{ padding: 16, textAlign: "center" }}>Loading schedules…</div>
  } else if (error) {
    content = (
      <div style={{ padding: 16, color: "red" }}>
        Failed to load schedules: {error instanceof Error ? error.message : "Unknown error"}
      </div>
    )
  } 
  else if (schedules.length === 0 && !isCreating) {
    content = (
      <EmptyState
        onCreate={handleCreate}
        titleText="No schedules yet"
        descriptionText="Create your first schedule to control when tasks can be auto-planned."
        buttonText="Create Schedule"
      />
    )
  } else if (editingSchedule) {
    content = (
      <ScheduleEditForm
        schedule={editingSchedule}
        dayLabels={DAY_LABELS}
        onSave={handleSave}
        onCancel={() => {
          setEditingSchedule(null)
          setIsCreating(false)
        }}
      />
    )
  } else if (selectedScheduleId != null) {
    if (detailQuery.isLoading) {
      content = (
        <div style={{ padding: 16, textAlign: "center" }}>
          Loading schedule…
        </div>
      )
    } else if (detailQuery.error) {
      content = (
        <div style={{ padding: 16 }}>
          <div style={{ color: "red", marginBottom: 8 }}>
            {detailQuery.error instanceof Error
              ? detailQuery.error.message
              : "Failed to load schedule"}
          </div>
          <button
            type="button"
            onClick={() => setSelectedScheduleId(null)}
            style={{ cursor: "pointer" }}>
            Back to list
          </button>
        </div>
      )
    } else if (detail) {
      content = (
        <DetailView
          detail={detail}
          onBack={() => setSelectedScheduleId(null)}
          onUpdate={() => {
            setIsCreating(false)
            setEditingSchedule(detail)
          }}
          onDelete={() => deleteScheduleById(detail.id)}
        />
      )
    } else {
      content = (
        <div style={{ padding: 16 }}>
          <button
            type="button"
            onClick={() => setSelectedScheduleId(null)}
            style={{ cursor: "pointer" }}>
            Back to list
          </button>
        </div>
      )
    }
  } else {
    content = (
      <>
        {schedules.map((schedule) => (
          <ScheduleListItem
            key={schedule.id}
            schedule={schedule}
            onSelect={() => setSelectedScheduleId(schedule.id)}
            onEdit={(e) => handleEdit(schedule, e)}
            onDelete={(e) => handleDelete(schedule, e)}
          />
        ))}
        <CreateButton onClick={handleCreate} ariaLabel="Add Schedule" />
      </>
    )
  }

  return (
    <>
      {content}
    </>
  )
}
