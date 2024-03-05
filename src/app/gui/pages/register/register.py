from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QGroupBox, QStackedWidget, QMessageBox
from PyQt6.QtCore import Qt
from src.lib.database import DatabaseManager  # Import your DatabaseManager class
#from src.app.gui.pages.login.login import LoginForm  # Import your LoginForm class

class RegistrationForm(QWidget):
    def __init__(self, stack_widget, db):
        super().__init__()

        self.stack_widget = stack_widget
        self.db = db

        self.init_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            # Jump back to the company page
            self.stack_widget.setCurrentIndex(0)  # Assuming index 0 is your company page
        else:
            super().keyPressEvent(event)    

    def init_ui(self):
        layout = QFormLayout()

        # Registration Page Widgets
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addRow(username_label, self.username_input)

        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(password_label, self.password_input)

        confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow(confirm_password_label, self.confirm_password_input)

        # Increase the vertical spacing between rows
        layout.setVerticalSpacing(70)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.on_register_clicked)
        register_button.setStyleSheet("background-color: blue; color: white;")
        layout.addRow(register_button)

        group_box = QGroupBox("Registration")
        group_box.setLayout(layout)
        group_box.setFixedWidth(600)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group_box, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the widget
        self.setStyleSheet("background-color: #D9D9D9;")  # Set the background color

    def on_register_clicked(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = 'admin'  # or whatever default role you want to assign
        compid = 1  # Assuming compid 1 for now, you might need to fetch it from your UI

        # Check if passwords match and username is not empty
        if password == self.confirm_password_input.text() and username:
            # Check if user is already registered in the company
            if self.db.check_user_in_company(username, compid):
                QMessageBox.warning(None, "Registration Failed", "User is already registered in the company.")
            else:
                # Perform registration in the database
                if self.db.register_user(username, password, role, compid):
                    print("Registration successful!")
                    # Show a success popup
                    QMessageBox.information(None, "Registration Success", "User registered successfully!")
                    # Switch to the login page after registration
                    login_form = LoginForm(self.stack_widget, self.db)
                    self.stack_widget.addWidget(login_form)
                    self.stack_widget.setCurrentWidget(login_form)
                else:
                    print("Registration failed. Username might already exist.")
        else:
            print("Invalid username or passwords do not match!")
