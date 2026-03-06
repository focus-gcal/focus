import { useQuery } from "@tanstack/react-query"
import { sendToBackground } from "@plasmohq/messaging"

export const SCHEDULES_LIST_QUERY_KEY = ["schedules", "list"] as const

export function useSchedulesList() {
  return useQuery({
    queryKey: SCHEDULES_LIST_QUERY_KEY,
    queryFn: async () => {
      const res = await sendToBackground({
        name: "schedules",
        body: { action: "list" },
      })
      if (!res.ok) throw new Error(res.error)
      return res.data
    },
  })
}