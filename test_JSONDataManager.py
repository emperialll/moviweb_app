import pytest
import json
from data_management.JSONDataManager import JSONDataManager
#TEST
# Test data
USER_DATA = {
    "1": {
        "name": "John",
        "movies": {
            "1": {
                "name": "Movie 1",
                "director": "Director 1",
                "rating": 7.5,
                "year": "2020"
            },
            "2": {
                "name": "Movie 2",
                "director": "Director 2",
                "rating": 8.2,
                "year": "2019"
            }
        }
    },
    "2": {
        "name": "Jane",
        "movies": {
            "1": {
                "name": "Movie 3",
                "director": "Director 3",
                "rating": 6.9,
                "year": "2021"
            }
        }
    }
}

# Fixture to initialize JSONDataManager with test data
@pytest.fixture
def json_data_manager(tmpdir):
    # Create a temporary JSON file
    json_file = tmpdir.join("test.json")
    json_file.write_text(json.dumps(USER_DATA), encoding='utf-8')

    # Initialize JSONDataManager with the temporary file
    data_manager = JSONDataManager(str(json_file))

    yield data_manager

    # Teardown: Delete the temporary file
    json_file.remove()


def test_get_all_users(json_data_manager):
    users = json_data_manager.get_all_users()
    assert users == USER_DATA


def test_get_user_movies(json_data_manager):
    user_id = "1"
    movies = json_data_manager.get_user_movies(user_id)
    assert movies == USER_DATA[user_id]["movies"]


def test_add_user(json_data_manager):
    new_user = {"name": "New User", "movies": {}}
    json_data_manager.add_user(new_user)
    users = json_data_manager.get_all_users()
    assert len(users) == len(USER_DATA) + 1
    assert "3" in users
    assert users["3"] == new_user


def test_add_movie(json_data_manager):
    user_id = "1"
    movie_title = "Titanic"
    json_data_manager.add_movie(user_id, movie_title)
    movies = json_data_manager.get_user_movies(user_id)
    assert len(movies) == len(USER_DATA[user_id]["movies"]) + 1
    assert "3" in movies
    assert movies["3"]["name"] == movie_title


def test_update_movie(json_data_manager):
    user_id = "1"
    movie_id = "1"
    movie_title = "Updated Movie"
    movie_director = "Updated Director"
    movie_rating = 9.0
    movie_year = "2022"
    json_data_manager.update_movie(user_id, movie_id, movie_title,
                                   movie_director, movie_rating, movie_year)
    movies = json_data_manager.get_user_movies(user_id)
    assert movies[movie_id]["name"] == movie_title
    assert movies[movie_id]["director"] == movie_director
    assert movies[movie_id]["rating"] == movie_rating
    assert movies[movie_id]["year"] == movie_year


def test_delete_movie(json_data_manager):
    user_id = "1"
    movie_id = "1"
    json_data_manager.delete_movie(user_id, movie_id)
    movies = json_data_manager.get_user_movies(user_id)
    assert len(movies) == len(USER_DATA[user_id]["movies"]) - 1
    assert movie_id not in movies


if __name__ == "__main__":
    pytest.main()
