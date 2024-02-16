from flask import Blueprint, current_app, jsonify, request, flash
from sqlalchemy import or_

from dbModels import Posts, Users, Likes
from extensions import bcrypt, db

api = Blueprint("api", __name__)


@api.route("/")
@api.route("/hello")
def hello():
    return "Hello from api"


# Users API
@api.route("/users/registerUser", methods=["POST"])
def create_user():
    """
    Makes a new user with provided json parameters if username and email are unique

    Request JSON:
        {
            "username": "john_doe",

            "email": "john@example.com",

            "password": "secure_password"
        }

    Response:
        201 Created - User created successfully.

        JSON: {"id": 1, "username": "john_doe"}
    """
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
            status = 201
            return jsonify(user.to_dict()), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route("/users/getByUsername", methods=['GET'])
def get_user_by_username():
    try:
        status = 500
        username = request.args.get("username")
        if not username:
            status = 409
            raise Exception("Username missing!")
        with current_app.app_context():
            user = Users.query.filter_by(username=username).first()
            if not user:
                status = 409
                raise Exception("User not found!")
            status = 200
            return jsonify(user.to_dict()), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route("/users/<int:id>", methods=['GET'])
def get_user_by_id(id):
    try:
        status = 500
        if not id:
            status = 409
            raise Exception("ID missing!")
        with current_app.app_context():
            user = Users.query.get(id)
            if not user:
                status = 409
                raise Exception("User not found!")
            status = 200
            return jsonify(user.to_dict()), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route("/users/all")
def get_all_users():
    try:
        status = 500
        with current_app.app_context():
            users = Users.query.order_by(Users.id.asc()).all()
            user_data = [user.to_dict() for user in users]
            status = 200
            return jsonify(user_data), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


# Posts API
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


@api.route('/createLike', methods=["POST"])
def createLike():
    try:
        status = 500
        request_data = request.get_json()
        username = request_data.get("username")
        post_id = request_data.get("postID")
        if not username or not post_id:
            status = 409
            raise Exception("Like parameters missing!")
        with current_app.app_context():
            user = Users.query.filter_by(username=username).first()
            user_id = user.id
            likes = Likes.query.filter_by(user_id=user_id, post_id=post_id).all()
            if likes:
                status = 409
                raise Exception("User already liked that post!")
            new_like = Likes(user_id, post_id)
            db.session.add(new_like)
            db.session.commit()
            print("like created")
            status = 200
            return jsonify({"message": "Like created!"}), status
    except Exception as e:
        return jsonify({'message': str(e)}), status
