from config import API_KEY
from flask import Flask, request, render_template, url_for, redirect
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
    return render_template('index.html', users=users)


@app.route("/add_movie/<title>")
def add_movie(title):
    API_KEY = ""
    # DataManager -> OMDb and create Movie
    movie = data_manager.add_movie(title=title, user_id=1, api_key=API_KEY)

    if movie is None:
        return f"Movie '{title}' mot found.", 404

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
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == "GET":
        try:
            movies = data_manager.get_movies(user_id)
        except Exception as e:
            return f"Loading movie failed: {e}", 500
        return render_template("movies.html", movies=movies, user_id=user_id)

    elif request.method == "POST":
        title = request.form.get("title")
        if title:
            API_KEY = ""
            try:
                data_manager.add_movie(title=title, user_id=user_id, api_key=API_KEY)
            except Exception as e:
                return f"Adding movie failed: {e}", 500
    return redirect(url_for("user_movies", user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()