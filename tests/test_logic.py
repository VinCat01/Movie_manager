import pytest
import json
import tempfile
import os
import sys
from pathlib import Path

parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

import logic


@pytest.fixture
def temp_json_file():
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file_path = temp_file.name

    test_data = [
        {"id": 1, "title": "The Matrix", "year": 1999, "watched": False},
        {"id": 2, "title": "Inception", "year": 2010, "watched": True},
        {"id": 3, "title": "Interstellar", "year": 2014, "watched": False}
    ]

    with open(temp_file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    temp_file.close()
    yield temp_file_path

    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)


@pytest.fixture
def sample_movies():
    return [
        {"id": 1, "title": "The Matrix", "year": 1999, "watched": False},
        {"id": 2, "title": "Inception", "year": 2010, "watched": True},
        {"id": 3, "title": "Interstellar", "year": 2014, "watched": False}
    ]


@pytest.fixture
def empty_movies():
    return []


def test_load_movies_existing_file(temp_json_file):
    movies = logic.load_movies(temp_json_file)

    assert len(movies) == 3
    assert movies[0]['title'] == "The Matrix"
    assert movies[0]['year'] == 1999
    assert movies[0]['watched'] == False
    assert movies[0]['id'] == 1
    assert movies[1]['title'] == "Inception"
    assert movies[1]['watched'] == True


def test_load_movies_nonexistent_file():
    movies = logic.load_movies("nonexistent_file_12345.json")
    assert movies == []


def test_load_movies_empty_file():
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file_path = temp_file.name
    temp_file.close()

    movies = logic.load_movies(temp_file_path)
    assert movies == []
    os.unlink(temp_file_path)


def test_load_movies_invalid_json():
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file_path = temp_file.name

    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")

    temp_file.close()
    movies = logic.load_movies(temp_file_path)
    assert movies == []
    os.unlink(temp_file_path)


def test_save_movies(temp_json_file, sample_movies):
    modified_movies = sample_movies.copy()
    modified_movies[0]['title'] = "Matrix Reloaded"

    logic.save_movies(temp_json_file, modified_movies)

    with open(temp_json_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    assert len(saved_data) == 3
    assert saved_data[0]['title'] == "Matrix Reloaded"


def test_save_movies_empty_list(temp_json_file):
    empty_list = []
    logic.save_movies(temp_json_file, empty_list)

    with open(temp_json_file, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)

    assert saved_data == []


def test_add_movie_to_empty_list(empty_movies):
    new_movies = logic.add_movie(empty_movies, "New Movie", 2023)

    assert len(new_movies) == 1
    assert new_movies[0]['title'] == "New Movie"
    assert new_movies[0]['year'] == 2023
    assert new_movies[0]['watched'] == False
    assert new_movies[0]['id'] == 1


def test_add_movie_to_existing_list(sample_movies):
    new_movies = logic.add_movie(sample_movies, "New Movie", 2023)

    assert len(new_movies) == 4
    assert new_movies[3]['title'] == "New Movie"
    assert new_movies[3]['year'] == 2023
    assert new_movies[3]['watched'] == False
    assert new_movies[3]['id'] == 4
    assert new_movies[0]['title'] == "The Matrix"
    assert new_movies[1]['title'] == "Inception"


def test_add_multiple_movies(empty_movies):
    movies1 = logic.add_movie(empty_movies, "Movie 1", 2000)
    assert len(movies1) == 1
    assert movies1[0]['id'] == 1

    movies2 = logic.add_movie(movies1, "Movie 2", 2001)
    assert len(movies2) == 2
    assert movies2[1]['id'] == 2

    movies3 = logic.add_movie(movies2, "Movie 3", 2002)
    assert len(movies3) == 3
    assert movies3[2]['id'] == 3


def test_add_movie_preserves_original(sample_movies):
    original_copy = sample_movies.copy()
    new_movies = logic.add_movie(sample_movies, "New Movie", 2023)

    assert len(sample_movies) == 3
    assert sample_movies == original_copy
    assert len(new_movies) == 4
    assert new_movies is not sample_movies


def test_mark_watched_existing_id(sample_movies):
    new_movies = logic.mark_watched(sample_movies, 1)

    assert new_movies[0]['watched'] == True
    assert new_movies[0]['id'] == 1
    assert new_movies[1]['watched'] == True
    assert new_movies[2]['watched'] == False


def test_mark_watched_nonexistent_id(sample_movies):
    new_movies = logic.mark_watched(sample_movies, 999)

    assert len(new_movies) == 3
    assert new_movies == sample_movies
    assert new_movies[0]['watched'] == False
    assert new_movies[1]['watched'] == True
    assert new_movies[2]['watched'] == False


def test_mark_watched_already_watched(sample_movies):
    new_movies = logic.mark_watched(sample_movies, 2)
    assert new_movies[1]['watched'] == True
    assert new_movies[1]['id'] == 2


def test_mark_watched_empty_list(empty_movies):
    new_movies = logic.mark_watched(empty_movies, 1)
    assert new_movies == []


def test_find_by_year_nonexistent(sample_movies):
    found = logic.find_by_year(sample_movies, 2000)
    assert found == []


def test_find_by_year_multiple():
    movies = [
        {"id": 1, "title": "Movie 1", "year": 2000, "watched": False},
        {"id": 2, "title": "Movie 2", "year": 2001, "watched": True},
        {"id": 3, "title": "Movie 3", "year": 2000, "watched": False},
        {"id": 4, "title": "Movie 4", "year": 2000, "watched": True}
    ]

    found = logic.find_by_year(movies, 2000)

    assert len(found) == 3
    assert all(movie['year'] == 2000 for movie in found)
    found_ids = {movie['id'] for movie in found}
    assert found_ids == {1, 3, 4}


def test_find_by_year_empty_list(empty_movies):
    found = logic.find_by_year(empty_movies, 2023)
    assert found == []





def test_integration_flow(temp_json_file):
    movies = logic.load_movies(temp_json_file)
    assert len(movies) == 3

    movies = logic.add_movie(movies, "Integration Test", 2024)
    assert len(movies) == 4

    movies = logic.mark_watched(movies, 4)
    assert movies[3]['watched'] == True

    logic.save_movies(temp_json_file, movies)
    loaded_again = logic.load_movies(temp_json_file)

    assert len(loaded_again) == 4
    assert loaded_again[3]['title'] == "Integration Test"
    assert loaded_again[3]['watched'] == True


def test_movie_with_missing_fields():
    movies = [
        {"id": 1, "title": "Movie 1"},
        {"id": 2, "year": 2000},
        {"id": 3, "title": "Movie 3", "year": 2000, "watched": False, "extra": "field"}
    ]

    found = logic.find_by_year(movies, 2000)
    assert len(found) == 2
    assert found[0]['id'] == 2
    assert found[1]['id'] == 3


@pytest.mark.parametrize("year,expected_count", [
    (1999, 1),
    (2010, 1),
    (2014, 1),
    (2000, 0),
    (2020, 0)
])
def test_find_by_year_parametrized(sample_movies, year, expected_count):
    found = logic.find_by_year(sample_movies, year)
    assert len(found) == expected_count


@pytest.mark.parametrize("movie_id,should_change", [
    (1, True),
    (2, False),
    (3, True),
    (4, False),
    (0, False),
])
def test_mark_watched_parametrized(sample_movies, movie_id, should_change):
    original_watched = None
    for movie in sample_movies:
        if movie['id'] == movie_id:
            original_watched = movie['watched']
            break

    new_movies = logic.mark_watched(sample_movies, movie_id)

    new_watched = None
    for movie in new_movies:
        if movie['id'] == movie_id:
            new_watched = movie['watched']
            break

    if should_change and original_watched is not None:
        assert new_watched == True
        assert new_watched != original_watched
    else:
        if original_watched is not None:
            assert new_watched == original_watched