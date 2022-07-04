from flask import abort
from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_username(self, val: str):
        return self.session.query(User).filter(User.username == val).first()

    def get_user_admin(self, val: str, filters):
        try:
            u = self.session.query(User).get(val)
            if "role" in filters:
                u = u.filter(User.role == filters.get("admin"))
            elif "role" in filters:
                u = u.filter(User.role == filters.get("user"))
            return u.all()
        except Exception as e:
            print("User roles Exception", e)
            raise abort(401)

    def create_user(self, user):
        user_ent = User(**user)
        self.session.add(user_ent)
        self.session.commit()
        return user_ent

    def delete(self, bid):
        user = self.get_one(bid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()
