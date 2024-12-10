import psycopg2
from psycopg2 import sql, OperationalError, IntegrityError
from config import db_name, user, password

class Library:
    def __init__(self, db_name, user, password, host="localhost", port=5432):
        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.connection.autocommit = True
            self._initialize_database()
        except OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def _initialize_database(self):
        # Создает таблицу книг, если она еще не существует
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(255) NOT NULL,
                    year INT NOT NULL,
                    status VARCHAR(50) DEFAULT 'в наличии'
                );
                """)
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")

    def add_book(self, title, author, year):
        # Добавляет книгу в библиотеку
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO books (title, author, year, status)
                VALUES (%s, %s, %s, 'в наличии') RETURNING id;
                """, (title, author, year))
                book_id = cursor.fetchone()[0]
                print(f"Книга '{title}' добавлена с ID: {book_id}")
        except IntegrityError as e:
            print(f"Ошибка при добавлении книги: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def delete_book(self, book_id):
        # Удаляет книгу из библиотеки
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE id = %s;", (book_id,))
                match cursor.rowcount:
                    case 1:
                        print(f"Книга с ID {book_id} удалена.")
                    case 0:
                        print(f"Книга с ID {book_id} не найдена.")
        except Exception as e:
            print(f"Ошибка при удалении книги: {e}")

    def search_books(self, query, field):
        # Ищет книги по title, author или year
        if field not in ["title", "author", "year"]:
            print("Некорректное поле поиска. Доступные поля: title, author, year.")
            return

        query_field = sql.Identifier(field)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql.SQL("""
                SELECT id, title, author, year, status
                FROM books
                WHERE {} ILIKE %s;
                """).format(query_field), (f"%{query}%",))
                results = cursor.fetchall()
                if results:
                    print("Найденные книги:")
                    for book in results:
                        self.display_book(book)
                else:
                    print("Книги не найдены.")
        except Exception as e:
            print(f"Ошибка при поиске книг: {e}")

    def display_books(self):
        # Отображает все книги в библиотеке
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT id, title, author, year, status FROM books;")
                books = cursor.fetchall()
                if not books:
                    print("Библиотека пуста.")
                else:
                    print("Список книг:")
                    for book in books:
                        self.display_book(book)
        except Exception as e:
            print(f"Ошибка при отображении книг: {e}")

    def update_status(self, book_id, new_status):
        # Изменяет статус книги
        if new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус. Допустимые статусы: 'в наличии', 'выдана'.")
            return

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                UPDATE books
                SET status = %s
                WHERE id = %s;
                """, (new_status, book_id))
                match cursor.rowcount:
                    case 1:
                        print(f"Статус книги с ID {book_id} изменён на '{new_status}'.")
                    case 0:
                        print(f"Книга с ID {book_id} не найдена.")
        except Exception as e:
            print(f"Ошибка при обновлении статуса книги: {e}")

    @staticmethod
    def display_book(book):
        # Выводит информацию о книге
        print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}, "
              f"Год: {book[3]}, Статус: {book[4]}")

    def close(self):
        # Закрывает соединение с базой данных
        try:
            self.connection.close()
        except Exception as e:
            print(f"Ошибка при закрытии соединения: {e}")

def main():
    library = Library(db_name=db_name, user=user, password=password)

    while True:
        print("""\nМеню:\n
        1. Добавить книгу\n
        2. Удалить книгу\n
        3. Искать книгу\n
        4. Отобразить все книги\n
        5. Изменить статус книги\n
        6. Выход\n\n""")

        choice = input("Выберите действие: ")
        match choice:
            case "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
            case "2":
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            case "3":
                field = input("Введите поле для поиска (title, author, year): ")
                query = input("Введите запрос для поиска: ")
                library.search_books(query, field)
            case "4":
                library.display_books()
            case "5":
                book_id = int(input("Введите ID книги: "))
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                library.update_status(book_id, new_status)
            case "6":
                print("Выход из программы.")
                library.close()
                break
            case _:
                print("Некорректный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()