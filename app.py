"""
Flask Application and Data Management Import Statements

This section imports necessary modules and classes for creating a Flask 
application, rendering templates, and utilizing data management functionalities
from JSON and CSV data managers.

Imported Modules:
    Flask:
        The Flask class from the 'flask' module used for 
        creating web applications.
    render_template:
        A function from the 'flask' module for rendering HTML templates.
    request:
        A module from the 'flask' module used to handle incoming requests.

Imported Data Managers:
    JSONDataManager: A class from 'data_management.JSONDataManager' for 
    managing JSON data.
    CSVDataManager: A class from 'data_management.CSVDataManager' for 
    managing CSV data.
"""
import json
import os
import requests
import sys
from flask import Flask, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from data_management.JSONDataManager import JSONDataManager
from data_management.CSVDataManager import CSVDataManager
from data_management.SQLDataManager import SQLiteDataManager
from data_management.SQL_Data_Models import db, User, UserMovies, Movies


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Use the appropriate path to your JSON, CSV or SQL file

# DATA_FILE_PATH = "user_data/users.json"
# data_manager = JSONDataManager(DATA_FILE_PATH)

# DATA_FILE_PATH = "user_data/users.csv"
# data_manager = CSVDataManager(DATA_FILE_PATH)

DATA_FILE_PATH = os.path.abspath('user_data/user_movies.sqlite')
data_manager = SQLiteDataManager(app, DATA_FILE_PATH)


def encrypt_password(password):
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return pw_hash


def check_password(password, pw_hash):
    password_is_match = bcrypt.check_password_hash(pw_hash, password)
    return password_is_match


def is_item_in_dict(item, dictionary):
    """
    Check if an item is present in a dictionary.
    This function checks whether the specified item exists as a key in the given dictionary.
    Args:
        item: The item to be checked for presence in the dictionary.
        dictionary (dict): The dictionary to be checked.
    Returns:
        bool: True if the item is found in the dictionary as a key, False otherwise.
    """
    if item in dictionary.keys():
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Route: Home
    Renders the homepage template.
    Returns:
        Rendered HTML template.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = data_manager.get_all_users()
        if type(users) is dict:  # For JSON and CSV Data Model
            for user_id, user_data in users.items():
                if user_data["email"] == email:
                    if check_password(password, user_data["password"]):
                        return redirect(url_for('my_movies', user_id=user_id))
        # For SQL Data Model
        user = User.query.filter_by(email=email).first()
        if check_password(password, user.password):
            return redirect(url_for('my_movies', user_id=user.id))
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
    Route: List Users
    Retrieves a list of users and renders the users template.
    Returns:
        Rendered HTML template with user data.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def my_movies(user_id):
    """
    Route: User Movies
    Retrieves movies for a specific user and renders the movies template.
    Args:
        user_id (str): User ID.
    Returns:
        Rendered HTML template with user's movies.
    """
    try:
        users = data_manager.get_all_users()
        if type(users) is dict:
            if is_item_in_dict(user_id, users):
                user_name = users[user_id]["name"]
                user_movies = data_manager.get_user_movies(user_id)
                return render_template('movies.html', movies=user_movies,
                                       user_name=user_name,
                                       user_id=user_id)
            else:
                return render_template('304.html')
        movies, user = data_manager.get_user_movies(user_id)
        return render_template('movies.html', movies=movies,
                               user_name=user.name,
                               id=user_id)
    except Exception as error:
        # Handle the exception appropriately, e.g., logging, error message, etc.
        return render_template('error.html', error_message=str(error))


if DATA_FILE_PATH.lower().endswith('.json'):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Route: Register (JSON)
        Handles user registration and rendering of registration form.
        Returns:
            "Registration successful!" upon successful POST request.
            Rendered HTML registration form template for GET request.
        """
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = encrypt_password(request.form.get('password'))
            user_details = {"name": name, "email": email,
                            "password": password, "movies": {}}
            data_manager.add_user(user_details)
            return "Registration successful!"

        return render_template('register.html')
else:
    # DATA_FILE_PATH.lower().endswith('.csv'):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Route: Register (CSV)
        Handles user registration and rendering of registration form.
        Returns:
            "Registration successful!" upon successful POST request.
            Rendered HTML registration form template for GET request.
        """
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = encrypt_password(request.form.get('password'))
            data_manager.add_user(name, email, password)
            return "Registration successful!"

        return render_template('register.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movies(user_id):
    """
    Route: Add Movie
    Handles adding a movie to a user's collection and rendering the movie addition form.
    Args:
        user_id (str): User ID.
    Returns:
        "Movie has been added successfully!" upon successful POST request.
        "Movie not found!" if the movie addition is unsuccessful.
        Rendered HTML add-movie form template for GET request.
    """
    if request.method == 'POST':
        movie_title = request.form.get('name')
        if data_manager.add_movie(user_id, movie_title) is False:
            return "Movie not found!"
        return "Movie has been added successfully!"

    return render_template('add-movie.html', user_id=user_id)


if DATA_FILE_PATH.lower().endswith('.json') or DATA_FILE_PATH.lower().endswith('.csv'):
    @app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
    def update_movies(user_id, movie_id):
        """
        Route: Update Movie

        Handles updating movie details for a user and rendering the movie update form.

        Args:
            user_id (str): User ID.
            movie_id (str): Movie ID.

        Returns:
            "Movie has been updated successfully!" upon successful POST request.
            Rendered HTML update-movie form template for GET request.
        """
        try:
            movies = data_manager.get_user_movies(user_id)
            movie = movies[movie_id]
            if request.method == 'POST':
                movie_title = request.form.get('name')
                movie_director = request.form.get('director')
                movie_rating = request.form.get('rating')
                movie_year = request.form.get('year')
                movie_note = request.form.get('note')
                data_manager.update_movie(user_id, movie_id, movie_title,
                                          movie_director, movie_rating,
                                          movie_year, movie_note)
                return "Movie has been updated successfully!"

            return render_template('update-movie.html',
                                   user_id=user_id,
                                   movie_id=movie_id,
                                   movie_title=movie['name'],
                                   movie_rating=movie['rating'],
                                   movie_director=movie['director'],
                                   movie_year=movie['year'],
                                   movie_note=movie['note'])
        except Exception as error:
            # Handle the exception appropriately, e.g., logging, error message, etc.
            return render_template('error.html', error_message=str(error))
else:
    @app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
    def update_movies(user_id, movie_id):
        try:
            if request.method == 'POST':
                movie_title = request.form.get('name')
                movie_director = request.form.get('director')
                movie_rating = request.form.get('rating')
                movie_year = request.form.get('year')
                movie_note = request.form.get('note')
                data_manager.update_movie(user_id, movie_id, movie_title,
                                          movie_director, movie_rating,
                                          movie_year, movie_note)
                return "Movie has been updated successfully!"

            movies, user = data_manager.get_user_movies(user_id)
            for movie in movies:
                if movie.movie_id == int(movie_id):
                    return render_template('update-movie.html',
                                           user_id=user_id,
                                           movie_id=movie_id,
                                           movie_title=movie.title,
                                           movie_rating=movie.rating,
                                           movie_director=movie.director,
                                           movie_year=movie.year,
                                           movie_note=movie.note)
            return "Movie not found"

        except Exception as error:
            print(error)
            # Handle the exception appropriately, e.g., logging, error message, etc.
            return render_template('error.html', error_message=str(error))


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    """
    Route: Delete Movie
    Handles deleting a movie from a user's collection.
    Args:
        user_id (str): User ID.
        movie_id (str): Movie ID.
    Returns:
        "The movie has been deleted successfully" upon successful POST request.
    """
    try:
        if request.method == 'POST':
            if data_manager.delete_movie(user_id, movie_id):
                return "The movie has been deleted successfully"
        else:
            return "Movie not found", 405  # HTTP status code for Method
    except Exception as error:
        # Handle the exception appropriately, e.g., logging, error message, etc.
        return render_template('error.html', error_message=str(error))


if DATA_FILE_PATH.lower().endswith('.sqlite'):
    @app.route('/users/<user_id>/add_review/<movie_id>', methods=['GET', 'POST'])
    def add_review(user_id, movie_id):
        if request.method == 'POST':
            rating = request.form.get('rating')
            review_text = request.form.get('review')
            data_manager.add_review(
                user_id, movie_id, float(rating), review_text)
            return "Review submitted successfully"

        else:
            movies, user = data_manager.get_user_movies(user_id)
            for user_movie, movie in movies:
                if user_movie.movie_id == int(movie_id):
                    movie_title = movie.title
                    # Replace with actual reviews retrieval
                    previous_reviews = data_manager.get_reviews_for_movie(
                        movie_id)

            return render_template('review.html', user_id=user_id,
                                   movie_id=movie_id, movie_title=movie_title,
                                   previous_reviews=previous_reviews)


@app.errorhandler(404)
def page_not_found(e):
    """
    Route: 404 Error Handler
    Handles rendering the 404 page.
    Args:
        e: Error object.
    Returns:
        Rendered HTML template for 404 page.
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
