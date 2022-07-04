from flask import request, abort
from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from helpers.decorators import admin_required, auth_required
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        try:
            all_users = user_service.get_all()
            res = UserSchema(many=True).dump(all_users)
            return res, 200
        except Exception:
            raise abort(401)

    def post(self):
        req_json = request.json
        user_service.create_user(req_json)
        return "", 201


@user_ns.route('/<int:bid>')
class UserView(Resource):
    def get(self, bid):
        user = user_service.get_one(bid)
        result = UserSchema().dump(user)
        return result, 200

    @auth_required
    @admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)
        return "", 204

    @auth_required
    @admin_required
    def delete(self, bid):
        user_service.delete(bid)
        return "", 204
