class TestDecorators:

    # если не прошел декоратор авторизации
    def test_auth_only_decorator(self, test_client):
        headers_to_test = {"Autorization": "Bearer XXX"}
        response = test_client.get("/movies/", headers=headers_to_test)
        assert response.status_code == 401, "Некорректная работа декоратора auth_only"
