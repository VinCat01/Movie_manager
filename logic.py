import json
import os



def load_movies(path: str) -> list[dict]:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, IOError):
        return []
    pass


def save_movies(path: str, movies: list[dict]) -> None:
    """Сохранение списка фильмов в JSON-файл."""
    pass


def add_movie(movies: list[dict], title: str, year: int) -> list[dict]:
    """Добавление нового фильма в список."""
    pass


def mark_watched(movies: list[dict], movie_id: int) -> list[dict]:
    """Отметить фильм как просмотренный."""
    pass


def find_by_year(movies: list[dict], year: int) -> list[dict]:
    """Поиск всех фильмов указанного года."""
    pass
