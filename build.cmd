echo off
echo ##########################
echo ### Building CLIENT.py ###
echo ##########################
pyinstaller --noconfirm --i NONE --specpath spec --onefile code/client/client.py
echo ##########################
echo ### Building SERVER.py ###
echo ##########################
pyinstaller --noconfirm --i NONE --specpath spec --onefile code/server/server.py
echo ###############################
echo ### Building AUTH-SERVER.py ###
echo ###############################
pyinstaller --noconfirm --i NONE --specpath spec --onefile code/auth/auth.py
echo #######################
echo ### Build complete! ###
echo #######################
del spec /q
timeout /t 3
