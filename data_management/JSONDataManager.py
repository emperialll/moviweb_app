import json
from DataManager import DataManagerInterface


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        # Return a dictionary of all users
        users = read_json_file("../user_data/users.json")
        return users

    def get_user_movies(self, user_id):
        # Return a dictionary of all movies for a given user
        users = read_json_file("../user_data/users.json")
        user = users.get(id, None)
        return user["movies"]

    def update_user_movie(self, movie, note):
        # update the note on a certain user's movie
        pass