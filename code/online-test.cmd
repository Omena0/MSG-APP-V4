cd auth
start "AUTH SERVER" "cmd /C py auth.py"
start cmd /C start "TUNNEL" "Playit-V0.9.3.exe"
cd ../server
start "SERVER" "cmd /C py "server.py"
cd ../client
start "CLIENT" "cmd /C py "client.py"
exit
