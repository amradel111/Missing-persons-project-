@echo off
echo Starting Redis Server...
echo.

SET REDIS_PATH=D:\project\Redis-x64-5.0.14.1
SET REDIS_PORT=6380

echo Using Redis from: %REDIS_PATH%
echo Using port: %REDIS_PORT%
echo.
echo If Redis starts successfully, you will see the Redis logo and messages like "Ready to accept connections".
echo The server will continue running in this window. Do not close it.
echo.

cd /d "D:\project\Missing-persons-project"

REM Check if redis-server.exe exists
IF NOT EXIST "%REDIS_PATH%\redis-server.exe" (
    echo ERROR: redis-server.exe not found at %REDIS_PATH%\redis-server.exe
    echo Please check the path and try again.
    goto :end
)

echo Starting Redis on port %REDIS_PORT%...
%REDIS_PATH%\redis-server.exe --port %REDIS_PORT%

:end
echo.
echo Redis server has stopped. Check for errors above.
pause 