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
        except e:
            print(e)
        finally:
            cursor.close()
            return result

    def addColumn(self, tableTitle, columnTitle):
        cursor = self.connection.cursor()
        result = False
        try:
            with  cursor:
                    query = "ALTER TABLE " + tableTitle + " ADD " + columnTitle + " VARCHAR(255);"
                    print(query)
                    cursor.execute(query)
                    result =  True
            self.connection.commit()
        except e:
            print(e)
        finally:
            cursor.close()
            return result
            
    def extractTableData(self,table):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                query = "SELECT * FROM xpba22f95w8rrd8q.`" + table + "`;"
                print(query)
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
        except e:
            print(e)
        finally:
            cursor.close()
            return response

    def createSQLTable(self, tableTitle):
        cursor = self.connection.cursor()
        response = False
        try:
            with  cursor:
                query = "CREATE TABLE " + str(tableTitle) + " (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY);"
                cursor.execute(query)
                cursor.execute("INSERT INTO " + str(tableTitle) +" (id) values(0);")
                result = cursor.fetchall()
                response = True
        except e:
            print(e)
            response = False
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
        except e:
            print(e)
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
        except:
            print("Error!")
        finally:
            cursor.close()
            return response
            
    def addCustomRow(self, table, columns, values):
        cursor = self.connection.cursor()
        query = ""
        try:
            with  cursor:
                query = "INSERT INTO `" + str(table) + "` (" + str(columns[0]) + ", "
                for column in range(1,len(columns) - 1):
                    query += str(columns[column]) + ", "
                query +=  str(columns[len(columns)-1]) + ") VALUES ('" + str(values[0]) + "', "
                for value in range(1,len(values) - 1):
                    query +=  "'" + str(values[value]) + "', "
                query += "'" + str(values[len(values)-1]) + "');"             
                cursor.execute(query)
            self.connection.commit()
        except :
            print("Error!")
            return query
        finally:
            cursor.close()

    def editCustomRow(self, table, rowId , columns, values):
        cursor = self.connection.cursor()
        query = ""
        try:
            with  cursor:
                query = "UPDATE `" + str(table) + "` SET "
                query += columns[0] + "='" + values[0] + "'"
                for curr in range(1,len(columns)):
                    query += ", " + columns[curr] + "='" + values[curr] + "'"
                query += " WHERE id=" + rowId + ";";
                cursor.execute(query)
            self.connection.commit()
        except :
            print("Error!")
            return query
        finally:
            cursor.close()

    def deleteInventory(self,id, tableTitle):
        cursor = self.connection.cursor()
        try:
            with  cursor:
                query = "DELETE FROM inventories WHERE inventory_id=" + str(id) + ";"
                cursor.execute(query)
                if tableTitle != "inventories" and tableTitle != "users":
                    cursor.execute("DROP TABLE " + tableTitle + ";")
            self.connection.commit()
        except:
            return False
        finally:
            cursor.close()
            return True
    def searchForRowDataById(self, id, tableTitle):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                cursor.execute("SELECT * FROM `" + tableTitle + "` " + "WHERE id=" + id + ";")
                result = cursor.fetchone()
                response = result  
        except:
            return False
        finally:
            cursor.close()
            return response
        
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

    def searchForDataInTableByColumn(self, tableTitle, columnTitle, valueToSearch):
        cursor = self.connection.cursor()
        response = ""
        try:
            with  cursor:
                query = "SELECT * FROM `" + tableTitle + "`" "WHERE " + columnTitle + " like '%" + valueToSearch  + "%';";  
                print(query)
                cursor.execute(query)
                result = cursor.fetchall()
                response = result  
        except:
            print("Error!")
        finally:
            cursor.close()
            return response
        