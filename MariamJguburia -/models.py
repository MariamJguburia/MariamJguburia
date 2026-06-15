from sqlalchemy import ForeignKey
from ext import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), default="Guest")

    def password_set(self, password):
        self.password = generate_password_hash(password)

    def password_check(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Place(db.Model, BaseModel):
    __tablename__ = "places"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    known_since = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    image = db.Column(db.String(), default="default_image.jpg")
    flag = db.Column(db.String(), default="default_flag.png")


class Review(db.Model, BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    place_id = db.Column(ForeignKey("places.id"))