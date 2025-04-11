import os
import logging
from typing import Dict, Any, Optional
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "terminal_quest"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "terminal_quest"),
}


def get_connection():
    """Get a database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            cursor_factory=RealDictCursor,
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return None


def execute_query(query: str, params: tuple = None) -> Optional[list]:
    """Execute a query and return results"""
    conn = None
    try:
        conn = get_connection()
        if not conn:
            logger.error("Failed to get database connection")
            return None

        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith(("SELECT", "RETURNING")):
                result = cursor.fetchall()
                return result
            conn.commit()
            return []

    except Exception as e:
        logger.error(f"Database query error: {str(e)}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def init_database():
    """Initialize the database schema"""
    create_tables_query = """
    -- Create characters table
    CREATE TABLE IF NOT EXISTS characters (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        char_class VARCHAR(50) NOT NULL,
        level INTEGER NOT NULL DEFAULT 1,
        exp INTEGER NOT NULL DEFAULT 0,
        exp_to_level INTEGER NOT NULL DEFAULT 100,
        health INTEGER NOT NULL,
        max_health INTEGER NOT NULL,
        attack INTEGER NOT NULL,
        defense INTEGER NOT NULL,
        mana INTEGER NOT NULL,
        max_mana INTEGER NOT NULL,
        gold INTEGER NOT NULL DEFAULT 0,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    -- Create inventory table
    CREATE TABLE IF NOT EXISTS inventory_items (
        id SERIAL PRIMARY KEY,
        character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
        item_type VARCHAR(20) NOT NULL,
        item_name VARCHAR(100) NOT NULL,
        item_data JSONB NOT NULL,
        equipped BOOLEAN NOT NULL DEFAULT FALSE,
        slot VARCHAR(20) NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );

    -- Create save slots table
    CREATE TABLE IF NOT EXISTS save_slots (
        id SERIAL PRIMARY KEY,
        slot_number INTEGER NOT NULL CHECK (slot_number BETWEEN 1 AND 5),
        character_id INTEGER REFERENCES characters(id) ON DELETE SET NULL,
        last_saved_at TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE (slot_number)
    );

    -- Initialize save slots
    INSERT INTO save_slots (slot_number)
    SELECT generate_series(1, 5)
    ON CONFLICT DO NOTHING;
    """

    try:
        execute_query(create_tables_query)
        logger.info("Database schema initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        return False
