from datetime import datetime

from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import mysql.connector
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import os

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from models import PrvaTabela, DrugaTabela, User, Poke

from flask_mail import Mail, Message

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://janko:janko@192.168.1.200:3306/prvaBaza"
# app.config['HOST_ADDRESS'] = '192.168.1.3'
# app.config['PORT'] = '80'
app.config['UPLOAD_FOLDER'] = './uploads/'
# Maximum allowed file size for upload (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sender@mail'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Define the SQLAlchemy engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)


@app.route("/mail")
def send_mail():
    msg = Message('Hello', sender=app.config['MAIL_USERNAME'], recipients=['receiver@mail'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


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
            return redirect(url_for('index'))
        user = dbSession.query(User).filter_by(username=username).first()
        if user is not None:
            flash("Username is taken")
            return redirect(url_for('index'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(emailParam=email, passwordParam=hashed_password, usernameParam=username)
        dbSession.add(user)
        dbSession.commit()
        flash("User created")
        session['username'] = username
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
    return redirect(url_for('index'))


@app.route('/get_users')
def get_users():
    dbSession = Session()
    users = dbSession.query(User).all()
    user_data = [{'username': user.username} for user in users]
    return jsonify(user_data)


@app.route('/newpoke')
def new_poke():
    dbSession = Session()
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
    if returnPoke:
        return redirect(url_for('my_pokes'))
    return redirect(url_for('index'))


@app.route('/mypokes')
def my_pokes():
    dbSession = Session()
    user = dbSession.query(User).filter(User.username == session['username']).first()
    pokes = dbSession.query(Poke).filter(Poke.userPoked == user.id, Poke.status == 'A').all()
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        os.makedirs('uploads', exist_ok=True)
        f.save(path)
        flash("file uploaded")
    return redirect(url_for('index'))


@app.route("/email", methods=["POST", "GET"])
def email_creation():
    sessionDatabase = Session()
    # dohvatanje query parametara po imenu
    email = request.args.get("email")
    if request.method == "POST":
        # dohvatanje form parametara u vidu key-value
        # request.form['key']
        email = request.form['email']
    if email:
        session["username"] = email
        allEmails = sessionDatabase.query(DrugaTabela.email).all()
        allEmails = [allEmails[i][0] for i in range(len(allEmails))]
        # print(allEmails)
        if email not in allEmails:
            novi = DrugaTabela(email)
            sessionDatabase.add(novi)
            sessionDatabase.commit()
        else:
            return "Korisnik vec postoji"
    sessionDatabase.close()
    return "kreiran korisnik" if email else "nema email-a"


# alternativni nacin za dodelu rute nekoj funkciji
# app.add_url_rule('/','hello',hello)
@app.route('/')
def index():
    return render_template("index.html")


# path params
@app.route('/hello/<name>')
def hello_name(name):
    return render_template("hello.html", name=name)


# path params kastovan (int, float, path)
@app.route('/sum/<int:num1>/<int:num2>')
def sum(num1, num2):
    return "%d" % (num1 + num2)


# redirektovanje i otkrivanje url-a za neku funkciju
@app.route("/inc/<int:num>")
def inc(num):
    return redirect(location=url_for("sum", num1=num, num2=1), code=302)


@app.route("/cheer/<name>")
def cheer(name):
    return render_template("cheerleaders.html", name=name)


@app.route('/baza')
def ping():
    name = request.args.get("name")
    mydb = mysql.connector.connect(host="192.168.1.200", port=3306, user="janko", password="janko", database="prvaBaza")
    cursor = mydb.cursor()
    if name:
        cursor.execute("insert into prvaTabela(ime, broj) values(%s, 101)", (name,))
    mydb.commit()
    cursor.execute("select * from prvaTabela")
    resultList = cursor.fetchall()
    for x in resultList:
        print(x)
    mydb.close()
    return f'name={name}' if name else "Nema imena"


@app.route("/sqla")
def sqla():
    session = Session()
    name = request.args.get("name")
    if name:
        novi = PrvaTabela(name, 120, "blabla")
        session.add(novi)
        session.commit()
    session.close()
    return "kreiran korisnik" if name else "nema parametaraa"


@app.route("/content")
def contentPage():
    if "username" in session:
        # postoji ime u sesiji, korisnik je ulogovan
        return render_template("logged.html")
    else:
        return render_template("notLogged.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.secret_key = "dev"
    app.run(host="0.0.0.0", port=5000, debug=True)
