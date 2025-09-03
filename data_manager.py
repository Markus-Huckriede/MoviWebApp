from models import db, User, Movie


class DataManager:
    def __init__(self):
        pass


    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()


    def get_users(self):
        return User.query.all()


    def get_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()


    def add_movie(self, title, user_id, api_key):
        import requests
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        response = requests.get(url).json()
        if response.get("Response") == "False":
            return None
        movie = Movie(
            name=response["Title"],
            director=response["Director"],
            year=response["Year"],
            poster_url=response["Poster"],
            user_id=user_id
        )
        db.session.add(movie)
        db.session.commit()
        return movie


    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return f"Movie '{new_title}' updated"
        return f"Movie with ID {movie_id} not found"


    def delete_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return f"Movie '{movie.name}' deleted"
        return f"Movie with ID {movie_id} not found"

