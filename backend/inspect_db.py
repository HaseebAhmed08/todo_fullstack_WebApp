import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("NEON_DB_URL")

if not DATABASE_URL:
    print("DATABASE_URL not set")
    exit(1)

print(f"Connecting to: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    table_names = inspector.get_table_names()
    print(f"Tables found: {table_names}")
    
    for table_name in table_names:
        print(f"\n--- Table: {table_name} ---")
        columns = inspector.get_columns(table_name)
        for column in columns:
            print(f"  - {column['name']} ({column['type']})")

except Exception as e:
    print(f"Error: {e}")
