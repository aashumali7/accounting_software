import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from src.lib.database import DatabaseManager

class CompanyForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Create Company Form')
        self.setGeometry(100, 100, 1000, 500)

        layout = QFormLayout(self)

        # Company details fields
        self.company_name_edit = QLineEdit(self)
        self.address_edit = QLineEdit(self)
        self.city_edit = QLineEdit(self)
        self.pincode_edit = QLineEdit(self)
        self.mobile_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        
        # Financial Year dropdown
        self.financial_year_combo = QComboBox(self)
        self.financial_year_combo.addItems(['2018-2019','2019-2020','2020-2021','2021-2022','2022-2023', '2023-2024', '2024-2025',])  # Add your desired options

        layout.addRow('Company Name:', self.company_name_edit)
        layout.addRow('Address:', self.address_edit)
        layout.addRow('City:', self.city_edit)
        layout.addRow('Pin Code:', self.pincode_edit)
        layout.addRow('Mobile:', self.mobile_edit)
        layout.addRow('Email:', self.email_edit)
        layout.addRow('Financial Year:', self.financial_year_combo)

        # OK and Cancel buttons
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton('OK', self)
        cancel_button = QPushButton('Cancel', self)

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addRow(buttons_layout)

class BasicWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Basic PyQt6 Window')
        self.showMaximized()

        # Create a layout for the entire window
        main_layout = QVBoxLayout(self)

        # Create a horizontal layout for the "Create Company" button
        create_company_layout = QVBoxLayout()

        # Add the create company button
        create_company_button = QPushButton('Create Company', self)
        create_company_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        create_company_button.clicked.connect(self.show_company_form)
        
        # Set button text to bold
        font = create_company_button.font()
        font.setBold(True)
        create_company_button.setFont(font)
        
        create_company_layout.addWidget(create_company_button)

        # Add the "Create Company" layout to the main layout
        main_layout.addLayout(create_company_layout)

        # Create a table
        self.company_table = QTableWidget(self)
        main_layout.addWidget(self.company_table)

        # Set stretch factor to make the table columns responsive
        header = self.company_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Fill the table with data
        self.populate_table()

        # Set the layout for the main window
        self.setLayout(main_layout)

    def populate_table(self):
        # Fetch data from the database
        company_data = self.db.select_company()

        # Set the number of rows and columns in the table
        num_rows = len(company_data)
        num_cols = len(company_data[0]) if num_rows > 0 else 0

        self.company_table.setRowCount(num_rows)
        self.company_table.setColumnCount(num_cols + 1)  # Add 1 for the extra column

        if num_rows > 0:
            # Populate the table with data
            for row_index, row_data in enumerate(company_data):
                for col_index, col_value in enumerate(row_data):
                    item = QTableWidgetItem(str(col_value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item not editable
                    self.company_table.setItem(row_index, col_index, item)

                # Add a fixed "Login" button in the last column
                login_button = QPushButton('Login', self)
                login_button.clicked.connect(self.login_clicked)
                self.company_table.setCellWidget(row_index, num_cols, login_button)

            # Add labels at the top of the table
            header_labels = ['Id', 'Company Name', 'Financial Year', "Action"]  # Updated header_labels
            for col_index, label in enumerate(header_labels):
                header_item = QTableWidgetItem(label)
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
                self.company_table.setHorizontalHeaderItem(col_index, header_item)

            # Set the size of the "Id" column
            self.company_table.setColumnWidth(0, 50)  # Set a fixed width for the ID column
            self.company_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)

            # Set the size of the "Company Name" column
            self.company_table.setColumnWidth(1, 120)  # Adjust the width as needed
            self.company_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

            # Set the size of the "Financial Year" column
            self.company_table.setColumnWidth(2, 80)  # Adjust the width as needed
            self.company_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

            # Set stretch factor to make the other columns responsive
            for col_index in range(3, num_cols + 1):  # Adjust the range
                self.company_table.horizontalHeader().setSectionResizeMode(col_index, QHeaderView.ResizeMode.Stretch)
        else:
            # No data, clear the header labels and set column sizes
            self.company_table.setHorizontalHeaderLabels([])
            self.company_table.setColumnWidth(0, 50)  # Set a fixed width for the ID column
            self.company_table.setColumnWidth(1, 120)
            self.company_table.setColumnWidth(2, 80)

    def show_company_form(self):
        company_form = CompanyForm()
        result = company_form.exec()

        if result == QDialog.DialogCode.Accepted:
            # Retrieve values from the form
            company_name = company_form.company_name_edit.text()
            financial_year = company_form.financial_year_combo.currentText()

            # Add the company to the database
            self.db.insert_company(company_name, financial_year)

            # Refresh the table with updated data
            self.populate_table()

            QMessageBox.information(self, 'Success', 'Company was created successfully.')

            # Process the form data as needed
            print(f'Company Name: {company_name}')
            print(f'Financial Year: {financial_year}')

    def login_clicked(self):
        # Implement the login functionality here
        QMessageBox.information(self, 'Login', 'Login button clicked.')

def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
