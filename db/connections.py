import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.NAME='SHEMS'
        self.USER='postgres'
        self.PASSWORD='root'
        self.HOST = 'localhost'
        self.port = 5432
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(database=self.NAME,
                                     user=self.USER,
                                     password=self.PASSWORD,
                                     host=self.HOST,
                                     port=self.port)
        return self.conn

    def terminate(self):
        if self.conn is None:
            return
        self.conn.close()
        self.conn = None