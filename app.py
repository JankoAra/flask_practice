from flask import Flask, request, render_template
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import PrvaTabela, DrugaTabela

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://janko:janko@192.168.1.200:3306/prvaBaza"

# Define the SQLAlchemy engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("post_request.html")


@app.route('/baza')
def ping():  # put application's code here
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
    email = request.args.get("email")
    if request.method == "POST":
        email = request.form['email']
    if email:
        novi = DrugaTabela(email)
        session.add(novi)
        session.commit()
    session.close()
    return "kreiran korisnik" if email else "nema email-a"


if __name__ == '__main__':
    app.run()
