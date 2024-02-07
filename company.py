import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox, QAbstractItemView, QHeaderView
from PyQt6.QtGui import QFont, QColor, QKeyEvent,QKeySequence,QShortcut
from PyQt6.QtCore import Qt

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

        layout = QFormLayout(self)

        # Company details fields
        self.company_name_edit = EnterLineEdit(self)
        self.address_edit = EnterLineEdit(self)
        self.city_edit = EnterLineEdit(self)
        self.pincode_edit = EnterLineEdit(self)
        self.mobile_edit = EnterLineEdit(self)
        self.email_edit = EnterLineEdit(self)
        
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
        ok_button = RoundedButton('OK', self)
        cancel_button = RoundedButton('Cancel', self)

        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addRow(buttons_layout)

        # Connect Enter key
        self.company_name_edit.returnPressed.connect(self.address_edit.setFocus)
        self.address_edit.returnPressed.connect(self.city_edit.setFocus)
        self.city_edit.returnPressed.connect(self.pincode_edit.setFocus)
        self.pincode_edit.returnPressed.connect(self.mobile_edit.setFocus)
        self.mobile_edit.returnPressed.connect(self.email_edit.setFocus)
        self.email_edit.returnPressed.connect(ok_button.click)

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
        self.company_table = QTableWidget(self)  # Use custom table widget
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

            # Populate the table with data
            for row_index, row_data in enumerate(company_data):
                for col_index, col_value in enumerate(row_data[1:]):  # Exclude ID column
                    item = QTableWidgetItem(str(col_value))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.company_table.setItem(row_index, col_index, item)

            # Add labels at the top of the table
            header_labels = ['Company Name', 'Financial Year']  # Updated header_labels
            for col_index, label in enumerate(header_labels):
                header_item = QTableWidgetItem(label)
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align the text
                header_item.setFont(QFont('', -1, QFont.Weight.Bold))  # Make the label bold
                self.company_table.setHorizontalHeaderItem(col_index, header_item)

            # Set the size of the columns
            self.company_table.setColumnWidth(0, 120)  # Adjust the width as needed for Company Name
            self.company_table.setColumnWidth(1, 80)  # Adjust the width as needed for Financial Year

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

def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
