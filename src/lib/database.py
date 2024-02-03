import sqlite3
import bcrypt

class DatabaseManager:
    #1. Property/Varible/State
    dbname='accounting.db'
    sqlfile='accounting.sql'
    
    #2. Constructor/Esp. Function/Method/
    def __init__(self ):# default paramater/argument
        self.conn = sqlite3.connect(f'./data/{self.dbname}')
        self.cur = self.conn.cursor()
        self.create_table()
        
    #3. Method/Function/Behaviours
   
    def create_table(self):
        # Step 1: Open a database connection
                    # module.method(aa)
        try:
            # Step 2: Open the SQL file and read its contents
            with open(f'./data/{self.sqlfile}', 'r') as sql_file:
                sql_script = sql_file.read()

            # Step 3: Execute the SQL commands in the file
            self.cur.executescript(sql_script)
            # Insert some data into the table
            #cursor.execute("DELETE FROM users;")
            # Hash the password before inserting into the database
            #hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
            # Insert some data into the table with the hashed password
            #object.method("string",(tuple1,tuple2,tuple3))
            #self.cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",('admin', hashed_password, 'admin'))

            # Commit the changes
            self.conn.commit()
            print("SQL file imported successfully.")
            
        except Exception as e:
            print("Error importing SQL file:", e)
    
    def checkIfAdminRegister(self):
        try:
            
            #2 Build the query
            self.cur.execute("SELECT COUNT(*) FROM users where role='admin'")
            
            # Execute the query and fetch the result
            result =  self.cur.fetchone()
            print(result)
            print(result[0])
            # Check if the count is greater than zero
            if result[0] > 0:
                return True
            else:
                return False
            pass
        except Exception as e:
            print('Failed')
            print('Hello',e)
            
            pass
        finally:
            
            pass
    
    def register_user(self, username, password):
        try:
            # Hash the password before inserting into the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cur.execute("INSERT INTO users (username, password,role) VALUES (?, ?, ?)", (username, hashed_password,'admin'))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Unique constraint violated, username already exists
            return False

    def login_user(self, username, password):
        self.cur.execute("SELECT id, username FROM users WHERE username=?", (username,))
        user_info = self.cur.fetchone()
        if user_info:
            self.cur.execute("SELECT password FROM users WHERE username=?", (username,))
            hashed_password = self.cur.fetchone()[0]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return True
        else:
            False
        
    def selectCompany(self):
        #2 Build the query
        self.cur.execute("SELECT * FROM companies")
        
        # Execute the query and fetch the result
        result =  self.cur.fetchall()
        return result
        pass

    def close(self):
        self.conn.close()