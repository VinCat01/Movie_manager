from logic import load_movies, save_movies, add_movie, mark_watched, find_by_year

DATA_FILE = "movies.json"

def main():
    movies = load_movies(DATA_FILE)

    while True:
        print("\nКаталог фильмов")
        print("1. Показать все фильмы")
        print("2. Добавить фильм")
        print("3. Отметить фильм как просмотренный")
        print("4. Найти фильмы по году")
        print("0. Выход")

        choice = input("Выберите пункт: ")

        if choice == "1":
            pass  # TODO: вывод списка фильмов

        elif choice == "2":
            pass  # TODO: ввод данных и вызов add_movie()

        elif choice == "3":
            pass  # TODO: ввод id и вызов mark_watched()

        elif choice == "4":
            pass  # TODO: ввод года и вывод результатов

        elif choice == "0":
            save_movies(DATA_FILE, movies)
            print("До свидания!")
            break

        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()
