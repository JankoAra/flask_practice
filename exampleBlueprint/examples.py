import mysql.connector
from flask import Blueprint, render_template, redirect, url_for, request, session, current_app
from flask_mail import Message
from sqlalchemy.orm import Session

from sqlacodegen_models_generation.models import PrvaTabela, DrugaTabela

bp = Blueprint("examples", __name__, template_folder='exampleTemplates')


@bp.route("hello")
def hello():
    return render_template("hello.html", name='janko examples')


# path params
@bp.route('/hello/<name>')
def hello_name(name):
    return render_template("hello.html", name=name)


# path params kastovan (int, float, path)
@bp.route('/sum/<int:num1>/<int:num2>')
def sum(num1, num2):
    return "%d" % (num1 + num2)


# redirektovanje i otkrivanje url-a za neku funkciju
@bp.route("/inc/<int:num>")
def inc(num):
    return redirect(location=url_for("examples.sum", num1=num, num2=1), code=302)


@bp.route("/cheer/<name>")
def cheer(name):
    return render_template("cheerleaders.html", name=name)


@bp.route('/baza')
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


@bp.route("/sqla")
def sqla():
    session = Session()
    name = request.args.get("name")
    if name:
        novi = PrvaTabela(name, 120, "blabla")
        session.add(novi)
        session.commit()
    session.close()
    return "kreiran korisnik" if name else "nema parametaraa"


@bp.route("/content")
def contentPage():
    if "username" in session:
        # postoji ime u sesiji, korisnik je ulogovan
        return render_template("logged.html")
    else:
        return render_template("notLogged.html")


@bp.route("/mail")
def send_mail():
    # obtain mail from main app
    mail = current_app.extensions['mail']
    msg = Message('Hello', sender='sender@mail.com', recipients=['receiver@mail'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"
