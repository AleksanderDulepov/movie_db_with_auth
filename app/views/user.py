from flask import request
from flask_restx import Namespace, Resource
#from app.container import user_service
from app.container import user_service
from app.dao.models.user import UserSchema

user_ns=Namespace("users")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_ns.route("/")
class UsersView(Resource):
    def get(self):
        data=request.args
        results = user_service.get_all()
        return users_schema.dump(results), 200

    def post(self):
        data = request.json
        results = user_service.do_post(data)
        if results is not None:
            return "",201
        return "Запись не была добавлена",405


@user_ns.route("/<int:u_id>")
class UserView(Resource):
    def get(self, u_id):
        result=user_service.get_one(u_id)
        if result is not None:
            return user_schema.dump(result), 200
        return "Записей с таким id нет в базе",404

    def put(self, u_id):
        data = request.json
        result = user_service.do_put(u_id,data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена",405


    def patch(self, u_id):
        data = request.json
        result = user_service.do_patch(u_id, data)
        if result is not None:
            return "", 204
        return "Запись не была обновлена", 405

    def delete(self, u_id):
        result = user_service.delete_one(u_id)
        if result is not None:
            return "",204
        return "Запись не была удалена", 404
