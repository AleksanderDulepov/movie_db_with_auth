from flask import request
from flask_restx import Namespace, Resource
from app.container import director_sevice
from app.dao.models.director import DirectorSchema
from app.helper.decorators import auth_only, admin_only

director_ns=Namespace("directors")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@director_ns.route("/")
class DirectorsView(Resource):
    @auth_only
    def get(self):
        results = director_sevice.get_all()
        return directors_schema.dump(results), 200

    @admin_only
    def post(self):
        data = request.json
        results = director_sevice.do_post(data)
        if results is not None:
            return "",201
        return "Запись не была добавлена",405


@director_ns.route("/<int:d_id>")
class DirectorView(Resource):
    @auth_only
    def get(self, d_id):
        result=director_sevice.get_one(d_id)
        if result is not None:
            return director_schema.dump(result), 200
        return "Записей с таким id нет в базе",404

    @admin_only
    def put(self, d_id):
        data = request.json
        result = director_sevice.do_put(d_id,data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена",405

    @admin_only
    def patch(self, d_id):
        data = request.json
        result = director_sevice.do_patch(d_id, data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена", 405

    @admin_only
    def delete(self, d_id):
        result = director_sevice.delete_one(d_id)
        if result is not None:
            return "",204
        return "Запись не была удалена", 404