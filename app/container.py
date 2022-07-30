from app.dao.director import DirectorDAO
from app.dao.genre import GenreDAO
from app.dao.movie import MovieDAO
from app.dao.user import UserDAO
from app.database import db
from app.service.auth import AuthService
from app.service.director import DirectorService
from app.service.genre import GenreService
from app.service.movie import MovieService
from app.service.user import UserService

movie_dao = MovieDAO(db.session)
movie_service = MovieService(movie_dao)

director_dao = DirectorDAO(db.session)
director_sevice = DirectorService(director_dao)

genre_dao = GenreDAO(db.session)
genre_sevice = GenreService(genre_dao)

user_dao = UserDAO(db.session)
user_service = UserService(user_dao)

auth_service = AuthService(user_service)
