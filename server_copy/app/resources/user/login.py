from flask_restful import Resource, abort, reqparse

from app.models.user import User

from flask_jwt_extended import create_access_token


class login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, nullable=False)
    parser.add_argument('password', required=True, nullable=False)

    #from flask import abort
    #from flask_restful import abort

    def put(self):

        data = self.parser.parse_args(strict=True)
        user = User.query.filter_by(username=data.get('username')).scalar()

        if user is None:
            abort(404, error='invalid username')

        if not user.validate_password(data.get('password')):
            abort(404, error='invalid password')

        access_token = create_access_token(user.id)

        return {
            'username': user.username,
            'access_token': access_token
        }