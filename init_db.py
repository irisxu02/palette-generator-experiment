import sqlite3

DATABASE = 'db.sqlite'

def init_db():
    conn = sqlite3.connect(DATABASE)
    with conn:
        cursor = conn.cursor()

        # Read and execute the schema.sql file
        with open('schema.sql', 'r') as schema_file:
            schema_sql = schema_file.read()
            cursor.executescript(schema_sql)

if __name__ == '__main__':
    init_db()
