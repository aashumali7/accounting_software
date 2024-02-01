from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QDialog
from PyQt6.QtGui import QPixmap

class CustomPopup(QDialog):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Popup")
        self.setMinimumSize(400, 300)  # Adjust the size accordingly

        # Add widgets and layout for the custom popup
        # You can customize this part based on your needs
        layout = QVBoxLayout(self)

        label = QLabel(content)
        layout.addWidget(label)

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

        # Create a horizontal layout for the LandingPage
        main_layout = QHBoxLayout(self)

        # Set layout margins and spacing to 0
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add a white section (80% width, 100% height)
        white_section = QWidget(self)
        white_section.setObjectName("white_section")
        white_section.setStyleSheet("background-color: white;")

        # Set layout margins and spacing to 0
        white_layout = QVBoxLayout(white_section)
        white_layout.setContentsMargins(0, 0, 0, 0)
        white_layout.setSpacing(5)

        # Add logo centered in the white area
        logo_label = QLabel()
        logo_path = "src/assets/unnamed.png"
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap.scaled(200, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

        white_layout.addWidget(logo_label)

        white_label = QLabel("Welcome to the Landing Page (White Section)")
        white_layout.addWidget(white_label)
        white_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(white_section, 8)  # Set the white section to take 80% of the available width

        # Add a blue section (20%)
        blue_section = QWidget(self)
        blue_section.setStyleSheet("background-color: #B7F7EF;")

        # Set layout margins and reduced spacing to 0
        blue_layout = QVBoxLayout(blue_section)
        blue_layout.setContentsMargins(0, 0, 0, 0)
        blue_layout.setSpacing(25)  # Adjusted spacing

        # Align the layout to the top
        blue_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Move language dropdown to the place of "Additional Information" label
        language_dropdown = QComboBox()
        language_dropdown.addItem("English")
        language_dropdown.addItem("Spanish")
        language_dropdown.addItem("French")
        blue_layout.addWidget(language_dropdown)

        # Create buttons for each menu item
        button_customers = QPushButton("Customers")
        button_suppliers = QPushButton("Suppliers")
        button_items = QPushButton("Items")
        button_sale_register = QPushButton("Sale Register")

        # Set button styles
        button_styles = """
            QPushButton {
                background-color: none;
                color: black;
                border: black;
                font-weight: bold;
            }
        """

        button_hover_style = """
            QPushButton:hover {
                cursor: pointinghand;
            }
        """

        button_customers.setStyleSheet(button_styles + button_hover_style)
        button_suppliers.setStyleSheet(button_styles + button_hover_style)
        button_items.setStyleSheet(button_styles + button_hover_style)
        button_sale_register.setStyleSheet(button_styles + button_hover_style)

        # Set cursor for buttons
        button_customers.setCursor(Qt.CursorShape.PointingHandCursor)
        button_suppliers.setCursor(Qt.CursorShape.PointingHandCursor)
        button_items.setCursor(Qt.CursorShape.PointingHandCursor)
        button_sale_register.setCursor(Qt.CursorShape.PointingHandCursor)

        # Connect each button to the show_custom_popup method with a specific argument
        button_customers.clicked.connect(lambda: self.show_custom_popup("Customers Details"))
        button_suppliers.clicked.connect(lambda: self.show_custom_popup("Suppliers Details"))
        button_items.clicked.connect(lambda: self.show_custom_popup("Items Details"))
        button_sale_register.clicked.connect(lambda: self.show_custom_popup("Sale Register Details"))

        # Add buttons to the layout without any spacing
        blue_layout.addWidget(button_customers, alignment=Qt.AlignmentFlag.AlignTop)
        blue_layout.addWidget(button_suppliers, alignment=Qt.AlignmentFlag.AlignTop)
        blue_layout.addWidget(button_items, alignment=Qt.AlignmentFlag.AlignTop)
        blue_layout.addWidget(button_sale_register, alignment=Qt.AlignmentFlag.AlignTop)

        main_layout.addWidget(blue_section, 1)  # Set the blue section to take 20% of the available width

        # Set the layout for the main widget
        self.setLayout(main_layout)

    def show_custom_popup(self, content):
        # Create an instance of the CustomPopup with the specified content
        custom_popup = CustomPopup(content, self)

        # Set the white section as the parent for the popup
        white_section = self.findChild(QWidget, "white_section")
        custom_popup.setParent(white_section)

        # Show the custom popup
        custom_popup.exec()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DashboardPage()
    window.show()
    sys.exit(app.exec())
