from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from models import PrvaTabela, DrugaTabela, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://janko:janko@192.168.1.200:3306/prvaBaza"
app.config['HOST_ADDRESS'] = '192.168.1.3'

# Define the SQLAlchemy engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)


@app.route('/form/<action>')
def form(action):
    if action == "register":
        return render_template("register_form.html", host=app.config['HOST_ADDRESS'])
    elif action == "login":
        return render_template("login_form.html", host=app.config['HOST_ADDRESS'])
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
            return redirect('/')
        user = dbSession.query(User).filter_by(username=username).first()
        if user is not None:
            flash("Username is taken")
            return redirect('/')
        user = User(emailParam=email, passwordParam=password, usernameParam=username)
        dbSession.add(user)
        dbSession.commit()
        flash("User created")
        session['username'] = username
    return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    dbSession = Session()
    if email and password:
        user = dbSession.query(User).filter_by(email=email, password=password).first()
        if user is not None:
            session['username'] = user.username
        else:
            flash("User doesn't exist")
    return redirect('/')


@app.route("/email", methods=["POST", "GET"])
def email_creation():
    sessionDatabase = Session()
    # dohvatanje query parametara po imenu
    email = request.args.get("email")
    if request.method == "POST":
        # dohvatanje form parametara u vidu key-value
        # request.form['key']
        email = request.form['email']
    created = False
    if email:
        session["username"] = email
        allEmails = sessionDatabase.query(DrugaTabela.email).all()
        allEmails = [allEmails[i][0] for i in range(len(allEmails))]
        # print(allEmails)
        if email not in allEmails:
            novi = DrugaTabela(email)
            sessionDatabase.add(novi)
            sessionDatabase.commit()
            created = True
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
