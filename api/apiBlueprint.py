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
@api.route("/users/register", methods=["POST"])
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
            status = 400
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


@api.route("/users/getByUsername/<username>", methods=['GET'])
def get_user_by_username(username):
    try:
        status = 500
        # username = request.args.get("username")
        if not username:
            status = 400
            raise Exception("Username missing!")
        with current_app.app_context():
            user = Users.query.filter_by(username=username).first()
            if not user:
                status = 404
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
            status = 400
            raise Exception("ID missing!")
        with current_app.app_context():
            user = Users.query.get(id)
            if not user:
                status = 404
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
@api.route("/posts/all", methods=["GET"])
def get_all_posts():
    status = 500
    try:
        with current_app.app_context():
            limit = request.args.get("limit")
            if limit is not None and limit != "undefined":
                limit = int(limit)
                posts = Posts.query.order_by(Posts.datetime.desc(), Posts.id.desc()).limit(limit).all()
            else:
                posts = Posts.query.order_by(Posts.datetime.desc(), Posts.id.desc()).all()
            post_data = [post.to_dict() for post in posts]
            return jsonify(post_data), 200
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route("/posts/<username>", methods=["GET"])
def get_all_posts_for_username(username):
    status = 500
    try:
        with current_app.app_context():
            user = Users.query.filter_by(username=username).first()
            posts = Posts.query.filter_by(author_id=user.id).order_by(Posts.datetime.desc(),
                                                                      Posts.id.desc()).all()
            post_data = [post.to_dict() for post in posts]
            return jsonify(post_data), 200
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route('/posts/new', methods=["POST"])
def create_post():
    """
        Makes a new post for a user

        Request JSON:
            {
                "username": "john_doe",

                "content": "This is some post content"
            }

        Response:
            201 Created - Post created successfully.

            JSON: {
                "id": "1",

                "content": "This is some post content",

                "author": {"id""1", "username":"john_doe"},

                "datetime": "Thu, 15 Feb 2024 23:09:57 GMT"
            }
        """
    status = 500
    try:
        data = request.get_json()
        username = data.get("username")
        content = data.get("content")
        if not username or not content:
            status = 400
            raise Exception('Parameters missing!')
        user = Users.query.filter_by(username=username).first()
        if not user:
            status = 404
            raise Exception('User doesn\'t exist!')
        post = Posts(user.id, content)
        db.session.add(post)
        db.session.commit()
        status = 201
        return jsonify(post.to_dict()), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


@api.route("/posts/delete", methods=["DELETE"])
def delete_post():
    status = 500
    try:
        data = request.get_json()
        username = data.get("username")
        postID = data.get("postID")
        if not username or not postID:
            status = 400
            raise Exception('Parameters missing!')
        user = Users.query.filter_by(username=username).first()
        if not user:
            status = 404
            raise Exception('User doesn\'t exist!')
        post = Posts.query.filter_by(id=postID).first()
        if not post:
            status = 404
            raise Exception('Post doesn\'t exist!')
        if post.author_id != user.id:
            status = 403
            raise Exception('User is not the author of the post!')
        likes = Likes.query.filter_by(post_id=postID).all()
        for like in likes:
            db.session.delete(like)
        db.session.delete(post)
        db.session.commit()
        status = 200
        return jsonify({"message": "Post deleted!"}), status
    except Exception as e:
        flash(str(e))
        return jsonify({'message': str(e)}), status


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
