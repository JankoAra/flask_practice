import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_from_directory
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from api.apiBlueprint import api
from dbModels import Users, Pokes, Posts
from exampleBlueprint.examples import bp
from extensions import bcrypt, db, cors

app = Flask(__name__)
cors.init_app(app)
bcrypt.init_app(app)

# sql connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://janko:janko@192.168.1.200:3306/flasktest"

db.init_app(app)

# config for file upload
app.config['UPLOAD_FOLDER'] = './uploads/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
# Maximum allowed file size for upload (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# from flask_mail import Mail
# config for mail sending using flask_mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'mail_username'
# app.config['MAIL_PASSWORD'] = 'password'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# mail = Mail(app)

# register all blueprints after setting up configurations
app.register_blueprint(bp, url_prefix='/examples')
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/form/<action>')
def form(action):
    if action == "register":
        return render_template("register_form.html")
    elif action == "login":
        return render_template("login_form.html")
    elif action == "uploadfile":
        return render_template("upload_file.html")
    return "greska"


@app.route('/session/username/<username>', methods=["POST"])
def set_session_username(username):
    session["username"] = username
    return redirect(url_for("index"))


@app.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    with app.app_context():
        if email and password:
            user = Users.query.filter_by(email=email).first()
            if user is not None:
                if bcrypt.check_password_hash(user.password, password):
                    session['username'] = user.username
                else:
                    flash("Username or password are wrong")
            else:
                flash("Username or password are wrong")
    return redirect(url_for('index'))


@app.route('/newpoke')
def new_poke():
    return render_template("newpoke.html")


@app.route('/mypokes')
def my_pokes():
    return render_template("mypokes.html")


def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def allowed_file(filename):
    # print(filename.rsplit('.', 1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload-img', methods=["POST"])
def upload_img():
    # current_directory = os.getcwd()
    # print("Current Directory:", current_directory)
    # print("App root path:", app.root_path)
    if request.content_length > app.config['MAX_CONTENT_LENGTH']:
        flash('File size exceeds the allowed limit')
        return redirect(url_for('index'))
    f = request.files['file']
    if not allowed_file(f.filename):
        flash("Unsupported file type")
        return redirect(url_for('index'))
    if f:
        timestamp = get_timestamp()
        filename = f"{timestamp}_{secure_filename(f.filename)}"
        upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
        path = os.path.join(upload_folder, secure_filename(filename))
        # print("image path:", path)
        f.save(path)
        flash("file uploaded")
        return render_template("display_image.html", img_filename=filename)
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.secret_key = "dev"
    # with app.app_context():
    #     db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
