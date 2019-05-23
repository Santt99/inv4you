import pymysql.cursors


class Database:
    def __init__(self):
        host = "a07yd3a6okcidwap.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
        user = "m7479tvdnwwfimqo"
        password = "jse16k4dx7nd6l8l"
        db = "xpba22f95w8rrd8q"
        self.connection = pymysql.connect(host=host, user=user, password=password,db =db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cursor = self.connection.cursor()

    def createUser(self,email,password):
        try:
            with  self.cursor as cursor:
                self.cursor.execute("SELECT * FROM users WHERE email=%s;",(email))
                result = cursor.fetchone()
                if result == None:
                    self.cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)",(email,password))
                    return True
                else: 
                    print("User all ready exists!")
                    return False;
            self.connection.commit()
        finally:
            self.connection.close()
            

    def login(self,email,password):
        response = ""
        try:
            with  self.cursor as cursor:
             
                self.cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s;",(email,password))
                result = cursor.fetchone()
                response = result  
        finally:
            self.connection.close()
            return response
    
    def searchForUserFiles(self,id):
        response = ""
        try:
            with  self.cursor as cursor:
                self.cursor.execute("SELECT name,path,description FROM files WHERE owner_id=%s",(id))
                result = cursor.fetchone()
                response = result  
        finally:
            self.connection.close()
            return response

    def createFile(self, owner_id, name, description, path):
        response = ""
        try:
            with  self.cursor as cursor:
                self.cursor.execute("INSERT INTO files (owner_id, name, description, path) VALUES (%s, %s, %s, %s)",(owner_id, name, description, path))
                return True
            self.connection.commit()
        finally:
            self.connection.close()