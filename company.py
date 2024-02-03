import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QFormLayout, QLineEdit, QLabel
from src.lib.database import DatabaseManager

class CompanyForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Create Company Form')
        self.setGeometry(100, 100, 1000, 500)

        layout = QFormLayout(self)

        # Company details fields
        self.company_name_edit = QLineEdit(self)
        self.company_address_edit = QLineEdit(self)
        self.company_city_edit = QLineEdit(self)
        self.company_pincode_edit = QLineEdit(self)
        self.company_country_edit = QLineEdit(self)
        self.company_email_edit = QLineEdit(self)
        self.company_mobile_edit = QLineEdit(self)

        layout.addRow('Company Name:', self.company_name_edit)
        layout.addRow('Address:', self.company_address_edit)
        layout.addRow('City:', self.company_city_edit)
        layout.addRow('Pincode:', self.company_pincode_edit)
        layout.addRow('Country:', self.company_country_edit)
        layout.addRow('Email:', self.company_email_edit)
        layout.addRow('Mobile Number:', self.company_mobile_edit)

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

        # Create a horizontal layout for the image and button
        image_button_layout = QHBoxLayout()

        # Add the button and set it to a fixed size
        small_button = QPushButton('Create Company', self)
        small_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Connect the button click to the slot method
        small_button.clicked.connect(self.show_company_form)

        # Add the button to the horizontal layout
        image_button_layout.addWidget(small_button)

        # Add the image and button layout to the main layout
        main_layout.addLayout(image_button_layout)

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
        company_data = self.db.selectCompany()

        # Set the number of rows and columns in the table
        num_rows = len(company_data)
        num_cols = len(company_data[0]) if num_rows > 0 else 0

        self.company_table.setRowCount(num_rows)
        self.company_table.setColumnCount(num_cols)

        # Populate the table with data
        for row_index, row_data in enumerate(company_data):
            for col_index, col_value in enumerate(row_data):
                item = QTableWidgetItem(str(col_value))
                self.company_table.setItem(row_index, col_index, item)

        # Hide the vertical header (column count indicator)
        self.company_table.verticalHeader().setVisible(False)

        # Add labels at the top of the table
        header_labels = ['Id', 'Company Name']
        for col_index, label in enumerate(header_labels):
            header_item = QTableWidgetItem(label)
            self.company_table.setHorizontalHeaderItem(col_index, header_item)

        # Set the size of the "Id" column
        self.company_table.setColumnWidth(0, 50)
        # Set the size of the "Company Name" column
        self.company_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    def show_company_form(self):
        company_form = CompanyForm()
        result = company_form.exec()

        if result == QDialog.DialogCode.Accepted:
            # Retrieve values from the form if needed
            company_name = company_form.company_name_edit.text()
            company_address = company_form.company_address_edit.text()
            company_city = company_form.company_city_edit.text()
            company_pincode = company_form.company_pincode_edit.text()
            company_country = company_form.company_country_edit.text()
            company_email = company_form.company_email_edit.text()
            company_mobile = company_form.company_mobile_edit.text()

            # Add the company to the database
            self.db.insert_company(company_name)

            # Refresh the table with updated data
            self.populate_table()

            # Process the form data as needed
            print(f'Company Name: {company_name}')
            print(f'Address: {company_address}')
            print(f'City: {company_city}')
            print(f'Pincode: {company_pincode}')
            print(f'Country: {company_country}')
            print(f'Email: {company_email}')
            print(f'Mobile Number: {company_mobile}')


def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
