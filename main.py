from flask import Flask
from flask_restx import Api
from app.config import Config
from app.dao.models.director import Director
from app.dao.models.genre import Genre
from app.dao.models.movie import Movie
from app.dao.models.user import User
from app.database import db
from app.views.auth import auth_ns
from app.views.director import director_ns
from app.views.genre import genre_ns
from app.views.movie import movie_ns
import json

from app.views.user import user_ns


def create_app(config):
    # создание приложения
    application = Flask(__name__)
    # конфиги

    application.config.from_object(config)  # (конфигурация загружается из обьекта)
    application.app_context().push()  # применение загруженных конфигов

    return application


def configure_app(application_):
    db.init_app(application_)  # конфигурирование приложения в БД

    api = Api(application_)  # конфигурирование приложения в Api
    # регистрируем неймспейсы, ака блюпринты
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


def create_db():
    db.drop_all()
    db.create_all()

    with open("data/movies.json", "r", encoding="utf-8") as file:
        data_movies = json.load(file)
        objects_movies = [Movie(**i) for i in data_movies]

    db.session.add_all(objects_movies)
    # заполнение таблицы director
    with open("data/directors.json", "r", encoding="utf-8") as file:
        data_directors = json.load(file)
        objects_directors = [Director(**i) for i in data_directors]

    db.session.add_all(objects_directors)
    # заполнение таблицы genre
    with open("data/genres.json", "r", encoding="utf-8") as file:
        data_genres = json.load(file)
        objects_genres = [Genre(**i) for i in data_genres]

    db.session.add_all(objects_genres)
    # заполнение таблицы user
    with open("data/users.json", "r", encoding="utf-8") as file:
        data_users = json.load(file)
        objects_users = [User(**i) for i in data_users]

    db.session.add_all(objects_users)

    db.session.commit()


if __name__ == '__main__':
    app_config = Config()  # создание обьекта класса Config
    app = create_app(app_config)  # вызов функции создания и настройки приложения Flask
    configure_app(app)  # вызов функции конфигурирования приложения с БД, APi
    create_db()  # создание и наполнение БД данными из json
    app.run()
