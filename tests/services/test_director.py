import pytest
from unittest.mock import MagicMock
from app.dao.director import DirectorDAO
from app.dao.models.director import Director
from app.service.director import DirectorService


@pytest.fixture()
def director_dao():
    # создание подменного экземпляра дао, только для фикстуры
    director_dao = DirectorDAO(None)

    # подменные данные для тестирования без сервиса
    director_1 = Director(id=1, name="Name_director_1")
    director_2 = Director(id=2, name="Name_director_2")
    director_3 = Director(id=3, name="Name_director_3")

    # переопределение методов
    director_dao.get_one = MagicMock(return_value=director_1)
    director_dao.get_all = MagicMock(return_value=[director_1, director_2, director_3])
    director_dao.do_post = MagicMock(return_value=Director(id=4))
    director_dao.do_update = MagicMock(return_value=Director(id=4))
    director_dao.do_delete = MagicMock(return_value="")

    return director_dao


# сами тесты DirectorService:

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.test_director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.test_director_service.get_one(d_id=1)
        assert director is not None, "Ошибка тестирования метода get_one (возврат None значения)"
        assert director.id == 1, "Ошибка тестирования метода get_one (возврат обьекта с неверным id)"

    def test_get_all(self):
        directors = self.test_director_service.get_all()
        assert directors is not None, "Ошибка тестирования метода get_all (возврат None значения)"
        assert len(directors) > 0, "Ошибка тестирования метода get_all (неверное количество возвращаемых обьектов)"

    def test_do_post(self):
        data = {"id": 4, "name": "Name_director_4"}
        posted_director = self.test_director_service.do_post(data=data)
        assert posted_director is not None, "Ошибка тестирования метода do_post (возврат None значения)"
        assert posted_director.id == 4, "Ошибка тестирования метода do_post (возвращен неверный id)"

    def test_do_put(self):
        data = {"name": "Test_name_director_4"}
        updated_director = self.test_director_service.do_put(d_id=4, data=data)
        assert updated_director is not None, "Ошибка тестирования метода do_put (возврат None значения)"
        assert updated_director.id == 4, "Ошибка тестирования метода do_put (возвращен неверный id)"

    def test_do_patch(self):
        data = {"name": "Test_name_director_4"}
        patched_director = self.test_director_service.do_patch(d_id=4, data=data)
        assert patched_director is not None, "Ошибка тестирования метода do_patch(возврат None значения)"
        assert patched_director.id == 4, "Ошибка тестирования метода do_patch (возвращен неверный id)"

    def test_delete_one(self):
        result = self.test_director_service.delete_one(d_id=4)
        assert result is not None, "Ошибка тестирования метода delete_one(возврат None значения)"
        assert result == "", "Ошибка тестирования метода delete_one"
