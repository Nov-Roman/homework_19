import calendar
import datetime
import jwt
from helpers.constants import SECRET_KEY, JWT_ALG


class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_user_by_username(username)

        if not user:
            raise Exception()

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

        data = {
            'username': user.username,
            'role': user.role
        }
        # access токен на 30 минут
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALG)

        # refresh токен на 130 дней
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET_KEY, algorithm=JWT_ALG)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=SECRET_KEY, algorithms=[JWT_ALG])
        username = data['username']
        user = self.user_service.get_user_by_username(username)

        if not user:
            raise Exception()
        return self.generate_tokens(user.username, None, is_refresh=True)
