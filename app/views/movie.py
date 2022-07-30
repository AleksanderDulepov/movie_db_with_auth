from flask import request
from flask_restx import Namespace, Resource
from app.container import movie_service
from app.dao.models.movie import MovieSchema
from app.helper.decorators import auth_only, admin_only

movie_ns=Namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_ns.route("/")
class MoviesView(Resource):
    @auth_only
    def get(self):
        data=request.args
        results = movie_service.get_with_filter(data)
        return movies_schema.dump(results), 200

    @admin_only
    def post(self):
        data = request.json
        results = movie_service.do_post(data)
        if results is not None:
            return "",201
        return "Запись не была добавлена",405


@movie_ns.route("/<int:m_id>")
class MovieView(Resource):
    @auth_only
    def get(self, m_id):
        result=movie_service.get_one(m_id)
        if result is not None:
            return movie_schema.dump(result), 200
        return "Записей с таким id нет в базе",404

    @admin_only
    def put(self, m_id):
        data = request.json
        result = movie_service.do_put(m_id,data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена",405

    @admin_only
    def patch(self, m_id):
        data = request.json
        result = movie_service.do_patch(m_id, data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена", 405

    @admin_only
    def delete(self, m_id):
        result = movie_service.delete_one(m_id)
        if result is not None:
            return "",204
        return "Запись не была удалена", 404
