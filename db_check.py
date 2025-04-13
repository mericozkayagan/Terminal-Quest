#!/usr/bin/env python3

import logging
import sys
import os
from dotenv import load_dotenv

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("db_check")

# Import after logging setup
try:
    from src.config.database import execute_query, init_database
    from src.services.character_storage import CharacterStorageService
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    sys.exit(1)


def check_database_connection():
    """Check if the database connection is working"""
    try:
        # Try to execute a simple query
        result = execute_query("SELECT 1 AS connection_test")
        if result is not None:
            logger.info("✅ Database connection successful")
            return True
        else:
            logger.error("❌ Database connection failed - execute_query returned None")
            return False
    except Exception as e:
        logger.error(f"❌ Database connection failed: {str(e)}")
        return False


def check_tables_exist():
    """Check if the required tables exist"""
    try:
        # Query to check if tables exist
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('characters', 'inventory_items', 'save_slots')
        """

        result = execute_query(query)

        if result is None:
            logger.error("❌ Failed to check tables")
            return False

        table_names = [row["table_name"] for row in result]

        if len(table_names) == 3:
            logger.info(f"✅ All required tables exist: {', '.join(table_names)}")
            return True
        else:
            missing_tables = set(["characters", "inventory_items", "save_slots"]) - set(
                table_names
            )
            logger.error(f"❌ Missing tables: {', '.join(missing_tables)}")
            return False

    except Exception as e:
        logger.error(f"❌ Error checking tables: {str(e)}")
        return False


def check_save_slots():
    """Check if the save slots are initialized"""
    try:
        save_slots = CharacterStorageService.get_save_slots()

        if save_slots is None:
            logger.error("❌ Failed to get save slots")
            return False

        if len(save_slots) == 5:
            logger.info(f"✅ Save slots are initialized: {len(save_slots)} slots found")
            return True
        else:
            logger.error(
                f"❌ Save slots not initialized correctly: Found {len(save_slots)} slots, expected 5"
            )
            return False

    except Exception as e:
        logger.error(f"❌ Error checking save slots: {str(e)}")
        return False


def initialize_database():
    """Initialize database schema"""
    try:
        logger.info("Initializing database schema...")
        success = init_database()

        if success:
            logger.info("✅ Database schema initialized successfully")
            return True
        else:
            logger.error("❌ Failed to initialize database schema")
            return False

    except Exception as e:
        logger.error(f"❌ Error initializing database: {str(e)}")
        return False


def main():
    """Main function"""
    load_dotenv()

    logger.info("Starting database check...")

    # Check database connection
    if not check_database_connection():
        logger.error("Database connection failed. Make sure PostgreSQL is running.")
        sys.exit(1)

    # Check if tables exist
    tables_exist = check_tables_exist()

    # If tables don't exist, initialize database
    if not tables_exist:
        logger.info("Required tables don't exist. Initializing database...")
        if not initialize_database():
            logger.error("Failed to initialize database. Exiting.")
            sys.exit(1)

    # Check save slots
    if not check_save_slots():
        logger.info("Reinitializing database to fix save slots...")
        if not initialize_database():
            logger.error("Failed to reinitialize database. Exiting.")
            sys.exit(1)

        # Check save slots again
        if not check_save_slots():
            logger.error(
                "Still failed to initialize save slots. Check your database configuration."
            )
            sys.exit(1)

    logger.info("Database check completed successfully.")


if __name__ == "__main__":
    main()
