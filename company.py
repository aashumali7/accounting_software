import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox, QAbstractItemView, QHeaderView
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QDate

# Assuming this is your custom database manager module
from src.lib.database import DatabaseManager

class RoundedButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #6A4B08; /* green*/
                border: none;
                color: white;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 15px;
                border-radius: 15px;
                width: 120px;
                height: 40px;
            }
            QPushButton:hover {
                background-color: #283FE8; /* Darker Green */
            }
            QPushButton:pressed {
                background-color: #0EC5FF; /* Green */
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class EnterLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.focusNextChild()
        else:
            super().keyPressEvent(event)

class CompanyForm(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Create Company Form')
        self.setGeometry(100, 100, 1000, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Set spacing between fields

        # Company details fields
        self.company_name_edit = EnterLineEdit(self)
        self.address_edit = EnterLineEdit(self)
        self.city_edit = EnterLineEdit(self)
        self.pincode_edit = EnterLineEdit(self)
        self.mobile_edit = EnterLineEdit(self)
        self.email_edit = EnterLineEdit(self)
        
        # Start month dropdown
        self.start_month_combo = QComboBox(self)
        self.start_month_combo.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

        # End month dropdown
        self.end_month_combo = QComboBox(self)
        self.end_month_combo.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

        # Start year dropdown
        self.start_year_combo = QComboBox(self)
        current_year = QDate.currentDate().year()
        self.start_year_combo.addItems([str(year) for year in range(current_year, current_year + 11)])

        # End year dropdown
        self.end_year_combo = QComboBox(self)
        self.end_year_combo.setDisabled(True)  # Disable editing

        layout.addWidget(QLabel('Company Name:'))
        layout.addWidget(self.company_name_edit)

        layout.addWidget(QLabel('Address:'))
        layout.addWidget(self.address_edit)

        layout.addWidget(QLabel('City:'))
        layout.addWidget(self.city_edit)

        layout.addWidget(QLabel('Pin Code:'))
        layout.addWidget(self.pincode_edit)

        layout.addWidget(QLabel('Mobile:'))
        layout.addWidget(self.mobile_edit)

        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email_edit)

        start_date_layout = QHBoxLayout()
        start_date_layout.addWidget(QLabel('Start Month:'))
        start_date_layout.addWidget(self.start_month_combo)

        start_date_layout.addWidget(QLabel('Start Year:'))
        start_date_layout.addWidget(self.start_year_combo)

        end_date_layout = QHBoxLayout()
        end_date_layout.addWidget(QLabel('End Month:'))
        end_date_layout.addWidget(self.end_month_combo)

        end_date_layout.addWidget(QLabel('End Year:'))
        end_date_layout.addWidget(self.end_year_combo)

        layout.addLayout(start_date_layout)
        layout.addLayout(end_date_layout)

        # OK and Cancel buttons
        buttons_layout = QHBoxLayout()
        ok_button = RoundedButton('OK', self)
        cancel_button = RoundedButton('Cancel', self)

        ok_button.clicked.connect(self.check_and_accept)
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        # Connect Enter key
        self.company_name_edit.returnPressed.connect(self.address_edit.setFocus)
        self.address_edit.returnPressed.connect(self.city_edit.setFocus)
        self.city_edit.returnPressed.connect(self.pincode_edit.setFocus)
        self.pincode_edit.returnPressed.connect(self.mobile_edit.setFocus)
        self.mobile_edit.returnPressed.connect(self.email_edit.setFocus)
        self.email_edit.returnPressed.connect(ok_button.click)

        # Connect start year combo box signal
        self.start_year_combo.currentIndexChanged.connect(self.update_end_year_options)

        # Initially update the end year options
        self.update_end_year_options()

    def update_end_year_options(self):
        start_year_index = self.start_year_combo.currentIndex()
        if start_year_index != -1:
            start_year = int(self.start_year_combo.currentText())
            self.end_year_combo.clear()
            self.end_year_combo.addItems([str(year) for year in range(start_year + 1, start_year + 12)])

    def check_and_accept(self):
        if self.company_name_edit.text().strip() == "":
            QMessageBox.warning(self, 'Warning', 'Please enter the company name.')
            self.company_name_edit.setFocus()
        else:
            self.accept()

class BasicWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Create a shortcut for Alt+C
        shortcut = QShortcut(QKeySequence("Alt+C"), self)
        shortcut.activated.connect(self.show_company_form)

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
        create_company_button = RoundedButton('Create Company', self)
        create_company_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        create_company_button.clicked.connect(self.show_company_form)
        
        create_company_layout.addWidget(create_company_button)

        # Add the "Create Company" layout to the main layout
        main_layout.addLayout(create_company_layout)

        # Create a table
        self.company_table = MyTableWidget(self)  # Use custom table widget
        main_layout.addWidget(self.company_table)

        # Set stretch factor to make the table columns responsive
        header = self.company_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set selection behavior to select entire rows
        self.company_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Fill the table with data
        self.populate_table()

        # Set the layout for the main window
        self.setLayout(main_layout)

    def populate_table(self):
        # Fetch data from the database
        company_data = self.db.select_company()
        print("Company data:", company_data)

        if company_data:
            num_rows = len(company_data)

            self.company_table.setRowCount(num_rows)
            self.company_table.setColumnCount(2)  # Fixed number of columns (Company Name, Financial Year)

            # Populate the table with sorted data
            for row_index, row_data in enumerate(company_data):
                company_name = row_data[1]
                start_month = row_data[7]
                start_year = row_data[8]
                end_month = row_data[9]
                end_year = row_data[10]

                # Construct the financial year string
                financial_year = f"{start_month} {start_year} - {end_month} {end_year}"

                item_company_name = QTableWidgetItem(company_name)
                item_company_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_company_name.setFlags(item_company_name.flags() & ~Qt.ItemFlag.ItemIsEditable)

                item_financial_year = QTableWidgetItem(financial_year)
                item_financial_year.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_financial_year.setFlags(item_financial_year.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.company_table.setItem(row_index, 0, item_company_name)
                self.company_table.setItem(row_index, 1, item_financial_year)

            # Set the labels for the table columns
            header_labels = ['Company Name', 'Financial Year']
            for col_index, label in enumerate(header_labels):
                header_item = QTableWidgetItem(label)
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                header_item.setFont(QFont('', -1, QFont.Weight.Bold))
                self.company_table.setHorizontalHeaderItem(col_index, header_item)

            # Set the size of the columns
            self.company_table.setColumnWidth(0, 200)  # Adjust the width as needed for Company Name
            self.company_table.setColumnWidth(1, 200)  # Adjust the width as needed for Financial Year

            # Set stretch factor to make the columns responsive
            self.company_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        else:
            # No data, clear the header labels
            self.company_table.clear()
            self.company_table.setHorizontalHeaderLabels([])


    def show_company_form(self):
        company_form = CompanyForm()
        result = company_form.exec()

        if result == QDialog.DialogCode.Accepted:
            # Retrieve values from the form
            company_name = company_form.company_name_edit.text().strip()
            address = company_form.address_edit.text().strip()
            city = company_form.city_edit.text().strip()
            pincode = company_form.pincode_edit.text().strip()
            mobile = company_form.mobile_edit.text().strip()
            email = company_form.email_edit.text().strip()
            start_month = company_form.start_month_combo.currentText()
            start_year = company_form.start_year_combo.currentText()
            end_month = company_form.end_month_combo.currentText()
            end_year = company_form.end_year_combo.currentText()

            if company_name:  
                # Add the company to the database
                self.db.insert_company(company_name, address, city, pincode, mobile, email, start_month, start_year, end_month, end_year)

                # Refresh the table with updated data
                self.populate_table()

                QMessageBox.information(self, 'Success', 'Company was created successfully.')

                # Process the form data as needed
                print(f'Company Name: {company_name}')
                print(f'Address: {address}')
                print(f'City: {city}')
                print(f'Pincode: {pincode}')
                print(f'Mobile: {mobile}')
                print(f'Email: {email}')
                print(f'Start Month: {start_month}')
                print(f'Start Year: {start_year}')
                print(f'End Month: {end_month}')
                print(f'End Year: {end_year}')
            else:
                # Company name is empty, keep the form open without closing it
                company_form.show()

class MyTableWidget(QTableWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            current_row = self.currentRow()
            if current_row != -1:  # Ensure a row is selected
                company_name = self.item(current_row, 0).text()  # Assuming company name is in the first column
                QMessageBox.information(self, 'Company Name', f'Selected Company: {company_name}')
        elif event.key() == Qt.Key.Key_Tab:
            current_row = self.currentRow()
            next_row = current_row + 1
            if next_row < self.rowCount():
                self.setCurrentCell(next_row, 0)
            else:
                self.setCurrentCell(0, 0)
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
