import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_lib.db')
cursor = connection.cursor()

# Создаем таблицу books с колонкой для пути к PDF файлу
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating TEXT NOT NULL,
    status TEXT NOT NULL,
    pdf_path TEXT
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
