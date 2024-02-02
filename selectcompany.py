import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap

class BasicWindow(QWidget):
    def __init__(self):
        super().__init__()

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

        # Add the image
        logo_label = QLabel(self)
        logo_pixmap = QPixmap('./create2.png')  # Set the actual path to your logo
        logo_label.setPixmap(logo_pixmap.scaled(50, 50))  # Adjust the size as needed

        # Add the button and image to the horizontal layout
        image_button_layout.addWidget(small_button)
        image_button_layout.addWidget(logo_label)

        # Add the image and button layout to the main layout
        main_layout.addLayout(image_button_layout)

        # Create a table
        table = QTableWidget(self)
        table.setRowCount(5)  # Set the number of rows
        table.setColumnCount(3)  # Set the number of columns

        # Fill the table with dummy data
        for row in range(5):
            for col in range(3):
                item = QTableWidgetItem(f'Row {row}, Col {col}')
                table.setItem(row, col, item)

        # Set stretch factor to make the table columns responsive
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add the table to the main layout
        main_layout.addWidget(table)

        # Set the layout for the main window
        self.setLayout(main_layout)

def main():
    app = QApplication(sys.argv)
    basic_window = BasicWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
