from flask import Flask
import requests
from models import Movie
from data_manager import DataManager

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to MoviWeb App!"


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
    )
    '''
    save movie
    '''
    dm = DataManager()
    dm.add_movie(movie)
    return f"{movie.name} successfully added!"