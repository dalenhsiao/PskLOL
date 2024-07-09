# CREATE TABLES

table_create = """
    CREATE TABLE IF NOT EXISTS cmu (
        id SERIAL PRIMARY KEY,
        display_name TEXT,
        last_name VARCHAR(50),

)"""
