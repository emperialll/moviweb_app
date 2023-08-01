from flask import Flask, render_template, request
from data_management.JSONDataManager import JSONDataManager
from data_management.CSVDataManager import CSVDataManager

app = Flask(__name__)

data_file_path = "user_data/users.csv"
# Use the appropriate path to your JSON or CSV file
# data_manager = JSONDataManager(data_file_path)
data_manager = CSVDataManager(data_file_path)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def my_movies(user_id):
    users = data_manager.get_all_users()
    if user_id in users.keys():
        user_name = users[user_id]["name"]
        user_movies = data_manager.get_user_movies(user_id)
        return render_template('movies.html', movies=user_movies,
                               user_name=user_name,
                               user_id=user_id)
    else:
        return render_template('304.html')

if data_file_path.lower().endswith('.json'):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            user_details = {"name": name, "movies": {}}
            data_manager.add_user(user_details)
            return "Registration successful!"

            # Render the registration form template for GET requests
        return render_template('register.html')
elif data_file_path.lower().endswith('.csv'):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            data_manager.add_user(name)
            return "Registration successful!"

            # Render the registration form template for GET requests
        return render_template('register.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movies(user_id):
    if request.method == 'POST':
        movie_title = request.form.get('name')
        if data_manager.add_movie(user_id, movie_title) is False:
            return "Movie not found!"
        return "Movie has been added successfully!"

        # Render the registration form template for GET requests
    return render_template('add-movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movies(user_id, movie_id):
    movies = data_manager.get_user_movies(user_id)
    movie = movies[movie_id]
    if request.method == 'POST':
        movie_title = request.form.get('name')
        movie_director = request.form.get('director')
        movie_rating = request.form.get('rating')
        movie_year = request.form.get('year')
        movie_note = request.form.get('note')
        data_manager.update_movie(user_id, movie_id, movie_title,
                                  movie_director, movie_rating, movie_year, movie_note)
        return "Movie has been updated successfully!"

        # Render the registration form template for GET requests
    return render_template('update-movie.html',
                           user_id=user_id,
                           movie_id=movie_id,
                           movie_title=movie['name'],
                           movie_rating=movie['rating'],
                           movie_director=movie['director'],
                           movie_year=movie['year'],
                           movie_note=movie['note'])


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    if request.method == 'POST':
        data_manager.delete_movie(user_id, movie_id)
        return "The movie has been deleted successfully"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
