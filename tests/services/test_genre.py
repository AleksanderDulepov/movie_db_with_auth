import pytest
from unittest.mock import MagicMock
from app.dao.genre import GenreDAO
from app.dao.models.genre import Genre
from app.service.genre import GenreService


@pytest.fixture()
def genre_dao():
    # создание подменного экземпляра дао, только для фикстуры
    genre_dao = GenreDAO(None)

    # подменные данные для тестирования без сервиса
    genre_1 = Genre(id=1, name="Name_genre_1")
    genre_2 = Genre(id=2, name="Name_genre_2")
    genre_3 = Genre(id=3, name="Name_genre_3")

    # переопределение методов
    genre_dao.get_one = MagicMock(return_value=genre_1)
    genre_dao.get_all = MagicMock(return_value=[genre_1, genre_2, genre_3])
    genre_dao.do_post = MagicMock(return_value=Genre(id=4))
    genre_dao.do_update = MagicMock(return_value=Genre(id=4))
    genre_dao.do_delete = MagicMock(return_value="")

    return genre_dao


# сами тесты GenreService:

class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.test_genre_service = GenreService(dao=genre_dao)

    # self.test_genre_service это и есть наш GenreService с подмененным dao (тестим его методы)

    def test_get_one(self):
        genre = self.test_genre_service.get_one(g_id=1)
        assert genre is not None, "Ошибка тестирования метода get_one (возврат None значения)"
        assert genre.id == 1, "Ошибка тестирования метода get_one (возврат обьекта с неверным id)"

    def test_get_all(self):
        genres = self.test_genre_service.get_all()
        assert genres is not None, "Ошибка тестирования метода get_all (возврат None значения)"
        assert len(genres) > 0, "Ошибка тестирования метода get_all (неверное количество возвращаемых обьектов)"

    def test_do_post(self):
        data = {"id": 4, "name": "Name_genre_4"}
        posted_genre = self.test_genre_service.do_post(data=data)
        assert posted_genre is not None, "Ошибка тестирования метода do_post (возврат None значения)"
        assert posted_genre.id == 4, "Ошибка тестирования метода do_post (возвращен неверный id)"

    def test_do_put(self):
        data = {"name": "Test_name_director_4"}
        updated_genre = self.test_genre_service.do_put(g_id=4, data=data)
        assert updated_genre is not None, "Ошибка тестирования метода do_put (возврат None значения)"
        assert updated_genre.id == 4, "Ошибка тестирования метода do_put (возвращен неверный id)"

    def test_do_patch(self):
        data = {"name": "Test_name_genre_4"}
        patched_genre = self.test_genre_service.do_patch(g_id=4, data=data)
        assert patched_genre is not None, "Ошибка тестирования метода do_patch(возврат None значения)"
        assert patched_genre.id == 4, "Ошибка тестирования метода do_patch (возвращен неверный id)"

    def test_delete_one(self):
        result = self.test_genre_service.delete_one(g_id=4)
        assert result is not None, "Ошибка тестирования метода delete_one(возврат None значения)"
        assert result == "", "Ошибка тестирования метода delete_one"
