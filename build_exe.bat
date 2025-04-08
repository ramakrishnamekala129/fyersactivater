@echo off
echo Building Fyers Auth GUI executable...
pyinstaller --onefile --windowed --name FyersAuthGUI fyers_auth_gui.py
echo Done! Executable created in dist folder.
pause