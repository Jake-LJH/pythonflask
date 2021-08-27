from model.DatabasePool import DatabasePool
from config.Settings import Settings
import jwt
import datetime
import bcrypt

class User:

    @classmethod

    def getUsers(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "SELECT * FROM user"   
            cursor.execute(sql,[])
            users = cursor.fetchall()
            return users
        finally: 
            dbConn.close()
    
    
    @classmethod
    def getUserByUserid(cls,userid):

        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "SELECT * FROM user WHERE id=%s"   
            cursor.execute(sql,(userid,))
            users = cursor.fetchall()
            return users
        finally: 
            dbConn.close()

    @classmethod
    def insertUser(cls,username, email, role, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            password = password.encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())

            sql = "INSERT into user(username, email, role, password) values(%s,%s,%s,%s)"   
            cursor.execute(sql,(username, email, role, hashed))
            dbConn.commit()
            recordCount = cursor.rowcount
            print(cursor.lastrowid)
            return recordCount
        finally: 
            dbConn.close()
    

    @classmethod
    def updateUser(cls,userid, email, password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "UPDATE user SET email = %s, password= %s WHERE id = %s"   
            cursor.execute(sql,(email, password,userid))
            dbConn.commit()
            recordCount = cursor.rowcount
            return recordCount
        finally: 
            dbConn.close()

    @classmethod
    def deleteUser(cls,userid):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "DELETE from user WHERE id = %s"   
            cursor.execute(sql,(userid,))
            dbConn.commit()

            recordCount = cursor.rowcount
            return recordCount
        finally: 
            dbConn.close()

    @classmethod
    def loginUser(cls,userJSON):
        try:
            dbConn=DatabasePool.getConnection()

            print(userJSON)
            cursor = dbConn.cursor(dictionary=True)
            sql = "select * from user where email=%s"

            cursor.execute(sql,(userJSON["email"],))
            user = cursor.fetchone() #at most 1 record since email is supposed to be unique
            if user==None:
                return {"jwt":""}

            else:
                
                password = userJSON["password"].encode()
                hashed = user['password'].encode()
                
                if bcrypt.checkpw(password, hashed):#True means valid password 
                    payload={"userid":user["id"],"role":user["role"],"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=7200)}

                    jwtToken=jwt.encode(payload,Settings.secretKey,algorithm="HS256")
                    return {"jwt":jwtToken}
                else:
                    return {"jwt":""}
        finally:
            dbConn.close()

    @classmethod
    def login(cls, email):
        try:
            dbConn=DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "select * from user where email= %s"
            cursor.execute(sql,(email,))
            user = cursor.fetchone() #at most 1 record since email is supposed to be unique
            if user==None:
                return {"jwt":""}
            return user
        finally:
            dbConn.close()

