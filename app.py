from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload
import os

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from exampleBlueprint.examples import bp
from models import DrugaTabela, PrvaTabela, User, Poke, Base


from flask_mail import Mail

from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)



# sql connection
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://janko:janko@192.168.1.200:3306/testbaza"
from dbModels import db
db.init_app(app)
# Define the SQLAlchemy engine and session

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# Session = sessionmaker(bind=engine)
# Base.metadata.create_all(bind=engine)


# config for file upload
app.config['UPLOAD_FOLDER'] = './uploads/'
# Maximum allowed file size for upload (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB

# config for mail sending using flask_mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mail_username'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# register all blueprints after setting up configurations
app.register_blueprint(bp, url_prefix='/examples')


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
    dbSession = Session()
    if email and password and username:
        user = dbSession.query(User).filter_by(email=email).first()
        if user is not None:
            flash("Email is taken")
            dbSession.close()
            return redirect(url_for('index'))
        user = dbSession.query(User).filter_by(username=username).first()
        if user is not None:
            flash("Username is taken")
            dbSession.close()
            return redirect(url_for('index'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(emailParam=email, passwordParam=hashed_password, usernameParam=username)
        dbSession.add(user)
        dbSession.commit()
        flash("User created")
        session['username'] = username
    dbSession.close()
    return redirect(url_for('index'))


@app.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    dbSession = Session()
    if email and password:
        user = dbSession.query(User).filter_by(email=email).first()
        if user is not None:
            if bcrypt.check_password_hash(user.password, password):
                session['username'] = user.username
            else:
                flash("Username or password are wrong")
        else:
            flash("Username or password are wrong")
    dbSession.close()
    return redirect(url_for('index'))


@app.route('/get_users')
def get_users():
    dbSession = Session()
    users = dbSession.query(User).all()
    user_data = [{'username': user.username} for user in users]
    dbSession.close()
    return jsonify(user_data)


@app.route('/newpoke')
def new_poke():
    with Session() as dbSession:
        users = dbSession.query(User).filter(User.username != session['username']).all()
    return render_template("newpoke.html", users=users)


@app.route('/makepoke/<usernamePoked>')
def create_poke(usernamePoked):
    returnPoke = bool(request.args.get('returnpoke'))
    pokeID = request.args.get('poke')
    print(returnPoke, pokeID)
    pokeID = int(pokeID) if pokeID is not None else None
    dbSession = Session()
    if returnPoke and pokeID:
        stmt = update(Poke).where(Poke.id == pokeID).values(status='N')
        dbSession.execute(stmt)
    userPoked = dbSession.query(User).filter(User.username == usernamePoked).first()
    userPoking = dbSession.query(User).filter(User.username == session['username']).first()
    poke = Poke(userPoking.id, userPoked.id, 'A')
    dbSession.add(poke)
    dbSession.commit()
    dbSession.close()
    if returnPoke:
        return redirect(url_for('my_pokes'))
    return redirect(url_for('index'))


@app.route('/mypokes')
def my_pokes():
    dbSession = Session()
    user = dbSession.query(User).filter(User.username == session['username']).first()
    # using joinedload to eagerly load user1 before closing dbSession
    pokes = dbSession.query(Poke).options(joinedload("user1")).filter(Poke.userPoked == user.id,
                                                                      Poke.status == 'A').all()
    dbSession.close()
    return render_template("mypokes.html", pokes=pokes)


@app.route('/ignorepoke/<int:pokeID>')
def ignore_poke(pokeID):
    dbSession = Session()
    print(pokeID)
    if pokeID:
        stmt = update(Poke).where(Poke.id == pokeID).values(status='N')
        dbSession.execute(stmt)
        dbSession.commit()
    dbSession.close()
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


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.secret_key = "dev"
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
