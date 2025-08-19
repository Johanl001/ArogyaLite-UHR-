import os
from backend.database.sqlite_manager import SQLiteManager

DB_PATH = os.getenv("DB_PATH", "./data/health.db")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    mgr = SQLiteManager(DB_PATH)
    mgr.init_db()
    print("Initialized DB at", DB_PATH)
