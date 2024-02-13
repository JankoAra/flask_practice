import os
from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
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
app.config['UPLOAD_FOLDER'] = './uploads/'
# Maximum allowed file size for upload (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB

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


@app.route('/register', methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    with app.app_context():
        if email and password and username:
            user = Users.query.filter_by(email=email).first()
            if user is not None:
                flash("Email is taken")
                return redirect(url_for('index'))
            user = Users.query.filter_by(username=username).first()
            if user is not None:
                flash("Username is taken")
                return redirect(url_for('index'))
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = Users(emailParam=email, passwordParam=hashed_password, usernameParam=username)
            db.session.add(user)
            db.session.commit()
            flash("User created")
            session['username'] = username
    return redirect(url_for('index'))


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


@app.route('/get_users')
def get_users():
    with app.app_context():
        users = Users.query.all()
        user_data = [{'username': user.username} for user in users]
    return jsonify(user_data)


@app.route('/newpoke')
def new_poke():
    with app.app_context():
        users = Users.query.filter(Users.username != session['username']).all()
    return render_template("newpoke.html", users=users)


@app.route('/makepoke/<usernamePoked>')
def create_poke(usernamePoked):
    returnPoke = bool(request.args.get('returnpoke'))
    pokeID = request.args.get('poke')
    print(returnPoke, pokeID)
    pokeID = int(pokeID) if pokeID is not None else None
    with app.app_context():
        if returnPoke and pokeID:
            stmt = update(Pokes).where(Pokes.id == pokeID).values(status='N')
            db.session.execute(stmt)
        userPoked = Users.query.filter(Users.username == usernamePoked).first()
        userPoking = Users.query.filter(Users.username == session['username']).first()
        poke = Pokes(userPoking.id, userPoked.id, 'A')
        db.session.add(poke)
        db.session.commit()
    if returnPoke:
        return redirect(url_for('my_pokes'))
    return redirect(url_for('index'))


@app.route('/mypokes')
def my_pokes():
    with app.app_context():
        user = Users.query.filter(Users.username == session['username']).first()
        # using joinedload to eagerly load user1 before closing dbSession
        pokes = Pokes.query.options(joinedload(Pokes.user1)).filter(Pokes.userPoked == user.id,
                                                                    Pokes.status == 'A').all()
    return render_template("mypokes.html", pokes=pokes)


@app.route('/ignorepoke/<int:pokeID>')
def ignore_poke(pokeID):
    with app.app_context():
        print(pokeID)
        if pokeID:
            stmt = update(Pokes).where(Pokes.id == pokeID).values(status='N')
            db.session.execute(stmt)
            db.session.commit()
    return redirect(url_for('my_pokes'))


def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


@app.route('/upload-file', methods=["POST"])
def upload_file():
    if request.content_length > app.config['MAX_CONTENT_LENGTH']:
        flash('File size exceeds the allowed limit')
        return redirect(url_for('index'))
    f = request.files['file']
    if f:
        timestamp = get_timestamp()
        filename = f"{timestamp}_{secure_filename(f.filename)}"
        uploads_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
        if not os.path.exists(uploads_folder):
            os.makedirs(uploads_folder, exist_ok=True)
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        f.save(path)
        flash("file uploaded")
    return redirect(url_for('index'))


@app.route('/newpost', methods=['POST'])
def uploadAPost():
    username = session['username']
    content = request.form['postContent']
    print(username, content)
    with app.app_context():
        user = Users.query.filter_by(username=username).first()
        post = Posts(user.id, content)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.secret_key = "dev"
    # with app.app_context():
    #     db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
