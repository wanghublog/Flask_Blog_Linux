from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import abort, current_app
from flask_restful import Resource

from wanghublog.controllers.flask_restful import parsers
from wanghublog.models import User

#为验证通过的用户创建token
class AuthApi(Resource):
    """Restful api of Auth."""

    def post(self):
        """Can be execute when receive HTTP Method `POST`."""

        args = parsers.user_post_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()

        # Check the args['password'] whether as same as user.password.
        if user.check_password(args['password']):
            # serializer object will be saved the token period of time.
            print('密码验证通过')
            serializer = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=600)#有效时间
            
            return {'token': str(serializer.dumps({'id':user.id}))}
        else:
            abort(401)


