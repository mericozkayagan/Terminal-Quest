@echo off
echo Terminal Quest - Starting environment...

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH. Please install Python 3.
    pause
    exit /b 1
)

:: Check if Docker is installed
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Docker is not installed or not in PATH.
    echo The game will run without save functionality.
    echo Install Docker and Docker Compose for save/load features.
    echo Installing Python dependencies...
    python -m pip install -r requirements.txt
    echo Starting Terminal Quest without database...
    python main.py
    pause
    exit /b 0
)

:: Check if Docker Compose is installed
where docker-compose >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Docker Compose is not installed or not in PATH.
    echo The game will run without save functionality.
    echo Install Docker Compose for save/load features.
    echo Installing Python dependencies...
    python -m pip install -r requirements.txt
    echo Starting Terminal Quest without database...
    python main.py
    pause
    exit /b 0
)

:: Install Python dependencies
echo Installing Python dependencies...
python -m pip install -r requirements.txt

:: Check if port 5432 is already in use
netstat -ano | findstr :5432 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Warning: Port 5432 is already in use.
    echo You may have another PostgreSQL server running.
    echo Would you like to continue anyway? The game will run without save functionality. (y/n)
    set /p response=
    if /i "%response%"=="y" (
        echo Starting Terminal Quest without database...
        python main.py
        pause
        exit /b 0
    ) else (
        echo Exiting. Please stop any PostgreSQL server running on port 5432 and try again.
        pause
        exit /b 1
    )
)

:: Start the database container
echo Starting PostgreSQL database container...
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo Failed to start database container. The game will run without save functionality.
    python main.py
    pause
    exit /b 0
)

:: Wait for database to be ready
echo Waiting for database to be ready...
echo This may take a few moments...
timeout /t 10 >nul

:: Run the game
echo Starting Terminal Quest...
python main.py

echo Cleaning up...
:: Keep containers running in case the user wants to play again
:: To stop containers, run: docker-compose down

pause
