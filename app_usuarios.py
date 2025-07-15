import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for, flash
from passlib.hash import sha256_crypt

# Nombres de los integrantes del grupo (modifica aquí tus nombres reales)
INTEGRANTES = [
    {"usuario": "clobos", "clave": "clobos"},
    
]

DB_FILE = "usuarios.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    
    for integrante in INTEGRANTES:
        cur.execute("SELECT * FROM usuarios WHERE nombre = ?", (integrante["usuario"],))
        if cur.fetchone() is None:
            hash_pwd = sha256_crypt.hash(integrante["clave"])
            cur.execute("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", (integrante["usuario"], hash_pwd))
    conn.commit()
    conn.close()


init_db()

app = Flask(__name__)
app.secret_key = 'secretoexamen123'  

TEMPLATE = """
<!doctype html>
<title>Login Examen DRY7122</title>
<h2>Ingreso de usuario</h2>
<form method=post>
  Usuario: <input type=text name=usuario required><br>
  Contraseña: <input type=password name=clave required><br>
  <input type=submit value="Ingresar">
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul style="color:red;">
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
    </ul>
  {% endif %}
{% endwith %}
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (usuario,))
        fila = cur.fetchone()
        conn.close()
        if fila and sha256_crypt.verify(clave, fila[0]):
            return f"<h2>Bienvenido, {usuario}!</h2><p>Acceso concedido.</p>"
        else:
            flash("Usuario o clave incorrectos.")
    return render_template_string(TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5800, debug=True)

