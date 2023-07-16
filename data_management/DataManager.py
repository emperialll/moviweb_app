from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, user_details):
        pass

    @abstractmethod
    def add_movie(self, user_id, movie_title):
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, movie_title, movie_director,
                     movie_rating, movie_year):
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        pass