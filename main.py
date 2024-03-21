# import libraries
import flet as ft
import sqlite3

# Establishing a connection to the database
conn = sqlite3.connect('database.db — копия')
c = conn.cursor()

# main function
def main(page: ft.page):
    page.theme_mode = ft.ThemeMode.DARK
    # create text fields for entering information
    txt_name_book = ft.TextField(label="название книги", width=300)
    txt_name_author = ft.TextField(label="автор", width=300)
    txt_name_genre = ft.TextField(label="жанр", width=300)
    txt_rating = ft.TextField(label="рейтинг", width=300)
    txt_status = ft.TextField(label="статус", width=300)

    def button_clicked(e):
        # getting values from text fields
        name_book = txt_name_book.value
        author_book = txt_name_author.value
        genre_book = txt_name_genre.value
        rating_book = txt_rating.value
        status_book = txt_status.value

        if name_book and author_book and genre_book and rating_book and status_book:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            c.execute(
                "insert into books (name, author, genre, rating, status) values (?,?,?,?,?)",
                (name_book, author_book, genre_book, rating_book, status_book)
            )

            conn.commit()
            output_text.value = "книга добавлена"
        else:
            output_text.value = "заполни все поля"

    # function for adding a book
    def add_book(e):
        button_clicked(e)
    # create a text field to display information about adding a book
    output_text = ft.Text()

    # create a button to add a book
    submit_btn = ft.ElevatedButton(text="добавить", on_click=add_book)

    def get_books():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("select * from books")
        return c.fetchall()

    # function for filling the table with book data
    def fill_table(data):
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("№")),
                ft.DataColumn(ft.Text("название")),
                ft.DataColumn(ft.Text("автор")),
                ft.DataColumn(ft.Text("жанр")),
                ft.DataColumn(ft.Text("рейтинг")),
                ft.DataColumn(ft.Text("статус")),
                ft.DataColumn(ft.IconButton(icon=ft.icons.DELETE, on_click=delete_book))
            ]
        )

        for row in data:
            table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row[0])),
                    ft.DataCell(ft.Text(row[1])),
                    ft.DataCell(ft.Text(row[2])),
                    ft.DataCell(ft.Text(row[3])),
                    ft.DataCell(ft.Text(row[4])),
                    ft.DataCell(ft.Text(row[5])),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DELETE, on_click=delete_book, data=row[0]))
                ]
            ))

        return table

    # function for browsing books
    def view_books(e):
        if isinstance(page.controls[-1], ft.DataTable):
            page.controls.pop()

        data = get_books()
        table = fill_table(data)
        # display books as a scrolling list
        page.scroll = ft.ScrollMode.AUTO
        page.controls.append(table)
        page.update()

    # function for deleting a book
    def delete_book(e):
        index = e.control.data
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("delete from books where id=?", (index,))
        conn.commit()
        view_books(e)

    view_books_btn = ft.ElevatedButton(text="покажи книги", on_click=view_books)

    # add all elements to the page
    page.add(txt_name_book,
             txt_name_author,
             txt_name_genre,
             txt_rating,
             txt_status,
             output_text,
             submit_btn,
             view_books_btn)

# run the application with the main function as the target
ft.app(target=main)
# below is a web-based version of the app
# ft.app(target=main, view=ft.AppView.WEB_BROWSER)