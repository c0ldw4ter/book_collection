import uuid

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, year):
       # Добавляет книгу в библиотеку
        book = {
            "id": str(uuid.uuid4()),
            "title": title,
            "author": author,
            "year": year,
            "status": "в наличии"
        }
        self.books.append(book)
        print(f"Книга '{title}' добавлена с ID: {book['id']}")

    def delete_book(self, book_id):
        # Удаляет книгу из библиотеки
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                print(f"Книга с ID {book_id} удалена.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, query, field):
        # Ищет книги по title, author или year
        if field not in ["title", "author", "year"]:
            print("Некорректное поле поиска. Доступные поля: title, author, year.")
            return

        results = [book for book in self.books if query.lower() in str(book[field]).lower()]
        if results:
            print("Найденные книги:")
            for book in results:
                self.display_book(book)
        else:
            print("Книги не найдены.")

    def display_books(self):
        # Отображает все книги в библиотеке
        if not self.books:
            print("Библиотека пуста.")
        else:
            print("Список книг:")
            for book in self.books:
                self.display_book(book)

    def update_status(self, book_id, new_status):
        # Изменяет статус книги
        if new_status not in ["в наличии", "выдана"]:
            print("Некорректный статус. Допустимые статусы: 'в наличии', 'выдана'.")
            return

        for book in self.books:
            if book["id"] == book_id:
                book["status"] = new_status
                print(f"Статус книги с ID {book_id} изменён на '{new_status}'.")
                return
        print(f"Книга с ID {book_id} не найдена.")

    @staticmethod
    def display_book(book):
        # Выводит информацию о книге
        print(f"ID: {book['id']}, Название: {book['title']}, Автор: {book['author']}, "
              f"Год: {book['year']}, Статус: {book['status']}")


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания книги: ")
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            library.delete_book(book_id)
        elif choice == "3":
            field = input("Введите поле для поиска (title, author, year): ")
            query = input("Введите запрос для поиска: ")
            library.search_books(query, field)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = input("Введите ID книги: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, new_status)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()


