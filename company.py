import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QFormLayout, QLineEdit, QComboBox, QLabel, QMessageBox, QAbstractItemView, QHeaderView
from PyQt6.QtGui import QFont, QColor, QKeyEvent, QKeySequence, QShortcut
from PyQt6.QtCore import Qt ,QDate

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
        self.end_year_combo.addItems([str(year) for year in range(current_year, current_year + 11)])

        layout.addRow('Company Name:', self.company_name_edit)
        layout.addRow('Address:', self.address_edit)
        layout.addRow('City:', self.city_edit)
        layout.addRow('Pin Code:', self.pincode_edit)
        layout.addRow('Mobile:', self.mobile_edit)
        layout.addRow('Email:', self.email_edit)
        layout.addRow('Start Month:', self.start_month_combo)
        layout.addRow('Start Year:', self.start_year_combo)
        layout.addRow('End Month:', self.end_month_combo)
        layout.addRow('End Year:', self.end_year_combo)

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
            # Sort company data by company name (assuming the company name is in the first column)
            sorted_company_data = sorted(company_data, key=lambda x: x[1])

            num_rows = len(sorted_company_data)

            self.company_table.setRowCount(num_rows)
            self.company_table.setColumnCount(2)  # Fixed number of columns (Company Name, Financial Year)

            # Populate the table with sorted data
            for row_index, row_data in enumerate(sorted_company_data):
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
            company_name = company_form.company_name_edit.text().strip()  # Remove leading/trailing whitespace
            start_month = company_form.start_month_combo.currentText()
            start_year = company_form.start_year_combo.currentText()
            end_month = company_form.end_month_combo.currentText()
            end_year = company_form.end_year_combo.currentText()

            if company_name:  # Check if company name is not empty
                # Add the company to the database
                self.db.insert_company(company_name, f"{start_month} {start_year}", f"{end_month} {end_year}")

                # Refresh the table with updated data
                self.populate_table()

                QMessageBox.information(self, 'Success', 'Company was created successfully.')

                # Process the form data as needed
                print(f'Company Name: {company_name}')
                print(f'Start Month: {start_month}')
                print(f'Start Year: {start_year}')
                print(f'End Month: {end_month}')
                print(f'End Year: {end_year}')
            else:
                QMessageBox.warning(self, 'Error', 'Please enter a company name.')


class MyTableWidget(QTableWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            selected_row = self.currentRow()
            if selected_row >= 0:
                item = self.item(selected_row, 0)
                company_name = item.text()
                QMessageBox.information(self, 'Company Name', f'The selected company is: {company_name}')
        elif event.key() == Qt.Key.Key_Tab:
            # Move to the next row
            current_row = self.currentRow()
            next_row = current_row + 1
            if next_row < self.rowCount():
                self.setCurrentCell(next_row, 0)
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()