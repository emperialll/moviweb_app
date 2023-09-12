import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

    def __repr__(self):
        return self.__str__()


class UserMovies(db.Model):
    __tablename__ = 'favorite_movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    note = Column(String, nullable=False)

    def __str__(self):
        return (
            f"Movies("
            f"movie_id={self.movie_id}, "
            f"user_id={self.user_id}, "
            f"title='{self.title}', "
            f"director='{self.director}', "
            f"year={self.year}, "
            f"rating={self.rating}, "
            f"note='{self.note}'"
            f")"
        )

    def __repr__(self):
        return self.__str__()


class Movies(db.Model):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    genre = Column(String, nullable=False)
    director = Column(String, nullable=False)
    writer = Column(String, nullable=False)
    actors = Column(String, nullable=False)
    plot = Column(String, nullable=False)
    language = Column(String, nullable=False)
    country = Column(String, nullable=False)
    poster = Column(String, nullable=False)
    _type = Column(String, nullable=False)

    def to_dict(self):
        return {
            'movie_id': self.movie_id,
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'genre': self.genre,
            'director': self.director,
            'writer': self.writer,
            'actors': self.actors,
            'plot': self.plot,
            'language': self.language,
            'country': self.country,
            'poster': self.poster,
            '_type': self._type
        }

    def __str__(self):
        return (
            f"Movies("
            f"movie_id={self.movie_id}, "
            f"title='{self.title}', "
            f"year={self.year}, "
            f"rating={self.rating}, "
            f"genre='{self.genre}', "
            f"director='{self.director}', "
            f"writer='{self.writer}', "
            f"actors='{self.actors}', "
            f"plot='{self.plot}', "
            f"language='{self.language}', "
            f"country='{self.country}', "
            f"poster='{self.poster}', "
            f"type='{self._type}', "
            f")"
        )

    def __repr__(self):
        return self.__str__()


class Reviews(db.Model):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    review_text = Column(Text)
    rating = Column(Float)

    def __str__(self):
        return f"Review {self.review_id} for Movie {self.movie_id}, \
            User {self.user_id}: {self.review_text}"

    def __repr__(self):
        return f"<Review(review_id={self.review_id}, movie_id={self.movie_id},\
             user_id={self.user_id}, rating={self.rating})>"

######################## This section is being used only for table creation ####################
################################################################################################
################################################################################################

# important Note: To create tables uncomment below and comment out db.init_app(app) in SQLDataManager.py

# if __name__ == '__main__':
#     parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     # Add the parent directory to sys.path
#     sys.path.insert(0, parent_dir)
#     # Create the new tables
#     from app import app
#     with app.app_context():
#         db.init_app(app)
#         db.create_all()
