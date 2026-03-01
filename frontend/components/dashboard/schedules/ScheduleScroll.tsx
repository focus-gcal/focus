import type { ReactNode } from "react"

interface ScheduleScrollProps {
  children: ReactNode
  /** Extra inline styles for the scroll container (e.g. paddingTop, flexDirection) */
  style?: React.CSSProperties
}

export function ScheduleScroll({ children, style }: ScheduleScrollProps) {
  return (
    <div
      className="schedule-scroll"
      style={{
        flex: 1,
        minHeight: 0,
        overflowY: "auto",
        overflowX: "hidden",
        WebkitOverflowScrolling: "touch",
        ...style,
      }}>
      {children}
    </div>
  )
}
