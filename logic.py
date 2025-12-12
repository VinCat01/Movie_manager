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



def save_movies(path: str, movies: list[dict]) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(movies, file, ensure_ascii=False, indent=2)



def add_movie(movies: list[dict], title: str, year: int) -> list[dict]:
    updated_movies = movies.copy()
    if updated_movies:
        max_id = max(movie.get('id', 0) for movie in updated_movies)
    else:
        max_id = 0
    new_movie = {
        "id": max_id + 1,
        "title": title,
        "year": year,
        "watched": False
    }
    updated_movies.append(new_movie)
    return updated_movies



def mark_watched(movies: list[dict], movie_id: int) -> list[dict]:
    updated_movies = movies.copy()
    for movie in updated_movies:
        if movie.get('id') == movie_id:
            movie['watched'] = True
            break

    return updated_movies



def find_by_year(movies: list[dict], year: int) -> list[dict]:
    return [movie for movie in movies if movie.get('year') == year]
    pass
