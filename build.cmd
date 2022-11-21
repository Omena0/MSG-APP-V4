echo off
echo ##########################
echo ### Building CLIENT.py ###
echo ##########################
pyinstaller -y --specpath spec/ -F -n Client.exe -i NONE code/client/client.py

echo #######################
echo ### Build complete! ###
echo #######################
timeout /t 3
