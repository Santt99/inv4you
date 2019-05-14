import pymysql.cursors


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = "2Bytes1Bit.2018"
        self.connection = pymysql.connect(host=host, user=user, password=password,db ="inv4you", cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cursor = self.connection.cursor()

    def createUser(self,email,password):
        try:
            with  self.cursor as cursor:
                self.cursor.execute("SELECT * FROM inv4you.users WHERE email=%s;",(email))
                result = cursor.fetchone()
                if result == None:
                    self.cursor.execute("INSERT INTO users (email, pass) VALUES (%s, %s)",(email,password))
                else: 
                    print("User all ready exists!")
            self.connection.commit()
        finally:
            self.connection.close()
            return True

    def login(self,email,password):
        response = ""
        try:
            with  self.cursor as cursor:
             
                self.cursor.execute("SELECT * FROM inv4you.users WHERE email=%s AND pass=%s;",(email,password))
                result = cursor.fetchone()
                response = result  
        finally:
            self.connection.close()
            return response
