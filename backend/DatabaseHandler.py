import psycopg2

class DatabaseHandler:
    def __init__(self, db_config):
        # Establish a connection to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname=db_config['DATABASE_NAME'],
            user=db_config['DATABASE_USER'],
            password=db_config['DATABASE_PASSWORD'],
            host=db_config['DATABASE_HOST'],
            port=db_config['DATABASE_PORT']
        )
        # Create a cursor object
        self.cursor = self.conn.cursor()

    # Execute a SQL query
    def execute_query(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    # Fetch a single row from the result of a SQL query
    def fetch_one(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    # Fetch all rows from the result of a SQL query
    def fetch_all(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()