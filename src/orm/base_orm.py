class BaseORM:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    