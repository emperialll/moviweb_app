import json
import requests
from .DataManager import DataManagerInterface

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {file_path}")
    return None


def write_json_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except IOError:
        print(f"Error writing to file: {file_path}")


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
        if users is not None:
            user = users.get(user_id, None)
            if user:
                return user.get("movies", None)
        return None

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
        if users is not None:
            user_movies = users.get(user_id, {}).get("movies", {})
            try:
                response = requests.get(API + movie_title)
                response.raise_for_status()
                movie_dict_data = json.loads(response.text)
                if movie_dict_data['Response'] == 'False':
                    return False
                else:
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
            except requests.exceptions.RequestException as e:
                print(f"Error making API request: {e}")
            except (KeyError, ValueError) as e:
                print(f"Error processing movie data: {e}")

    def update_movie(self, user_id, movie_id, movie_title, movie_director,
                     movie_rating, movie_year):
        users = read_json_file(self.filename)
        if users is not None:
            try:
                users[user_id]["movies"][movie_id] = {'name': movie_title,
                                                      'director': movie_director,
                                                      'rating': movie_rating,
                                                      'year': movie_year}
                write_json_file(self.filename, users)
            except KeyError:
                print("Invalid user_id or movie_id")
            except ValueError:
                print("Invalid movie rating or year")

    def delete_movie(self, user_id, movie_id):
        users = read_json_file(self.filename)
        if users is not None:
            movies = users.get(user_id, {}).get("movies", {})
            try:
                movies.pop(movie_id)
                write_json_file(self.filename, users)
            except KeyError:
                print("Invalid user_id or movie_id")
