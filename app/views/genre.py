from flask import request
from flask_restx import Namespace, Resource
from app.container import genre_sevice
from app.dao.models.genre import GenreSchema
from app.helper.decorators import auth_only, admin_only

genre_ns=Namespace("genres")

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@genre_ns.route("/")
class GenresView(Resource):
    @auth_only
    def get(self):
        results = genre_sevice.get_all()
        return genres_schema.dump(results), 200

    @admin_only
    def post(self):
        data = request.json
        results = genre_sevice.do_post(data)
        if results is not None:
            return "",201
        return "Запись не была добавлена",405


@genre_ns.route("/<int:g_id>")
class GenreView(Resource):
    @auth_only
    def get(self, g_id):
        result=genre_sevice.get_one(g_id)
        if result is not None:
            return genre_schema.dump(result), 200
        return "Записей с таким id нет в базе",404

    @admin_only
    def put(self, g_id):
        data = request.json
        result = genre_sevice.do_put(g_id,data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена",405

    @admin_only
    def patch(self, g_id):
        data = request.json
        result = genre_sevice.do_patch(g_id, data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена", 405

    @admin_only
    def delete(self, g_id):
        result = genre_sevice.delete_one(g_id)
        if result is not None:
            return "",204
        return "Запись не была удалена", 404