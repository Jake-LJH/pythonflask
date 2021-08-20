from model.DatabasePool import DatabasePool

class Category:

    @classmethod
    def getAllCategory(cls):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql="select * from category"
        cursor.execute(sql)
        category = cursor.fetchall()

        dbConn.close()

        return category

