import jwt
from flask import request
from flask_restx import abort

from app.helper.constants import JWT_SECRET, JWT_ALGORITHM


def auth_only(func):
    def wrapper(*args, **kwargs):
        # проверка наличия заголовка в запросе
        if "Autorization" not in request.headers:
            abort(401)

        data = request.headers["Autorization"]
        token = data.split("Bearer ")[-1]  # вычленение самого токена из заголовка

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            print(e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_only(func):
    def wrapper(*args, **kwargs):
        # проверка наличия заголовка в запросе
        if "Autorization" not in request.headers:
            abort(401)

        data = request.headers["Autorization"]
        token = data.split("Bearer ")[-1]  # вычленение самого токена из заголовка
        role = None

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            # извлечение роли role из payload части раскодированного токена
            role = user.get("role", "user")  # если роль не была зашифрована в токене, будет обычным юзером
        except Exception as e:
            print(e)
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
