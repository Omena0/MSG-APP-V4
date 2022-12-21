cd server
start "SERVER" "cmd /C py "server.py"
cd ../client
start "CLIENT" "cmd /C py "client.py"
exit
