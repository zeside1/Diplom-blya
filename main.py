import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PIL import Image, ImageFilter, ImageOps


class PhotoEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фоторедактор")
        self.setWindowState(Qt.WindowMaximized)

        self.original_image = None
        self.filtered_image = None

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        select_button = QPushButton("Выбрать фото", self)
        select_button.clicked.connect(self.select_photo)

        blur_button = QPushButton("Размытие", self)
        blur_button.clicked.connect(self.apply_blur_filter)

        grayscale_button = QPushButton("Черно-белое", self)
        grayscale_button.clicked.connect(self.apply_grayscale_filter)

        negative_button = QPushButton("Негатив", self)
        negative_button.clicked.connect(self.apply_negative_filter)

        rotate_button = QPushButton("Поворот", self)
        rotate_button.clicked.connect(self.apply_rotate_filter)

        undo_button = QPushButton("Отменить фильтр", self)
        undo_button.clicked.connect(self.confirm_undo_filter)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.setGeometry(20, 500, 100, 30)
        self.save_button.clicked.connect(self.save_image)

        button_layout = QHBoxLayout()
        button_layout.addWidget(select_button)
        button_layout.addWidget(blur_button)
        button_layout.addWidget(grayscale_button)
        button_layout.addWidget(negative_button)
        button_layout.addWidget(rotate_button)
        button_layout.addWidget(undo_button)
        button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.image_label)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def select_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Image Files (*.jpg *.jpeg *.png)")

        if file_path:
            self.original_image = Image.open(file_path)
            self.filtered_image = self.original_image.copy()
            self.display_image(self.original_image)

    def apply_blur_filter(self):
        if self.filtered_image:
            self.filtered_image = self.filtered_image.filter(ImageFilter.BLUR)
            self.display_image(self.filtered_image)

    def apply_grayscale_filter(self):
        if self.filtered_image:
            self.filtered_image = self.filtered_image.convert("L")
            self.display_image(self.filtered_image)

    def apply_negative_filter(self):
        if self.filtered_image:
            self.filtered_image = ImageOps.invert(self.filtered_image)
            self.display_image(self.filtered_image)

    def apply_rotate_filter(self):
        if self.filtered_image:
            self.filtered_image = self.filtered_image.rotate(90)
            self.display_image(self.filtered_image)

    def confirm_undo_filter(self):
        if self.original_image:
            confirmation = QMessageBox.question(self, "Подтверждение", "Вы точно уверены, что хотите отменить фильтр?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.undo_filter()

    def undo_filter(self):
        if self.original_image:
            self.display_image(self.original_image)
            self.filtered_image = self.original_image.copy()

    def save_image(self):
        save_path = "отредактированное"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        image_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", save_path, "JPEG (*.jpg)")
        if image_path:
            self.filtered_image.save(image_path, "JPEG")
            QMessageBox.information(self, "Успешно", "Изображение сохранено.")

    def display_image(self, image):
        image = image.convert("RGBA")
        image = image.resize((self.width() - 20, self.height() - 150))
        qimage = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorWindow()
    window.show()
    sys.exit(app.exec_())