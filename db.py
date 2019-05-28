import pymysql.cursors


class Database:
    def __init__(self):
        host = "a07yd3a6okcidwap.cbetxkdyhwsb.us-east-1.rds.amazonaws.com"
        user = "m7479tvdnwwfimqo"
        password = "jse16k4dx7nd6l8l"
        db = "xpba22f95w8rrd8q"
        self.connection = pymysql.connect(host=host, user=user, password=password,db =db, cursorclass=pymysql.cursors.
                                   DictCursor)
       

    def createUser(self,email,password):
        cursor = self.connection.cursor()
        try:
            with  cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s;",(email))
                result = cursor.fetchone()
                if result == None:
                    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s);",(email,password))
                    result =  True
                else: 
                    print("User all ready exists!")
                    result =  False
            self.connection.commit()
        finally:
            cursor.close()
            return result
            
    def extractTableData(self,table):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                query = "SELECT * FROM xpba22f95w8rrd8q.`" + table + "`"
                cursor.execute(query)
                result = cursor.fetchall()
                response = result
        except e:
            print(e)
        finally:
            cursor.close()
            return response

    def getTableNameById(self, id):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                query = "SELECT title FROM inventories WHERE inventory_id=" + str(id) + ";"
                cursor.execute(query)
                result = cursor.fetchall()
                response = result  
        finally:
            cursor.close()
            return response

    def login(self,email,password):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s;",(email,password))
                result = cursor.fetchone()
                response = result  
        finally:
            cursor.close()
            return response
    
    def searchForUserInventories(self,id):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                query = "SELECT title,description,inventory_id FROM inventories WHERE owner_id=" + str(id) + ";"
                cursor.execute(query)
                result = cursor.fetchall()
                response = result  
        finally:
            cursor.close()
            return response
            

    def deleteInventory(self,id):
        cursor = self.connection.cursor()
        try:
            with  cursor:
                query = "DELETE FROM inventories WHERE inventory_id=" + str(id) + ";"
                cursor.execute(query)
            self.connection.commit()
        except:
            return False
        finally:
            cursor.close()
            return True

    def createInventory(self, owner_id, title, description):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                cursor.execute("INSERT INTO inventories (owner_id, title ,description) VALUES (%s, %s, %s)",(owner_id, title, description))
            self.connection.commit()
        except:
            return False
        finally:
            cursor.close()
            return True