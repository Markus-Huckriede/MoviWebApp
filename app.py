from flask import Flask, request, render_template, redirect, url_for
from models import db, User, Movie
from data_manager import DataManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def add_user():
    name = request.form.get("name")
    if name:
        data_manager.create_user(name)
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    if request.method == "POST":
        title = request.form.get("title")
        if title:
            # Add Movie via OMDb API
            movie = data_manager.add_movie(title=title, user_id=user_id)
            if movie is None:
                return f"Movie '{title}' not found.", 404
        return redirect(url_for("user_movies", user_id=user_id))

    # GET request -> Filme laden
    movies = data_manager.get_movies(user_id)
    return render_template("movies.html", movies=movies, user_id=user_id)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)