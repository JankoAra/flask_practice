from flask import Blueprint, current_app, jsonify

from dbModels import Posts

api = Blueprint("api", __name__)


@api.route("/")
@api.route("/hello")
def hello():
    return "Hello from api"


@api.route("/getAllPosts")
def getAllPosts():
    with current_app.app_context():
        posts = Posts.query.order_by(Posts.datetime.desc(), Posts.id.desc()).limit(8).all()
        post_data = [
            {'id': post.id, 'content': post.content, 'authorUsername': post.author.username, 'datetime': post.datetime}
            for post in posts]
    return jsonify(post_data)
