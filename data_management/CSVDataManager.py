import csv
import json
import os
import requests
from .DataManager import DataManagerInterface

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='

def read_csv_file(file_path):
    users = {}
    
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            user_id = row['User ID']
            user_name = row['User Name']
            movie_id = row['Movie ID']
            movie_name = row['Movie Name']
            director = row['Director']
            year = row['Year']
            rating = row['Rating']
            note = row['Note']
            
            # Check if the user exists in the dictionary, if not, create a new user
            if user_id not in users:
                users[user_id] = {
                    'name': user_name,
                    'movies': {}
                }
            
            # Add the movie to the user's dictionary of movies
            users[user_id]['movies'][movie_id] = {
                'name': movie_name,
                'director': director,
                'year': year,
                'rating': rating,
                'note': note
            }
    
    return users

def write_csv_file(file_path, users):
    field_names = ['User ID', 'User Name', 'Movie ID', 'Movie Name', 'Director', 'Year', 'Rating', 'Note']
    
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=field_names)
        csv_writer.writeheader()
        
        for user_id, user_data in users.items():
            user_name = user_data['name']
            movies = user_data['movies']
            
            for movie_id, movie_data in movies.items():
                movie_name = movie_data['name']
                director = movie_data['director']
                year = movie_data['year']
                rating = movie_data['rating']
                note = movie_data['note']
                
                csv_writer.writerow({
                    'User ID': user_id,
                    'User Name': user_name,
                    'Movie ID': movie_id,
                    'Movie Name': movie_name,
                    'Director': director,
                    'Year': year,
                    'Rating': rating,
                    'Note': note
                })


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a dictionary of all users
        users = read_csv_file(self.filename)
        return users

    def get_user_movies(self, user_id):
        # Return a dictionary of all movies for a given user
        users = read_csv_file(self.filename)
        user = users.get(user_id, None)
        return user["movies"]
    
    def add_user(self, name):
        users = {}
        if os.path.exists(self.filename):
            users = read_csv_file(self.filename)
            user_id = int(list(users.keys())[-1]) + 1
            users[user_id] = {'name': name, 'movies':{'': {'name': '', 'director': '', 'year': '', 'rating': '', 'note': ''}}}
        else:
            users[1] = {'name': name, 'movies':{'': {'name': '', 'director': '', 'year': '', 'rating': '', 'note': ''}}}
        write_csv_file(self.filename, users)

    def add_movie(self, user_id, movie_title):
        users = read_csv_file(self.filename)
        if users is not None:
            user_movies = users.get(user_id, {}).get("movies", {})
            response = requests.get(API + movie_title)
            response.raise_for_status()
            movie_dict_data = json.loads(response.text)
            if movie_dict_data['Response'] == 'False':
                return False
            else:
                movies_id_list = list(users[user_id]['movies'].keys())

                if len(movies_id_list) == 0 or movies_id_list[-1] == '':
                    movie_id = 1
                else:
                    movie_id = int(movies_id_list[-1]) + 1
                
                if users[user_id]['movies'] == {'': {'name': '', 'director': '', 'year': '', 'rating': '', 'note': ''}}:
                    users[user_id]['movies'][movie_id] = users[user_id]['movies'].pop('')
                    users[user_id]['movies'][movie_id] = {'name': movie_dict_data['Title'], 
                                                        'director': movie_dict_data['Director'],
                                                        'rating': movie_dict_data['imdbRating'],
                                                        'year': movie_dict_data['Year'],
                                                        'note': ''}
                else:
                    users[user_id]['movies'][movie_id] = {'name': movie_dict_data['Title'], 
                                                        'director': movie_dict_data['Director'],
                                                        'rating': movie_dict_data['imdbRating'],
                                                        'year': movie_dict_data['Year'],
                                                        'note': ''}
        write_csv_file(self.filename, users)

    def update_movie(self, user_id, movie_id, movie_title, movie_director,
                     movie_rating, movie_year):
        users = read_csv_file(self.filename)
        if users is not None:
            try:
                users[user_id]["movies"][movie_id] = {'name': movie_title,
                                                      'director': movie_director,
                                                      'rating': movie_rating,
                                                      'year': movie_year}
                write_csv_file(self.filename, users)
            except KeyError:
                print("Invalid user_id or movie_id")
            except ValueError:
                print("Invalid movie rating or year")

    def delete_movie(self, user_id, movie_id):
        users = read_csv_file(self.filename)
        if users is not None:
            movies = users.get(user_id, {}).get("movies", {})
            try:
                movies.pop(movie_id)
                write_csv_file(self.filename, users)
            except KeyError:
                print("Invalid user_id or movie_id")