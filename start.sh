#!/bin/bash

echo "Terminal Quest - Starting environment..."

# Detect OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Windows OS detected"
    RUNNING_ON_WINDOWS=true
else
    RUNNING_ON_WINDOWS=false
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python is not installed or not in PATH. Please install Python 3."
        exit 1
    else
        PY_CMD="python"
    fi
else
    PY_CMD="python3"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
$PY_CMD -m pip install -r requirements.txt

# Check if PostgreSQL is already running on the system
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="terminal_quest"
DB_PASSWORD="password"
DB_NAME="terminal_quest"

# Test if we can connect to the existing database
if $PY_CMD -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='$DB_HOST',
        port='$DB_PORT',
        user='$DB_USER',
        password='$DB_PASSWORD',
        database='$DB_NAME'
    )
    conn.close()
    print('Connection successful!')
    exit(0)
except Exception as e:
    print(f'Connection failed: {e}')
    exit(1)
" &> /dev/null; then
    echo "PostgreSQL database is already configured and accessible. Using existing database."

    # Run the game
    echo "Starting Terminal Quest..."
    $PY_CMD main.py
    exit 0
fi

# If we reach here, we need to check for Docker

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Warning: Docker is not installed or not in PATH."
    echo "The game will run without save functionality."
    echo "Install Docker and Docker Compose for save/load features."

    # Run the game without DB
    echo "Starting Terminal Quest without database..."
    $PY_CMD main.py
    exit 0
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Warning: Docker Compose is not installed or not in PATH."
    echo "The game will run without save functionality."
    echo "Install Docker Compose for save/load features."

    # Run the game without DB
    echo "Starting Terminal Quest without database..."
    $PY_CMD main.py
    exit 0
fi

# Check if port 5432 is already in use (but not by our DB)
PORT_CHECKER="lsof -i :5432"
if $RUNNING_ON_WINDOWS; then
    PORT_CHECKER="netstat -ano | findstr :5432"
fi

if eval $PORT_CHECKER &> /dev/null; then
    echo "Warning: Port 5432 is already in use by another PostgreSQL instance."
    echo "Options:"
    echo "  1. Continue without save functionality"
    echo "  2. Try to use the existing PostgreSQL (may require manual setup)"
    echo "  3. Exit and modify docker-compose.yml to use a different port"

    read -p "Choose an option (1-3): " port_option

    case $port_option in
        1)
            echo "Starting Terminal Quest without database..."
            $PY_CMD main.py
            exit 0
            ;;
        2)
            echo "Please set up the database manually with these credentials:"
            echo "  Host: localhost"
            echo "  Port: 5432"
            echo "  User: terminal_quest"
            echo "  Password: password"
            echo "  Database: terminal_quest"
            echo "Starting Terminal Quest..."
            $PY_CMD main.py
            exit 0
            ;;
        3)
            echo "Exiting. Please edit docker-compose.yml and change the port mapping."
            echo "For example, change '5432:5432' to '5433:5432'"
            exit 1
            ;;
        *)
            echo "Invalid option. Exiting."
            exit 1
            ;;
    esac
fi

# Start the database container
echo "Starting PostgreSQL database container..."
if ! docker-compose up -d; then
    echo "Failed to start database container. The game will run without save functionality."
    $PY_CMD main.py
    exit 0
fi

# Function to check DB connection
check_db_connection() {
    if $RUNNING_ON_WINDOWS; then
        # On Windows, we'll try to connect using Python
        $PY_CMD -c "
        import time
        import psycopg2
        try:
            conn = psycopg2.connect(
                host='$DB_HOST',
                port='$DB_PORT',
                user='$DB_USER',
                password='$DB_PASSWORD',
                database='$DB_NAME'
            )
            conn.close()
            exit(0)
        except Exception:
            exit(1)
        " &> /dev/null
        return $?
    else
        # On other platforms, we can use pg_isready
        docker exec terminal-quest-db pg_isready -U terminal_quest &> /dev/null
        return $?
    fi
}

# Wait for database to be ready
echo "Waiting for database to be ready..."
for i in {1..10}; do
    if check_db_connection; then
        echo "Database is ready!"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "Database did not become ready in time. The game will run, but save functionality may not work."
    fi
    echo "Waiting for database... ($i/10)"
    sleep 2
done

# Run the game
echo "Starting Terminal Quest..."
$PY_CMD main.py

# Cleanup on exit
cleanup() {
    echo "Cleaning up..."
    # Keep containers running in case the user wants to play again
    # To stop containers, run: docker-compose down
}

trap cleanup EXIT
