#!/usr/bin/env python3
"""
Script to reset migration state (for testing purposes)
"""

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def reset_migration():
    """Reset migration state to allow re-migration"""
    print("🔄 Resetting migration state...")
    print("=" * 50)
    
    try:
        # Connect to database
        conn = sqlite3.connect(os.getenv('DB_NAME'))
        cursor = conn.cursor()
        
        # Reset migration state
        cursor.execute("UPDATE library_migration_state SET migration_completed = 0 WHERE id = 1")
        conn.commit()
        
        print("✅ Migration state reset successfully!")
        print("💡 Next time you start the app, migration will run again")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error resetting migration: {e}")

if __name__ == "__main__":
    reset_migration()
