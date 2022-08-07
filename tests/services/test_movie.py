import pytest
from unittest.mock import MagicMock

from app.dao.models.movie import Movie
from app.dao.movie import MovieDAO
from app.service.movie import MovieService


@pytest.fixture()
def movie_dao():
    # создание подменного экземпляра дао, только для фикстуры
    movie_dao = MovieDAO(None)

    # подменные данные для тестирования без сервиса
    movie_1 = Movie(id=1, title="Title_movie_1", description="Description_movie_1", year=2001)
    movie_2 = Movie(id=2, title="Title_movie_2", description="Description_movie_2", year=2002)
    movie_3 = Movie(id=3, title="Title_movie_3", description="Description_movie_3", year=2003)

    # переопределение методов
    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2, movie_3])
    movie_dao.get_with_filter = MagicMock(return_value=movie_1)
    movie_dao.do_post = MagicMock(return_value=Movie(id=4))
    movie_dao.do_update = MagicMock(return_value=Movie(id=4))
    movie_dao.do_delete = MagicMock(return_value="")
    return movie_dao


# сами тесты UserService:

class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.test_movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.test_movie_service.get_one(m_id=1)
        assert movie is not None, "Ошибка тестирования метода get_one (возврат None значения)"
        assert movie.id == 1, "Ошибка тестирования метода get_one (возврат обьекта с неверным id)"

    def test_get_with_filter(self):
        movie = self.test_movie_service.get_with_filter(data={"year": 2001})
        assert movie is not None, "Ошибка тестирования метода get_with_filter (возврат None значения)"
        assert movie.year == 2001, "Ошибка тестирования метода get_with_filter (неверная фильтрация)"

    def test_do_post(self):
        data = {"id": 4, "title": "Title_movie_4", "description": "Description_movie_4", "year": 2004}
        posted_movie = self.test_movie_service.do_post(data=data)
        assert posted_movie is not None, "Ошибка тестирования метода do_post (возврат None значения)"
        assert posted_movie.id == 4, "Ошибка тестирования метода do_post (возвращен неверный id)"

    def test_do_put(self):
        data = {"year": 2005}
        updated_movie = self.test_movie_service.do_put(m_id=4, data=data)
        assert updated_movie is not None, "Ошибка тестирования метода do_put (возврат None значения)"
        assert updated_movie.id == 4, "Ошибка тестирования метода do_put (возвращен неверный id)"

    def test_do_patch(self):
        data = {"year": 2005}
        patched_movie = self.test_movie_service.do_patch(m_id=4, data=data)
        assert patched_movie is not None, "Ошибка тестирования метода do_patch(возврат None значения)"
        assert patched_movie.id == 4, "Ошибка тестирования метода do_patch (возвращен неверный id)"

    def test_delete_one(self):
        result = self.test_movie_service.delete_one(m_id=4)
        assert result is not None, "Ошибка тестирования метода delete_one(возврат None значения)"
        assert result == "", "Ошибка тестирования метода delete_one"
