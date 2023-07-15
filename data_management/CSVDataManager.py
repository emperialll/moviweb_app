import csv
from DataManager import DataManagerInterface


def read_csv_file(file_path):
    data = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            user_id = row['User ID']
            user_name = row['User Name']
            movie_id = row['Movie ID']
            movie_name = row['Movie Name']
            director = row['Director']
            year = int(row['Year'])
            rating = float(row['Rating'])

            if user_id not in data:
                data[user_id] = {
                    'name': user_name,
                    'movies': {}
                }

            data[user_id]['movies'][movie_id] = {
                'name': movie_name,
                'director': director,
                'year': year,
                'rating': rating
            }

    return data


class CSVDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a dictionary of all users
        users = read_csv_file("../user_data/users.csv")
        return users

    def get_user_movies(self, user_id):
        # Return a dictionary of all movies for a given user
        users = read_csv_file("../user_data/users.csv")
        user = users.get(id, None)
        return user["movies"]

    def update_user_movie(self, movie, note):
        # update the note on a certain user's movie
        pass
