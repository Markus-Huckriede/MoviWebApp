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

    def add_movie(self, movie):
        new_movie = Movie(
            name=name,
            director=director,
            year=year,
            poster_url=poster_url,
            user_id=user_id
        )
        db.session.add(new_movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.name = new_title
            db.session.commit()
            return f"Movie '{new_title}' updated"
        return f"Movie with ID {movie_id} not found"

    def delete_movie(self, movie_id):
        pass