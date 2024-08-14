import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QInputDialog, QFileDialog, QLabel, QHBoxLayout, QGridLayout, QScrollArea
from PySide6.QtGui import QPixmap
import linecache

class DynamicButtonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hell Porn Selector")
        self.setFixedSize(1200, 1000)
        self.image_paths = []

        self.layout_mini = QHBoxLayout()
        self.layout = QGridLayout()
        self.layout.addLayout(self.layout_mini, 0, 0)

        self.main_layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_widget = QWidget()
        self.image_widget.setLayout(self.layout)
        self.scroll_area.setWidget(self.image_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_new_button)


        self.main_layout.addWidget(self.create_button)

        # Load previously created buttons
        self.load_images()
        #self.load_buttons()

        self.setLayout(self.main_layout)

    def create_new_button(self):
        text, ok = QInputDialog.getText(self, "Enter Text", "Enter text for the new button:")
        if ok:
            new_button = QPushButton(text)
            test_button = QPushButton('Source')
            # Save the new button to a file
            self.save_button(text)

        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", os.getcwd())
        if folder_path:
            self.save_folder_path(folder_path)
            print(folder_path)

        img, image_path = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")

        if image_path:
            # Display the selected image within the container widget
            pixmap = QPixmap(img)
            pixmap = pixmap.scaledToHeight(500)
            image_label = QLabel()
            image_label.setPixmap(pixmap)

            new_button_layout = QHBoxLayout()
            new_button_widget = QWidget()

            new_button_layout.addWidget(new_button)
            new_button_layout.addWidget(test_button)
            new_button_widget.setLayout(new_button_layout)


            row = len(self.image_paths) // 3
            col = len(self.image_paths) % 3

            if row <= 0:
                self.layout.addWidget(image_label, row, col)
                self.layout.addWidget(new_button_widget,  (row + 1), col)
            else:
                self.layout.addWidget(image_label, (row + 1), col)
                self.layout.addWidget(new_button_widget,  (row + 2), col)

            print(row)

            self.image_paths.append(image_path)

            self.save_image(img)



    def save_image(self, img):
        if not os.path.exists("image.txt"):
            with open("image.txt", "w") as t:
                t.write(img)
        else:
            with open("image.txt", "a") as t:
                t.write("\n" + img)

    def save_folder_path(self, fld):
        if not os.path.exists("folder.txt"):
            with open("folder.txt", "w") as f:
                f.write(fld)
        else:
            with open("folder.txt", "a") as f:
                f.write("\n" + fld)

    def save_button(self, text):
        if not os.path.exists("buttons.txt"):
            with open("buttons.txt", "w") as f:
                f.write(text)
        else:
            with open("buttons.txt", "a") as f:
                f.write("\n" + text)

    def load_images(self):
        if os.path.exists("image.txt"):
            with open("image.txt", "r") as t:
                lines = t.readlines()
                num_lines = len(lines)
                print(num_lines)

                x = 0
                y = 1

                image_file = "image.txt"
                button_file = "buttons.txt"
                folder_file = "folder.txt"

                while x < num_lines:

                    specific_image_line = linecache.getline(image_file, y)
                    specific_image_text = specific_image_line.strip()

                    specific_button_line = linecache.getline(button_file, y)
                    specific_button_text = specific_button_line.strip()

                    specific_folder_line = linecache.getline(folder_file, y)
                    specific_folder_text = specific_folder_line.strip()

                    print(specific_folder_text)

                    pixmap = QPixmap(specific_image_text)
                    pixmap = pixmap.scaledToHeight(500)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)

                    new_button = QPushButton(specific_button_text)
                    test_button = QPushButton('Source')
                    test_button.clicked.connect(lambda checked, path=specific_folder_text: self.open_folder(path))


                    new_button_layout = QHBoxLayout()
                    new_button_widget = QWidget()

                    new_button_layout.addWidget(new_button)
                    new_button_layout.addWidget(test_button)
                    new_button_widget.setLayout(new_button_layout)

                    row = x // 3
                    col = x % 3

                    if row <= 0:
                        self.layout.addWidget(image_label, row, col)
                        self.layout.addWidget(new_button_widget, (row + 1), col)
                    else:
                        if row <= 1:
                            self.layout.addWidget(image_label, (row + 1), col)
                            self.layout.addWidget(new_button_widget, (row + 2), col)
                        else:
                            self.layout.addWidget(image_label, (row * row), col)
                            self.layout.addWidget(new_button_widget, (row * row + 1), col)

                    x = x + 1
                    y = y + 1

    def open_folder(self, folder_path):
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print('folder does not exist')




"""
    def load_images(self):
        if os.path.exists("image.txt"):
            with open("image.txt", "r") as t:
                for line in t:
                    image_text = line.strip()
                    new_image_map = QPixmap(image_text)
                    new_image_map = new_image_map.scaledToHeight(500)
                    new_image = QLabel()
                    new_image.setPixmap(new_image_map)
                    self.layout.addWidget(new_image)
                    print(line)

    def load_buttons(self):
        if os.path.exists("buttons.txt"):
            with open("buttons.txt", "r") as f:
                for line in f:
                    button_text = line.strip()
                    new_button = QPushButton(button_text)
                    self.layout.addWidget(new_button)
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DynamicButtonApp()
    window.show()
    sys.exit(app.exec())