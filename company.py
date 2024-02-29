import sys
import pyttsx3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QLineEdit, QComboBox, QLabel, QMessageBox, QAbstractItemView, QHeaderView, QStackedWidget
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QIntValidator
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import threading


# Assuming this is your custom database manager module
from src.lib.database import DatabaseManager
from src.app.gui.pages.register.register import RegistrationForm
from country import countries_and_states

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
        self.setGeometry(100, 100, 1100, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Set spacing between fields

        # Company details fields
        self.company_name_edit = EnterLineEdit(self)
        self.company_name_edit.setFont(QFont('Comic Sans MS', 12))  # Set font size for company name input and shorten the length
        self.address_edit = EnterLineEdit(self)
        self.city_edit = EnterLineEdit(self)
        
        # Pincode edit field
        self.pincode_edit = EnterLineEdit(self)
        self.pincode_edit.setValidator(QIntValidator())  # Allow only integer input

        # Mobile edit field
        self.mobile_edit = EnterLineEdit(self)
        self.mobile_edit.setValidator(QIntValidator())  # Allow only integer input

        self.email_edit = EnterLineEdit(self)
        
        # Country dropdown
        self.country_combo = QComboBox(self)
        self.country_combo.setFont(QFont('Comic Sans MS', 14))  # Set font size for country dropdown
        # Populate country dropdown with sample data (replace with actual country data)
        self.country_combo.addItems(list(countries_and_states.keys()))
        # Connect the country dropdown to update the state dropdown
        self.country_combo.currentIndexChanged.connect(self.update_state_combo)

        # State dropdown
        self.state_combo = QComboBox(self)
        self.state_combo.setFont(QFont('Comic Sans MS', 14))  # Set font size for state dropdown

        # Start month dropdown
        self.start_month_combo = QComboBox(self)
        self.start_month_combo.setFont(QFont('Verdana', 12))  # Set font size for start month dropdown
        self.start_month_combo.addItems(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

        # End month dropdown
        self.end_month_combo = QComboBox(self)
        self.end_month_combo.setFont(QFont('Verdana', 12))  # Set font size for end month dropdown

        # Start year dropdown
        self.start_year_combo = QComboBox(self)
        self.start_year_combo.setFont(QFont('Times New Roman', 12))  # Set font size for start year dropdown
        current_year = QDate.currentDate().year()
        years_list = [str(year) for year in range(2015, current_year + 1)]  # Update the range to include years from 2015 to the current year
        self.start_year_combo.addItems(years_list)

        # Set the default index to the current year
        default_year_index = years_list.index(str(current_year))
        if default_year_index >= 0:
            self.start_year_combo.setCurrentIndex(default_year_index)

        # End year dropdown
        self.end_year_combo = QComboBox(self)
        self.end_year_combo.setFont(QFont('Times New Roman', 12))  # Set font size for end year dropdown

        # Set default country to India
        default_country_index = self.country_combo.findText("India")
        if default_country_index >= 0:
            self.country_combo.setCurrentIndex(default_country_index)

        # Company details layout
        company_details_layout = QHBoxLayout()
        company_details_layout.addWidget(QLabel('Company Name:'))
        company_details_layout.addWidget(self.company_name_edit)
        company_details_layout.addWidget(QLabel('Country:'))
        company_details_layout.addWidget(self.country_combo)
        company_details_layout.addWidget(QLabel('State:'))
        company_details_layout.addWidget(self.state_combo)

        # Address layout
        address_layout = QHBoxLayout()
        address_layout.addWidget(QLabel('Address:'))
        address_layout.addWidget(self.address_edit)

        # City, Pincode, Mobile, Email layout
        city_pincode_layout = QHBoxLayout()
        city_pincode_layout.addWidget(QLabel('City:'))
        city_pincode_layout.addWidget(self.city_edit)
        city_pincode_layout.addWidget(QLabel('Pin Code/Zip Code:'))
        city_pincode_layout.addWidget(self.pincode_edit)
        city_pincode_layout.addWidget(QLabel('Mobile:'))
        city_pincode_layout.addWidget(self.mobile_edit)
        city_pincode_layout.addWidget(QLabel('Email:'))
        city_pincode_layout.addWidget(self.email_edit)

        # Date layout
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel('Start Month:'))
        date_layout.addWidget(self.start_month_combo)
        date_layout.addWidget(QLabel('Start Year:'))
        date_layout.addWidget(self.start_year_combo)
        date_layout.addWidget(QLabel('End Month:'))
        date_layout.addWidget(self.end_month_combo)
        date_layout.addWidget(QLabel('End Year:'))
        date_layout.addWidget(self.end_year_combo)

        # Add layouts to main layout
        layout.addLayout(company_details_layout)
        layout.addLayout(address_layout)
        layout.addLayout(city_pincode_layout)
        layout.addLayout(date_layout)

        # OK and Cancel buttons
        buttons_layout = QHBoxLayout()
        ok_button = RoundedButton('OK', self)
        cancel_button = RoundedButton('Cancel', self)

        ok_button.clicked.connect(self.check_and_accept)
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(buttons_layout)

        # Set tab order
        self.setTabOrder(self.company_name_edit, self.country_combo)
        self.setTabOrder(self.country_combo, self.state_combo)
        self.setTabOrder(self.state_combo, self.address_edit)
        self.setTabOrder(self.address_edit, self.city_edit)
        self.setTabOrder(self.city_edit, self.pincode_edit)
        self.setTabOrder(self.pincode_edit, self.mobile_edit)
        self.setTabOrder(self.mobile_edit, self.email_edit)
        self.setTabOrder(self.email_edit, self.start_year_combo)
        self.setTabOrder(self.start_year_combo, self.start_month_combo)
        self.setTabOrder(self.start_month_combo, self.end_year_combo)
        self.setTabOrder(self.end_year_combo, self.end_month_combo)

        # Connect Enter key
        self.company_name_edit.returnPressed.connect(lambda: self.country_combo.setFocus(Qt.FocusReason.MouseFocusReason))  # Set focus to the country dropdown
        self.country_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Allow tabbing to country dropdown
        self.country_combo.currentIndexChanged.connect(self.update_state_combo)  # Update state dropdown based on selected country
        self.state_combo.currentIndexChanged.connect(lambda: self.address_edit.setFocus(Qt.FocusReason.MouseFocusReason))   # Set focus to the address field
        self.address_edit.returnPressed.connect(lambda: self.country_combo.setFocus(Qt.FocusReason.MouseFocusReason))  # Set focus to the country dropdown

        # Connect start year combo box signal
        self.start_year_combo.currentIndexChanged.connect(self.update_end_year_options)

        # Initially update the end year options
        self.update_end_year_options()

        # Connect country combo box signal
        self.country_combo.currentIndexChanged.connect(self.update_end_month_combo)

        # Initially update the end month options
        self.update_end_month_combo()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.focusNextChild()
        else:
            super().keyPressEvent(event) 

    def update_end_year_options(self):
        start_year_index = self.start_year_combo.currentIndex()
        if start_year_index != -1:
            start_year = int(self.start_year_combo.currentText())
            self.end_year_combo.clear()
            self.end_year_combo.addItems([str(year) for year in range(start_year + 1, start_year + 12)])

    def update_state_combo(self, index):
        selected_country = self.country_combo.currentText()
        if selected_country in countries_and_states:
            # Update state dropdown based on selected country
            self.state_combo.clear()
            self.state_combo.addItems([state.capitalize() for state in countries_and_states[selected_country]["states"]])
            
            # Update start and end months based on selected country's fiscal year
            fyear = countries_and_states[selected_country]["fyear"]
            self.start_month_combo.setCurrentIndex(self.start_month_combo.findText(fyear["start"]))
            self.end_month_combo.setCurrentIndex(self.end_month_combo.findText(fyear["end"]))

    def update_end_month_combo(self):
        selected_country = self.country_combo.currentText()

        # Clear existing items in the end month combo box
        self.end_month_combo.clear()

        if selected_country in countries_and_states:
            fyear = countries_and_states[selected_country]["fyear"]
            start_month = fyear["start"]
            end_month = fyear["end"]

            # Set the start month combo box to the start month of the fiscal year
            self.start_month_combo.setCurrentIndex(self.start_month_combo.findText(start_month))

            # Add end months based on the fiscal year
            months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            start_index = months.index(end_month)
            self.end_month_combo.addItems(months[start_index:] + months[:start_index])

            # Set the default end month to the first item in the combo box
            self.end_month_combo.setCurrentIndex(0)

    def check_and_accept(self):
        company_name = self.company_name_edit.text().strip()
        if company_name == "":
            self.show_warning('Please enter the company name.')
            self.company_name_edit.setFocus()
        else:
            # Check if the company name already exists in the database
            db = DatabaseManager()
            existing_company = db.select_company_by_name(company_name)
            if existing_company:
                self.show_warning('Company name already exists.', 'Warning')
                reply = QMessageBox.warning(self, 'Warning', 'Company name already exists.', QMessageBox.StandardButton.Ok)
                if reply == QMessageBox.StandardButton.Ok:
                    self.company_name_edit.setFocus()
            else:
                # Company name does not exist, accept the form
                self.accept()

    def show_warning(self, message, title='Warning'):
        QMessageBox.warning(self, title, message)   

class MyTableWidget(QTableWidget):
    registrationFormOpened = pyqtSignal(bool)

    def __init__(self, stack_widget, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stack_widget = stack_widget
        self.db = db

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.doubleClicked.connect(self.open_registration_form)  # Connect double click event to open the registration form

    def open_registration_form(self):
        current_row = self.currentRow()
        if current_row != -1:  # Ensure a row is selected
            # Emit signal to notify the form opening
            self.registrationFormOpened.emit(True)

            # Show the registration form
            registration_form = RegistrationForm(self.stack_widget, self.db)
            self.stack_widget.addWidget(registration_form)
            self.stack_widget.setCurrentWidget(registration_form)


    def keyPressEvent(self, event):
        if event.text().isalpha():
            key = event.text().upper()
            current_row = self.currentRow()
            current_col = self.currentColumn()
            num_rows = self.rowCount()
            for row in range(current_row + 1, num_rows):
                item = self.item(row, current_col)
                if item and item.text().upper().startswith(key):
                    self.setCurrentCell(row, current_col)
                    return
            for row in range(num_rows):
                item = self.item(row, current_col)
                if item and item.text().upper().startswith(key):
                    self.setCurrentCell(row, current_col)
                    return
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            current_row = self.currentRow()
            if current_row != -1:  # Ensure a row is selected
                company_name = self.item(current_row, 0).text()  # Assuming company name is in the first column
                self.open_registration_form(company_name)  # Call the method to open the register page
        elif event.key() == Qt.Key.Key_Tab:
            current_row = self.currentRow()
            next_row = current_row + 1
            if next_row < self.rowCount():
                self.setCurrentCell(next_row, 0)
            else:
                self.setCurrentCell(0, 0)
        else:
            super().keyPressEvent(event)

    def open_registration_form(self, company_name):
        # Emit signal to notify the form opening
        self.registrationFormOpened.emit(True)

        # Show the registration form
        registration_form = RegistrationForm(self.stack_widget, self.db)
        self.stack_widget.addWidget(registration_form)
        self.stack_widget.setCurrentWidget(registration_form)

class PermanentRegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()        

class BasicWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Create a stack widget to manage multiple pages
        self.stack_widget = QStackedWidget()  # Initialize the stack widget
        self.db = DatabaseManager()
        self.init_ui()
        self.create_shortcuts()

        # Connect signal of stack widget's current changed to a slot
        self.stack_widget.currentChanged.connect(self.handle_page_change)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            reply = QMessageBox.question(self, 'Close Application', 'Do you want to close the application?',
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                QApplication.quit()
            elif reply == QMessageBox.StandardButton.No:
                pass
        elif event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.focusNextChild()
        else:
            super().keyPressEvent(event)

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle('Accounting Software')
        self.showMaximized()

        # Create a layout for the entire window
        main_layout = QVBoxLayout(self)

        # Create a horizontal layout for the "Create Company" button
        create_company_layout = QVBoxLayout()

        # Add the create company button
        self.create_company_button = QLabel('<html><head/><body><p><span style="color:red; text-decoration: underline;">C</span>reate Company</p></body></html>', self)
        self.create_company_button.setFont(QFont('Comic Sans MS', 18))
        self.create_company_button.setStyleSheet("color: black;")
        self.create_company_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.create_company_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_company_button.mousePressEvent = self.show_company_form

        create_company_layout.addWidget(self.create_company_button)

        # Add the "Create Company" layout to the main layout
        main_layout.addLayout(create_company_layout)

        # Add the stack widget to the main layout
        main_layout.addWidget(self.stack_widget)

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Initialize the table widget
        self.init_table_widget()

    def handle_page_change(self, index):
        # Get the current widget from the stack widget
        current_widget = self.stack_widget.widget(index)
        # Check if the current widget is the register page
        if isinstance(current_widget, RegistrationForm):
            self.create_company_button.setVisible(False)
        else:
            self.create_company_button.setVisible(True)

    def create_shortcuts(self):
        # Create shortcut to open create company form
        create_company_shortcut = QShortcut(QKeySequence("Alt+C"), self)
        create_company_shortcut.activated.connect(self.show_company_form)

    def init_table_widget(self):
        # Create the table widget
        self.company_table = MyTableWidget(self.stack_widget, self.db)
        self.company_table.registrationFormOpened.connect(self.hide_create_company_button)
        self.populate_table()

        # Add the table widget to the stack widget
        self.stack_widget.addWidget(self.company_table)

    def hide_create_company_button(self, opened):
        if opened:
            self.create_company_button.hide()

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
                item_company_name.setFont(QFont('Comic Sans MS', 12,QFont.Weight.Bold))
                item_company_name.setFlags(item_company_name.flags() & ~Qt.ItemFlag.ItemIsEditable)

                item_financial_year = QTableWidgetItem(financial_year)
                item_financial_year.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item_financial_year.setFont(QFont('Comic Sans MS', 12,QFont.Weight.Bold))
                item_financial_year.setFlags(item_financial_year.flags() & ~Qt.ItemFlag.ItemIsEditable)

                self.company_table.setItem(row_index, 0, item_company_name)
                self.company_table.setItem(row_index, 1, item_financial_year)

            # Set the labels for the table columns
            header_labels = ['Company Name', 'Financial Year']
            for col_index, label in enumerate(header_labels):
                header_item = QTableWidgetItem(label)
                header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                header_item.setFont(QFont('', 15, QFont.Weight.Bold))
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


    def show_company_form(self, event=None):  # Fix method signature here
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

            # Add the company to the database
            self.db.insert_company(company_name, address, city, pincode, mobile, email, start_month, start_year, end_month, end_year)

            # Refresh the table with updated data
            self.populate_table()

            QMessageBox.information(self, 'Success', 'Company was created successfully.')

def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
