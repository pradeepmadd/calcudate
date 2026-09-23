@echo off
echo ========================================================
echo   Date ^& Time Calculator Pro - .exe Builder
echo ========================================================
echo.
echo Installing required libraries...
pip install pyinstaller ttkbootstrap python-dateutil

echo.
echo Compiling the app into an executable...
pyinstaller --onefile --windowed --noconsole calculator_pro.py

echo.
echo ========================================================
echo DONE!
echo You can find your new 'calculator_pro.exe' inside the 'dist' folder.
echo ========================================================
pause
