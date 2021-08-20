from mysql.connector import pooling

class DatabasePool:
    #class variable
    connection_pool = pooling.MySQLConnectionPool(
                               pool_name="ws_pool",
                               pool_size=5,
                               host='localhost',
                               database='furniture',
                               user='root',
                               password='')

    @classmethod
    def getConnection(cls): 
        dbConn = cls.connection_pool.get_connection()
        return dbConn
