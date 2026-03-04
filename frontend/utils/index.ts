export const DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

export function formatTime(s: string): string {
  const [h, m] = s.split(":").map(Number)
  if (h === 0) return `12:${m.toString().padStart(2, "0")} AM`
  if (h < 12) return `${h}:${m.toString().padStart(2, "0")} AM`
  if (h === 12) return `12:${m.toString().padStart(2, "0")} PM`
  return `${h - 12}:${m.toString().padStart(2, "0")} PM`
}

export function formatDays(days: number[]): string {
  if (!days || days.length === 0) return ""
  return days
    .map((d) => DAY_LABELS[d] ?? "")
    .filter(Boolean)
    .join(", ")
}

export interface SimpleTimeBlock {
  day_of_week: number
  start_time: string
  end_time: string
}

export function formatTimeBlocks(blocks: SimpleTimeBlock[]): string {
  if (!blocks || blocks.length === 0) return ""

  const byDay = new Map<number, { start_time: string; end_time: string }[]>()
  for (const block of blocks) {
    if (block.start_time >= block.end_time) continue
    if (!byDay.has(block.day_of_week)) {
      byDay.set(block.day_of_week, [])
    }
    byDay.get(block.day_of_week)!.push({
      start_time: block.start_time,
      end_time: block.end_time,
    })
  }

  const dayEntries = Array.from(byDay.entries()).sort(([a], [b]) => a - b)
  return dayEntries
    .map(([day, ranges]) => {
      const label = DAY_LABELS[day] ?? ""
      const formattedRanges = ranges
        .sort((a, b) => a.start_time.localeCompare(b.start_time))
        .map((r) => `${formatTime(r.start_time)} – ${formatTime(r.end_time)}`)
        .join(", ")
      return `${label} ${formattedRanges}`
    })
    .join("; ")
}

/** Parse "HH:MM" to minutes since midnight */
export function minutesFromTime(s: string): number {
  const [h, m] = s.split(":").map(Number)
  return (h ?? 0) * 60 + (m ?? 0)
}

const MINUTES_PER_DAY = 24 * 60

/** Get total hours for a schedule from time blocks or legacy day range */
export function getScheduleTotalHours(schedule: {
  time_blocks?: SimpleTimeBlock[]
  days_of_week?: number[]
  start_time?: string
  end_time?: string
}): number {
  let totalMinutes = 0
  if (schedule.time_blocks && schedule.time_blocks.length > 0) {
    for (const b of schedule.time_blocks) {
      const start = minutesFromTime(b.start_time)
      const end = minutesFromTime(b.end_time)
      if (end > start) totalMinutes += end - start
    }
  } else if (
    schedule.days_of_week?.length &&
    schedule.start_time != null &&
    schedule.end_time != null
  ) {
    const start = minutesFromTime(schedule.start_time)
    const end = minutesFromTime(schedule.end_time)
    if (end > start) {
      totalMinutes = (end - start) * schedule.days_of_week.length
    }
  }
  return totalMinutes / 60
}

/** Get percentage of day (0–100) allocated for each day 0..6 (Mon–Sun) */
export function getScheduleDayPercentages(schedule: {
  time_blocks?: SimpleTimeBlock[]
  days_of_week?: number[]
  start_time?: string
  end_time?: string
}): number[] {
  const out = [0, 0, 0, 0, 0, 0, 0]
  if (schedule.time_blocks && schedule.time_blocks.length > 0) {
    for (const b of schedule.time_blocks) {
      const start = minutesFromTime(b.start_time)
      const end = minutesFromTime(b.end_time)
      if (end > start && b.day_of_week >= 0 && b.day_of_week <= 6) {
        out[b.day_of_week] += (end - start) / MINUTES_PER_DAY
      }
    }
  } else if (
    schedule.days_of_week?.length &&
    schedule.start_time != null &&
    schedule.end_time != null
  ) {
    const start = minutesFromTime(schedule.start_time)
    const end = minutesFromTime(schedule.end_time)
    const pct = end > start ? (end - start) / MINUTES_PER_DAY : 0
    for (const d of schedule.days_of_week) {
      if (d >= 0 && d <= 6) out[d] += pct
    }
  }
  return out.map((p) => Math.min(100, Math.round(p * 100 * 10) / 10))
}

/** Per-day segments as [startPct, endPct] of the 24h day (0–100). Supports multiple blocks per day. */
export function getScheduleDaySegments(schedule: {
  time_blocks?: SimpleTimeBlock[]
  days_of_week?: number[]
  start_time?: string
  end_time?: string
}): [number, number][][] {
  const out: [number, number][][] = [[], [], [], [], [], [], []]
  const toPct = (mins: number) => Math.min(100, Math.max(0, (mins / MINUTES_PER_DAY) * 100))

  if (schedule.time_blocks && schedule.time_blocks.length > 0) {
    for (const b of schedule.time_blocks) {
      const start = minutesFromTime(b.start_time)
      const end = minutesFromTime(b.end_time)
      if (end > start && b.day_of_week >= 0 && b.day_of_week <= 6) {
        out[b.day_of_week].push([toPct(start), toPct(end)])
      }
    }
  } else if (
    schedule.days_of_week?.length &&
    schedule.start_time != null &&
    schedule.end_time != null
  ) {
    const start = minutesFromTime(schedule.start_time)
    const end = minutesFromTime(schedule.end_time)
    if (end > start) {
      const seg: [number, number] = [toPct(start), toPct(end)]
      for (const d of schedule.days_of_week) {
        if (d >= 0 && d <= 6) out[d].push(seg)
      }
    }
  }
  return out
}
