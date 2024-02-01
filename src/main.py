import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QStackedWidget
from PyQt6.QtGui import QIcon


from app.gui.pages.login.login import LoginForm
from app.gui.pages.register.register import RegistrationForm
from app.gui.pages.dashboard.dashboard import DashboardPage
from lib.database import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()

        self.setWindowTitle('OKLABS Account Software 1.0.0')
        icon = QIcon("./src/assets/icon.png")
        self.setWindowIcon(icon)
        self.setStyleSheet("background-color: #A4BFD8;")

        self.stacked_widget = QStackedWidget(self)
        self.init_ui()

    def init_ui(self):
        if not self.db.checkIfAdminRegister():
            registration_form = RegistrationForm(self.stacked_widget, self.db)
            self.stacked_widget.addWidget(registration_form)
            self.stacked_widget.setCurrentWidget(registration_form)
            print('Show The Registration Form')
        else:
            login_page = LoginForm(self.stacked_widget, self.db)
            self.stacked_widget.addWidget(login_page)
            self.stacked_widget.setCurrentWidget(login_page)
            print('Show The Login Form')

        self.setCentralWidget(self.stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.showMaximized()
    sys.exit(app.exec())