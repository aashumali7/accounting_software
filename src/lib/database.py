import sqlite3
import bcrypt

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

    def register_user(self, username, password):
        try:
            # Hash the password before inserting into the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed_password, 'admin'))
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
        return False

    def select_company(self):
        # Build the query
        self.cur.execute("SELECT * FROM companies")

        # Execute the query and fetch the result
        result = self.cur.fetchall()
        return result

    def insert_company(self, company_name, financial_year):
        try:
            # Build the query and insert the company data
            query = "INSERT INTO companies (company_name, financial_year) VALUES (?, ?)"
            self.cur.execute(query, (company_name, financial_year))
            self.conn.commit()
            print("Company added successfully.")
        except Exception as e:
            print("Error inserting company:", e)

    def close(self):
        self.conn.close()
