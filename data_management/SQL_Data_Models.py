import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

    def __repr__(self):
        return self.__str__()


class Movies(db.Model):
    __tablename__ = 'favorite_movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
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


if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Add the parent directory to sys.path
    sys.path.insert(0, parent_dir)
    # Create the new tables
    from app import app
    with app.app_context():
        db.create_all()
