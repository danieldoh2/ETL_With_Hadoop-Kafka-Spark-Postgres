import sqlite3


def list_tables(db_name):
    """List all tables in the specified SQLite database."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])

    connection.close()


# List tables in your SQLite database
db_name = 'health_data.db'
print('hi')
list_tables(db_name)


def read_health_events(db_name):
    """Read and print all health events from the specified SQLite database."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM health_events")

    rows = cursor.fetchall()
    for row in rows:
        print(row)

    connection.close()


# # Specify the SQLite database file name
# db_name = 'health_data.db'

# # Read and print the health events
# read_health_events(db_name)
