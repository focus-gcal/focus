import type { ReactNode } from "react"

interface ScheduleScreenLayoutProps {
  children: ReactNode
}

export function ScheduleScreenLayout({ children }: ScheduleScreenLayoutProps) {
  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        maxWidth: 480,
        width: "100%",
        margin: "0 auto",
        display: "flex",
        flexDirection: "column",
        minHeight: 0,
      }}>
      {children}
    </div>
  )
}
