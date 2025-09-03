from flask import Flask, request, render_template, url_for, redirect
import requests
from models import db, Movie
from data_manager import DataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db' # Choose a name for your database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager() # Create an object of your DataManager class



@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('home.html', users=users)


@app.route("/add_movie/<title>")
def add_movie(title):
    API_KEY = ""
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url).json()
    '''
    Error handling if movie does not exist
    '''
    if response.get("Response") == "False":
        return f"Movie '{title}' not found in OMDb.", 404

    '''
    creating movie object
    '''
    movie = Movie(
        name=response["Title"],
        director=response["Director"],
        year=response["Year"],
        poster_url=response["Poster"],
        user_id = 1
    )
    '''
    save movie
    '''
    data_manager.add_movie(movie)
    return f"{movie.name} successfully added!"


@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get("name")
    if name:
        data_manager.create_user(name)
    return redirect(url_for('home'))


@app.route('/users')
def list_users():
    users = data_manager.get_users()
    return str(users)  # Temporarily returning users as a string


@app.route('/movies/<int:user_id>')
def get_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_movies(user_id):
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    msg = data_manager.delete_movie(movie_id)
    return redirect(url_for('list_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == "GET":
        movies = data_manager.get_movies(user_id)
        return render_template("movies.html", movies=movies, user_id=user_id)
    elif request.method == "POST":
        # add new movie
        title = request.form.get("title")
        # OMDb, create movie
        data_manager.add_movie(movie)
    return redirect(url_for("user_movies", user_id=user_id))


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()