"""
SQL BRANCH
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

# from data_management.JSONDataManager import JSONDataManager
# from data_management.CSVDataManager import CSVDataManager
import requests
import json
from flask import Flask, render_template, request
from data_management.SQL_Data_Models import db, User, Movies
import os
import sys

# OMDB API to get movie data
API: str = 'http://www.omdbapi.com/?apikey=6f0c3bf6&t='

# Get the directory containing app.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory of current_dir (project_root) to sys.path
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


app = Flask(__name__)

# Setting the database URI
db_path = os.path.abspath('user_data/user_movies.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Initialize the SQLAlchemy extension with the Flask application
db.init_app(app)


#######################   JSON / CSV   ########################
###############################################################
###############################################################

# Use the appropriate path to your JSON or CSV file

# DATA_FILE_PATH = "user_data/users.json"
# data_manager = JSONDataManager(DATA_FILE_PATH)

# DATA_FILE_PATH = "user_data/users.csv"
# data_manager = CSVDataManager(DATA_FILE_PATH)

##############################################################


@app.route('/')
def home():
    """
    Route: Home
    Renders the homepage template.
    Returns:
        Rendered HTML template.
    """
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
    Route: List Users
    Retrieves a list of users and renders the users template.
    Returns:
        Rendered HTML template with user data.
    """
    # Fetch the list of users from the database
    users = User.query.all()
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
        users = User.query.all()
        movies = Movies.query.all()
        user_favorite_movies = []
        for movie in movies:
            if movie.user_id == int(user_id):
                user_favorite_movies.append(movie)
        for user in users:
            if user.id == int(user_id):
                name = user.name
        return render_template('movies.html', movies=user_favorite_movies,
                               name=name,
                               id=user_id)
    except Exception as error:
        # Handle the exception appropriately, e.g., logging, error message, etc.
        return render_template('error.html', error_message=str(error))


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
        # Create a new User object with the form data
        new_user = User(name=name, email=email)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        return "The author has been added successfully!"

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
        title = request.form.get('name')

        response = requests.get(API + title)
        response.raise_for_status()
        movie_dict_data = json.loads(response.text)
        if movie_dict_data['Response'] == 'False':
            return "Movie not found!"
        else:
            # Create a new movie object with the form data
            new_movie = Movies(user_id=user_id,
                               title=movie_dict_data['Title'],
                               director=movie_dict_data['Director'],
                               year=movie_dict_data['Year'],
                               rating=movie_dict_data['imdbRating'],
                               note="")

        # Add the user to the database
        db.session.add(new_movie)
        db.session.commit()
        return "Movie has been added successfully!"

    return render_template('add-movie.html', user_id=user_id)


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
        movie = Movies.query.filter_by(
            movie_id=movie_id, user_id=user_id).first()
        if movie:
            if request.method == 'POST':
                movie.title = request.form.get('name')
                movie.director = request.form.get('director')
                movie.rating = request.form.get('rating')
                movie.year = request.form.get('year')
                movie.note = request.form.get('note')

                # Update database
                db.session.commit()

                return "Movie has been updated successfully!"

            return render_template('update-movie.html',
                                   user_id=user_id,
                                   movie_id=movie_id,
                                   movie_title=movie.title,
                                   movie_rating=movie.rating,
                                   movie_director=movie.director,
                                   movie_year=movie.year,
                                   movie_note=movie.note)
        else:
            return "Movie not found"
    except Exception as error:
        # Handle the exception appropriately, e.g., logging, error message, etc.
        return render_template('error.html', error_message=str(error))


# @app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
# def delete_movie(user_id, movie_id):
#     """
#     Route: Delete Movie
#     Handles deleting a movie from a user's collection.
#     Args:
#         user_id (str): User ID.
#         movie_id (str): Movie ID.
#     Returns:
#         "The movie has been deleted successfully" upon successful POST request.
#     """
#     try:
#         if request.method == 'POST':
#             data_manager.delete_movie(user_id, movie_id)
#             return "The movie has been deleted successfully"
#     except Exception as error:
#         # Handle the exception appropriately, e.g., logging, error message, etc.
#         return render_template('error.html', error_message=str(error))


# @app.errorhandler(404)
# def page_not_found(e):
#     """
#     Route: 404 Error Handler
#     Handles rendering the 404 page.
#     Args:
#         e: Error object.
#     Returns:
#         Rendered HTML template for 404 page.
#     """
#     return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
