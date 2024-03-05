import sqlite3
import bcrypt
from PyQt6.QtWidgets import QMessageBox

class DatabaseManager:
    # Database properties
    dbname = 'accounting.db'
    sqlfile = 'accounting.sql'

    def __init__(self):
        # Connect to the database and create tables if not exist
        self.conn = sqlite3.connect(f'./data/{self.dbname}')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            # Open the SQL file and read its contents
            with open(f'./data/{self.sqlfile}', 'r') as sql_file:
                sql_script = sql_file.read()

            # Execute the entire SQL script
            self.cur.executescript(sql_script)

            # Commit the changes
            self.conn.commit()
            print("SQL file imported successfully.")
        except Exception as e:
            print("Error importing SQL file:", e)


    def check_if_admin_registered(self):
        try:
            # Build the query
            self.cur.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
            result = self.cur.fetchone()

            # Check if the count is greater than zero
            if result[0] > 0:
                return True
            else:
                return False
        except Exception as e:
            print('Failed')
            print('Error:', e)
            return False
        finally:
            pass

    def register_user(self, username, password, role, compid):
        try:
            # Hash the password before inserting into the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cur.execute("INSERT INTO users (username, password, role, compid) VALUES (?, ?, ?, ?)", (username, hashed_password, role, compid))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            # Unique constraint violated, username already exists
            print("Error registering user:", e)
            return False

    def check_user_in_company(self, username, compid):
        try:
            self.cur.execute("SELECT COUNT(*) FROM users WHERE username=? AND compid=?", (username, compid))
            result = self.cur.fetchone()
            return result[0] > 0
        except Exception as e:
            print("Error checking user in company:", e)
            return False
        
    def check_user_exists(self, username):
        try:
            # Execute a query to count the number of users with the provided username
            self.cur.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
            result = self.cur.fetchone()

            # If the count is greater than 0, the user exists
            return result[0] > 0
        except Exception as e:
            print("Error checking if user exists:", e)
            return False    

    def login_user(self, username, password):
        self.cur.execute("SELECT id, username FROM users WHERE username=?", (username,))
        user_info = self.cur.fetchone()
        if user_info:
            self.cur.execute("SELECT password FROM users WHERE username=?", (username,))
            hashed_password = self.cur.fetchone()[0]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return True
        return False

    def select_company(self):
        # Build the query
        self.cur.execute("SELECT * FROM companies ORDER BY company_name")

        # Execute the query and fetch the result
        result = self.cur.fetchall()
        return result
    
    def select_company_by_name(self, company_name):
        try:
            # Build the query to select the company by name
            query = "SELECT * FROM companies WHERE company_name = ?"
            self.cur.execute(query, (company_name,))
            
            # Fetch the result
            result = self.cur.fetchone()
            return result
        except Exception as e:
            print("Error selecting company by name:", e)
            return None

    def insert_company(self, company_name, address, city, pincode, mobile, email, start_month, start_year, end_month, end_year):
        try:
            # Check if the company name already exists
            existing_company = self.select_company_by_name(company_name)
            if existing_company:
                QMessageBox.warning(None, 'Company Exists', 'Company name already exists.')
                return False

            # Build the query and insert the company data
            query = "INSERT INTO companies (company_name, address, city, pincode, mobile, email, fy_start_month, fy_start_year, fy_end_month, fy_end_year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.cur.execute(query, (company_name, address, city, pincode, mobile, email, start_month, start_year, end_month, end_year))
            self.conn.commit()
            print("Company added successfully.")
            return True
        except Exception as e:
            print("Error inserting company:", e)
            return False            
    
    def close(self):
        self.conn.close()