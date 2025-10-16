@echo off
REM Build script for Capacitor Simulator C Library (Windows)

echo Building Capacitor Simulator C Library...
echo.

REM Create build directory if it doesn't exist
if not exist "build" mkdir build

REM Compile the C library
echo Compiling physics.c...
gcc -Wall -Wextra -shared -O2 -o build/libcapacitor_simulator.dll src/physics.c src/simulator.c -lm

if %errorlevel% neq 0 (
    echo Error: Failed to compile the library
    pause
    exit /b 1
)

REM Copy the library to the expected location
echo Copying library to src directory...
copy build\libcapacitor_simulator.dll src\ >nul

echo.
echo Build completed successfully!
echo Library created: src/libcapacitor_simulator.dll
echo.
pause
