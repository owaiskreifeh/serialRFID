@echo off
echo ========================================
echo    RFID Application Builder
echo ========================================
echo.
echo Choose your packaging method:
echo.
echo 1. PyInstaller (Recommended - Single EXE)
echo 2. Auto-py-to-exe (GUI Interface)
echo 3. cx_Freeze (Alternative)
echo 4. Install all tools
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto pyinstaller
if "%choice%"=="2" goto auto_py_to_exe
if "%choice%"=="3" goto cxfreeze
if "%choice%"=="4" goto install_tools
if "%choice%"=="5" goto exit
goto invalid

:pyinstaller
echo.
echo Building with PyInstaller...
python build_exe.py
goto end

:auto_py_to_exe
echo.
echo Launching Auto-py-to-exe GUI...
python build_gui.py
goto end

:cxfreeze
echo.
echo Building with cx_Freeze...
echo Installing cx_Freeze...
pip install cx_Freeze
echo Building executable...
python setup_cxfreeze.py build
echo.
echo Build completed! Check the build/ directory.
goto end

:install_tools
echo.
echo Installing all packaging tools...
pip install pyinstaller
pip install auto-py-to-exe
pip install cx_Freeze
echo.
echo All tools installed successfully!
goto end

:invalid
echo.
echo Invalid choice. Please enter 1-5.
pause
goto end

:exit
echo.
echo Goodbye!
exit /b 0

:end
echo.
echo Press any key to exit...
pause >nul
