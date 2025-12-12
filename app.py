import logic

FILE_PATH = "movies.json"

movies = logic.load_movies(FILE_PATH)

while True:
    print("КАЛАТОГ ФИЛЬМОВ")
    print("")
    print("1. Показать все фильмы")
    print("2. Добавить фильм")
    print("3. Отметить фильм как просмотренный")
    print("4. Найти фильмы по году")
    print("0. Выход")

    choice = input("Выберите действие: ").strip()

    if choice == '1':
        if not movies:
            print("\nСписок фильмов пуст.")
        else:
            print(f"\nВсего фильмов: {len(movies)}")
            for movie in movies:
                status = "[Смотрел]" if movie['watched'] else "[Не смотрел]"
                print(f"{movie['id']}. {movie['title']} ({movie['year']}) - Просмотрен: {status}")

    elif choice == '2':
        print("\nДобавление фильма")
        title = input("Название: ").strip()
        if not title:
            print("Ошибка: название обязательно")
            continue
        try:
            year = int(input("Год выпуска: ").strip())
        except ValueError:
            print("Ошибка: введите число для года")
            continue

        movies = logic.add_movie(movies, title, year)
        logic.save_movies(FILE_PATH, movies)
        print(f"Фильм '{title}' добавлен!")

    elif choice == '3':
        if not movies:
            print("\nСписок фильмов пуст")
            continue
        print("\nДоступные фильмы:")
        for movie in movies:
            status = "[Смотрел]" if movie['watched'] else "[Не смотрел]"
            print(f"{movie['id']}. {movie['title']} - Просмотрен: {status}")
        try:
            movie_id = int(input("\nВведите ID фильма для отметки: ").strip())
        except ValueError:
            print("Ошибка: введите число для ID")
            continue
        if not any(movie['id'] == movie_id for movie in movies):
            print(f"Фильм с ID {movie_id} не найден")
            continue
        movies = logic.mark_watched(movies, movie_id)
        logic.save_movies(FILE_PATH, movies)
        print("Фильм отмечен как просмотренный!")

    elif choice == '4':
        try:
            year = int(input("\nВведите год для поиска: ").strip())
        except ValueError:
            print("Ошибка: введите число для года")
            continue
        found_movies = logic.find_by_year(movies, year)
        if found_movies:
            print(f"\nНайдено {len(found_movies)} фильмов за {year} год:")
            for movie in found_movies:
                status = "[Смотрел]" if movie['watched'] else "[Не смотрел]"
                print(f"{movie['id']}. {movie['title']} - Просмотрен: {status}")
        else:
            print(f"Фильмы за {year} год не найдены")

    elif choice == '0':
        logic.save_movies(FILE_PATH, movies)
        print("Выход")
        quit(0)

    else:
        print("Ошибка: выберите от 0 до 4")
