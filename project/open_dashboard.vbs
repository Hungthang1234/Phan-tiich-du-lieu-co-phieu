Set objShell = CreateObject("WScript.Shell")

' Wait a bit for server to start
WScript.Sleep(2000)

' Open dashboard in default browser
objShell.Run "http://localhost:5000", , False

' Show message
objShell.Popup "Dashboard dang chay tai http://localhost:5000", 3, "Dashboard"
