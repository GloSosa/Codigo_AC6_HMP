import mysql.connector
from flask import Flask, render_template, request

def connectBD():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="333",
        database="users"
    )
    return db

def initBD():
    bd = connectBD()
    cursor = bd.cursor()


    query = "CREATE TABLE IF NOT EXISTS users(\
            user varchar(30) primary key,\
            password varchar(30),\
            name varchar(30), \
            surname1 varchar(30), \
            surname2 varchar(30), \
            age integer, \
            salary float); "
    cursor.execute(query)


    query = "SELECT count(*) FROM users;"
    cursor.execute(query)
    count = cursor.fetchall()[0][0]
    if (count == 0):
        query = "INSERT INTO users \
            VALUES('user01','admin','Ramón','Sigüenza','López',35,50000);"
        cursor.execute(query)

    bd.commit()
    bd.close()
    return


def checkUser(user, password):
    bd = connectBD()
    cursor = bd.cursor()

    query = f"SELECT user,name,surname1,surname2,age,genre FROM users WHERE user='{user}'\
            AND password='{password}'"
    cursor.execute(query)
    userData = cursor.fetchall()
    bd.close()

    if userData == []:
        return False
    else:
        return userData[0]

def createUser(username, password, name, surname1, surname2, age, salary):
    bd = connectBD()
    cursor = bd.cursor()

    query = """INSERT INTO users (user, password, name, surname1, surname2, age, salary) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (username, password, name, surname1, surname2, age, salary)
    cursor.execute(query, values)

    bd.commit()
    bd.close()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    initBD()
    return render_template("login.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/newUser", methods=['POST'])
def newUser():
    if request.method == 'POST':
        formData = request.form
        username = formData['username']
        password = formData['password']
        name = formData['name']
        surname1 = formData['surname1']
        surname2 = formData['surname2']
        age = formData['age']
        salary = formData['salary']
        
        createUser(username, password, name, surname1, surname2, age, salary)
        
        return "User created successfully!"

@app.route("/results", methods=('GET', 'POST'))
def results():
    if request.method == 'POST':
        formData = request.form
        user = formData['usuario']
        password = formData['contrasena']
        userData = checkUser(user, password)

        if userData == False:
            return render_template("results.html", login=False)
        else:
            return render_template("results.html", login=True, userData=userData)


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.run(host='localhost', port=5000, debug=True)
