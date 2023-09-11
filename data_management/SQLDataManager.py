import requests
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from data_management.SQL_Data_Models import db, User, UserMovies, Movies, Reviews
from .DataManager import DataManagerInterface

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app, db_file_name):
        self.db = None  # Initialize the db attribute

        self.init_db(app, db_file_name)  # Call the init_db method

    def init_db(self, app, db_file_name):
        # Configure the database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_name}'

        # Initialize the SQLAlchemy extension with the Flask application
        db.init_app(app)

        self.db = db

    def get_all_users(self):
        # Fetch the list of users from the database
        users = User.query.all()
        return users

    def get_user_movies(self, user_id):
        # Retrieve all movies associated with the user
        user_favorite_movies = db.session.query(UserMovies, Movies). \
            join(Movies, UserMovies.movie_id == Movies.movie_id). \
            filter(UserMovies.user_id == user_id).all()

        # Retrieve the user's information
        user = User.query.filter_by(id=user_id).first()
        return user_favorite_movies, user

    def add_user(self, name, email, password):
        # Create a new User object with the form data
        new_user = User(name=name, email=email, password=password)

        # Add the user to the database
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, user_id, movie_title):
        # Check if the movie already exists in the Movies table
        existing_movie = Movies.query.filter_by(title=movie_title).first()

        if existing_movie:
            # If the movie exists, add it to UserMovies and return
            new_user_movie = UserMovies(
                user_id=user_id, movie_id=existing_movie.movie_id, note="")
            db.session.add(new_user_movie)
            db.session.commit()
            return "Movie already exists in the database."

        # If the movie doesn't exist, fetch data from the API
        response = requests.get(API + movie_title)
        response.raise_for_status()
        movie_dict_data = json.loads(response.text)
        if movie_dict_data['Response'] == 'False':
            return "Movie not found!"
        else:
            # Create a new movie object with the form data
            new_movie = Movies(title=movie_dict_data['Title'],
                               year=movie_dict_data['Year'],
                               rating=movie_dict_data['imdbRating'],
                               genre=movie_dict_data['Genre'],
                               director=movie_dict_data['Director'],
                               writer=movie_dict_data['Writer'],
                               actors=movie_dict_data['Actors'],
                               plot=movie_dict_data['Plot'],
                               language=movie_dict_data['Language'],
                               country=movie_dict_data['Country'],
                               poster=movie_dict_data['Poster'],
                               _type=movie_dict_data['Type'])
            # Add the movie to the database
            db.session.add(new_movie)
            db.session.commit()

            # Retrieve the movie_id after it's been added to the database
            movie_id = new_movie.movie_id  # Assuming 'id' is the primary key of the Movies table

        new_user_movie = UserMovies(
            user_id=user_id, movie_id=movie_id, note="")
        # Add the user movie association to the database
        db.session.add(new_user_movie)
        db.session.commit()

        return "Movie added to the database and UserMovies."

    def update_movie(self, user_id, movie_id, movie_title,
                     movie_director, movie_rating, movie_year,
                     movie_note):
        movie = UserMovies.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()
        movie.title = movie_title
        movie.director = movie_director
        movie.rating = movie_rating
        movie.year = movie_year
        movie.note = movie_note
        # Update database
        db.session.commit()

    def delete_movie(self, user_id, movie_id):
        try:
            movie_to_delete = UserMovies.query.filter_by(
                movie_id=movie_id, user_id=user_id).first()
            # Delete the movie object from the session
            db.session.delete(movie_to_delete)
            db.session.commit()  # Commit the changes to the database
            return True
        except Exception as error:
            # Handle the exception appropriately, e.g., logging, error message, etc.
            print(error)

    def add_review(self, user_id, movie_id, rating, review):
        try:
            # Create a new review object with the form data
            new_review = Reviews(movie_id=movie_id,
                                 user_id=user_id,
                                 review_text=review,
                                 rating=rating)
            # Add the review to the database
            db.session.add(new_review)
            db.session.commit()
        except Exception as e:
            print(e)

    def get_reviews_for_movie(self, movie_id):
        reviews = Reviews.query.filter_by(movie_id=movie_id).all()
        return reviews
