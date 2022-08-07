import pytest
from main import create_app, configure_app
from app.config import Config_for_test


# #фикстура для тестирования вьюх
@pytest.fixture()
def app():
    app_config = Config_for_test()
    app = create_app(app_config)  # вызов функции создания и настройки приложения Flask
    configure_app(app)  # вызов функции конфигурирования приложения с БД, APi
    yield app


@pytest.fixture()
def test_client(app):
    return app.test_client()
