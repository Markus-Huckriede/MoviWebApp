from models import db, User, Movie
from config import API_KEY
import requests


class DataManager:
    def __init__(self):
        self.api_key = API_KEY

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        return User.query.all()

    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie(self, user_id, movie_id):
        movie = Movie.query.filter_by(user_id=user_id, id=movie_id).first()
        return movie

    def add_movie(self, title, user_id):
        from urllib.parse import quote
        title = title.strip()
        url = f"http://www.omdbapi.com/?t={quote(title)}&apikey={self.api_key}"
        response = requests.get(url).json()

        if response.get("Response") == "False":
            print(f"OMDb Error: {response.get('Error')}")
            return None

        movie = Movie(
            name=response["Title"],
            director=response["Director"],
            year=response["Year"],
            poster_url=response["Poster"],
            plot=response.get("Plot"),
            user_id=user_id
        )
        db.session.add(movie)
        db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False
