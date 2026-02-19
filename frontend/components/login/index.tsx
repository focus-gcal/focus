// components/login/index.tsx
function Login() {
  return (
    <div style={{ 
      display: "flex", 
      flexDirection: "column", 
      alignItems: "center", 
      justifyContent: "center",
      minHeight: "100%",
      padding: 24 
    }}>
      <img 
        src="/assets/icon.png"   // or your logo path
        alt="Logo" 
        style={{ width: 80, height: 80, marginBottom: 32 }}
      />
      <button
        onClick={() => { /* handle login */ }}
        style={{
          padding: "12px 24px",
          fontSize: 14,
          // your button styles
        }}
      >
        Sign in
      </button>
    </div>
  )
}

export default Login