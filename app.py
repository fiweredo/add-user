from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from selenium_script import agregar_usuario_en_plataforma
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actor TEXT,
                    nuevo_usuario TEXT,
                    timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
        result = c.fetchone()
        conn.close()
        if result:
            session['user'] = user
            return redirect('/dashboard')
        return "Credenciales inválidas"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        nuevo_user = request.form['nuevo_user']
        nuevo_pass = request.form['nuevo_pass']

        exito = agregar_usuario_en_plataforma(nuevo_user, nuevo_pass)

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute("INSERT INTO logs (actor, nuevo_usuario, timestamp) VALUES (?, ?, ?)",
                  (session['user'], nuevo_user, datetime.now().isoformat()))
        conn.commit()
        conn.close()

        return f"Usuario '{nuevo_user}' agregado {'con éxito' if exito else 'con error'}"
    return render_template('create_user.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
