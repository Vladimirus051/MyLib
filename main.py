import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QFileDialog,
                             QHeaderView)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import sqlite3
import subprocess


class BookApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.loadBooks()

    def initUI(self):
        self.setWindowTitle('Library App')
        self.setGeometry(100, 100, 1000, 700)

        layout = QVBoxLayout()

        form_layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Название книги')
        form_layout.addWidget(QLabel('Название книги:'))
        form_layout.addWidget(self.name_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText('Автор')
        form_layout.addWidget(QLabel('Автор:'))
        form_layout.addWidget(self.author_input)

        self.genre_input = QLineEdit(self)
        self.genre_input.setPlaceholderText('Жанр')
        form_layout.addWidget(QLabel('Жанр:'))
        form_layout.addWidget(self.genre_input)

        self.rating_input = QLineEdit(self)
        self.rating_input.setPlaceholderText('Рейтинг')
        form_layout.addWidget(QLabel('Рейтинг:'))
        form_layout.addWidget(self.rating_input)

        self.status_input = QLineEdit(self)
        self.status_input.setPlaceholderText('Статус')
        form_layout.addWidget(QLabel('Статус:'))
        form_layout.addWidget(self.status_input)

        self.pdf_path_input = QLineEdit(self)
        self.pdf_path_input.setPlaceholderText('Путь к PDF')
        self.pdf_path_input.setReadOnly(True)
        form_layout.addWidget(QLabel('PDF файл:'))
        form_layout.addWidget(self.pdf_path_input)

        self.upload_pdf_btn = QPushButton('Загрузить PDF', self)
        self.upload_pdf_btn.clicked.connect(self.uploadPDF)
        form_layout.addWidget(self.upload_pdf_btn)

        self.submit_btn = QPushButton('Добавить книгу', self)
        self.submit_btn.clicked.connect(self.addBook)
        form_layout.addWidget(self.submit_btn)

        layout.addLayout(form_layout)

        self.table = QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Автор', 'Жанр', 'Рейтинг', 'Статус', 'PDF файл', 'Открыть', 'Удалить'])
        self.table.cellClicked.connect(self.cellClicked)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def uploadPDF(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить PDF файл", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.pdf_path_input.setText(file_path)

    def loadBooks(self):
        conn = sqlite3.connect('my_lib.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
            view_btn = QPushButton('Открыть')
            view_btn.clicked.connect(self.viewBook)
            self.table.setCellWidget(i, 7, view_btn)

            delete_btn = QPushButton('Удалить')
            delete_btn.clicked.connect(self.deleteBook)
            self.table.setCellWidget(i, 8, delete_btn)

    def addBook(self):
        name = self.name_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        rating = self.rating_input.text()
        status = self.status_input.text()
        pdf_path = self.pdf_path_input.text()

        if not all([name, author, genre, rating, status, pdf_path]):
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля!')
            return

        conn = sqlite3.connect('my_lib.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (name, author, genre, rating, status, pdf_path) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, author, genre, rating, status, pdf_path))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Успех', 'Книга добавлена!')
        self.clearInputs()
        self.loadBooks()

    def deleteBook(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        book_id = self.table.item(index.row(), 0).text()

        conn = sqlite3.connect('my_lib.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, 'Успех', 'Книга удалена!')
        self.loadBooks()

    def viewBook(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        pdf_path = self.table.item(index.row(), 6).text()

        if pdf_path and os.path.exists(pdf_path):
            try:
                if sys.platform == 'win32':
                    os.startfile(pdf_path)
                elif sys.platform == 'darwin':
                    subprocess.call(['open', pdf_path])
                else:
                    subprocess.call(['xdg-open', pdf_path])
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть PDF файл: {e}')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Путь к PDF файлу не найден или файл не существует!')

    def clearInputs(self):
        self.name_input.clear()
        self.author_input.clear()
        self.genre_input.clear()
        self.rating_input.clear()
        self.status_input.clear()
        self.pdf_path_input.clear()

    def cellClicked(self, row, column):
        # Do nothing for now
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookApp()
    ex.show()
    sys.exit(app.exec_())
