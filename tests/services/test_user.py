import pytest
from unittest.mock import MagicMock

from app.dao.models.user import User
from app.dao.user import UserDAO
from app.service.user import UserService


@pytest.fixture()
def user_dao():
    # создание подменного экземпляра дао, только для фикстуры
    user_dao = UserDAO(None)

    # подменные данные для тестирования без сервиса
    user_1 = User(id=1, username="Username_1", password="Password_user_1", role="user")
    user_2 = User(id=2, username="Username_2", password="Password_user_2", role="user")
    user_3 = User(id=3, username="Username_3", password="Password_user_3", role="admin")

    # переопределение методов
    user_dao.get_one = MagicMock(return_value=user_1)
    user_dao.get_all = MagicMock(return_value=[user_1, user_2, user_3])
    user_dao.get_by_username = MagicMock(return_value=user_1)
    user_dao.do_post = MagicMock(return_value=User(id=4))
    user_dao.do_update = MagicMock(return_value=User(id=4))
    user_dao.do_delete = MagicMock(return_value="")
    return user_dao


# сами тесты UserService:

class TestUserService:
    @pytest.fixture(autouse=True)
    def user_service(self, user_dao):
        self.test_user_service = UserService(dao=user_dao)

    def test_get_one(self):
        user = self.test_user_service.get_one(u_id=1)
        assert user is not None, "Ошибка тестирования метода get_one (возврат None значения)"
        assert user.id == 1, "Ошибка тестирования метода get_one (возврат обьекта с неверным id)"

    def test_get_all(self):
        users = self.test_user_service.get_all()
        assert users is not None, "Ошибка тестирования метода get_with_filter (возврат None значения)"
        assert len(users) == 3, "Ошибка тестирования метода get_all (неверное кол-во)"

    def test_get_by_username(self):
        user = self.test_user_service.get_by_username(username="Username_1")
        assert user is not None, "Ошибка тестирования метода get_by_username (возврат None значения)"
        assert user.id == 1, "Ошибка тестирования метода get_by_username (возврат обьекта с неверным id)"

    def test_do_post(self):
        data = {"id": 4, "username": "Username_4", "password": "Password_user_4", "role": "user"}
        posted_user = self.test_user_service.do_post(data=data)
        assert posted_user is not None, "Ошибка тестирования метода do_post (возврат None значения)"
        assert posted_user.id == 4, "Ошибка тестирования метода do_post (возвращен неверный id)"

    def test_do_put(self):
        data = {"role": "user"}
        updated_user = self.test_user_service.do_put(u_id=4, data=data)
        assert updated_user is not None, "Ошибка тестирования метода do_put (возврат None значения)"
        assert updated_user.id == 4, "Ошибка тестирования метода do_put (возвращен неверный id)"

    def test_do_patch(self):
        data = {"role": "user"}
        patched_user = self.test_user_service.do_patch(u_id=4, data=data)
        assert patched_user is not None, "Ошибка тестирования метода do_patch(возврат None значения)"
        assert patched_user.id == 4, "Ошибка тестирования метода do_patch (возвращен неверный id)"

    def test_delete_one(self):
        result = self.test_user_service.delete_one(u_id=4)
        assert result is not None, "Ошибка тестирования метода delete_one(возврат None значения)"
        assert result == "", "Ошибка тестирования метода delete_one"

    def test_make_user_password_hash(self):
        password = self.test_user_service.make_user_password_hash(password="1111")
        assert password is not None, "Ошибка тестирования метода make_user_password_hash(возврат None значения)"
        assert password == b"8Ke7O806hWE6zYp4LZiXD5JLWx6FOGKEg3L0T9PYGz0=", "Ошибка тестирования метода " \
                                                                            "make_user_password_hash (неверный пароль)"

    def test_compare_password(self):
        is_matched = self.test_user_service.compare_password(
            hash_password_from_db="8Ke7O806hWE6zYp4LZiXD5JLWx6FOGKEg3L0T9PYGz0=", client_input_password="1111")
        assert is_matched, "Ошибка тестирования метода compare_password (пароли не совпадают)"
