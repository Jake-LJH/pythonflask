from model.DatabasePool import DatabasePool

class Furniture:

    @classmethod
    def getFurnitureByCat(cls,catid):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql="SELECT c.cat_id, cat_name, f.description, dimension, images, it_id, item_code, name, price, quantity FROM category c, furniture f WHERE f.cat_id = c.cat_id"
        cursor.execute(sql)
        furniture = cursor.fetchall()

        dbConn.close()

        return furniture