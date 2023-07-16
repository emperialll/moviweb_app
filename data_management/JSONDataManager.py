import json
import requests
from .DataManager import DataManagerInterface

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a dictionary of all users
        users = read_json_file(self.filename)
        return users

    def get_user_movies(self, user_id):
        # Return a dictionary of all movies for a given user
        users = read_json_file(self.filename)
        user = users.get(user_id, None)
        return user["movies"]

    def add_user(self, user_details):
        users = read_json_file(self.filename)
        users_id_list = list(users.keys())
        if len(users_id_list) == 0:
            user_id = "1"
        else:
            new_user_id_generation = int(users_id_list[-1]) + 1
            user_id = str(new_user_id_generation)
        users[user_id] = user_details
        write_json_file(self.filename, users)

    def add_movie(self, user_id, movie_title):
        users = read_json_file(self.filename)
        user_movies = users[user_id]["movies"]
        response = requests.get(API + movie_title)
        response.raise_for_status()
        movie_dict_data = json.loads(response.text)

        movies_id_list = list(user_movies.keys())

        if len(movies_id_list) == 0:
            movie_id = '1'
        else:
            new_movie_id_generation = int(movies_id_list[-1]) + 1
            movie_id = str(new_movie_id_generation)

        user_movies[movie_id] = {
            'name': movie_dict_data['Title'],
            'director': movie_dict_data['Director'],
            'rating': float(movie_dict_data['imdbRating']),
            'year': movie_dict_data['Year']
        }

        users.setdefault(user_id, {})["movies"] = user_movies
        write_json_file(self.filename, users)

    def update_movie(self, user_id, movie_id, movie_title, movie_director,
                     movie_rating, movie_year):
        users = read_json_file(self.filename)
        users[user_id]["movies"][movie_id] = {'name': movie_title,
                                              'director': movie_director,
                                              'rating': movie_rating,
                                              'year': movie_year}

        write_json_file(self.filename, users)

    def delete_movie(self, user_id, movie_id):
        users = read_json_file(self.filename)
        movies = users[user_id]["movies"]
        movies.pop(movie_id)
        write_json_file(self.filename, users)
