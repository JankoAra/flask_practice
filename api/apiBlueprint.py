from flask import Blueprint, current_app, jsonify, request, flash
from sqlalchemy import or_

from dbModels import Posts, Users
from extensions import bcrypt, db

api = Blueprint("api", __name__)


@api.route("/")
@api.route("/hello")
def hello():
    return "Hello from api"


@api.route("/getPosts")
def getPosts():
    with current_app.app_context():
        limit = request.args.get("limit")
        if limit is not None and limit != "undefined":
            limit = int(limit)
            posts = Posts.query.order_by(Posts.datetime.desc(), Posts.id.desc()).limit(limit).all()
        else:
            posts = Posts.query.order_by(Posts.datetime.desc(), Posts.id.desc()).all()
        post_data = [post.to_dict() for post in posts]
    return jsonify(post_data)


@api.route("/registerUser", methods=["POST"])
def registerUser():
    try:
        status = 500
        request_data = request.get_json()
        username = request_data.get("username")
        email = request_data.get("email")
        password = request_data.get("password")
        if not username or not email or not password:
            status = 409
            raise Exception("Register parameters missing!")
        with current_app.app_context():
            # check for users with same email or username
            users = Users.query.filter(or_(Users.username == username, Users.email == email)).all()
            if users:
                status = 409
                raise Exception("Username or email are taken!")
            # hash password and create a new user
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = Users(emailParam=email, passwordParam=hashed_password, usernameParam=username)
            db.session.add(user)
            db.session.commit()
            flash("User created!")
            status = 200
            return jsonify({"message": "User created!"}), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route("/getAllUsers")
def getAllUsers():
    with current_app.app_context():
        users = Users.query.order_by(Users.id.asc()).all()
        user_data = [user.to_dict() for user in users]
        return jsonify(user_data)