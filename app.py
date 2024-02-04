from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import PrvaTabela, DrugaTabela

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://janko:janko@192.168.1.200:3306/prvaBaza"

# Define the SQLAlchemy engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)


@app.route('/form')
def form():  # put application's code here
    return render_template("post_request.html")


# alternativni nacin za dodelu rute nekoj funkciji
# app.add_url_rule('/','hello',hello)
@app.route('/')
def hello():
    return "Hello world"


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
    return redirect(url_for("sum", num1=num, num2=1))

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


@app.route("/email", methods=["POST", "GET"])
def email_creation():
    session = Session()
    # dohvatanje query parametara po imenu
    email = request.args.get("email")
    if request.method == "POST":
        # dohvatanje form parametara u vidu key-value
        # request.form['key']
        email = request.form['email']
    if email:
        novi = DrugaTabela(email)
        session.add(novi)
        session.commit()
    session.close()
    return "kreiran korisnik" if email else "nema email-a"


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
