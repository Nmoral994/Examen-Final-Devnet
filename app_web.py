import sqlite3
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = "usuarios.db"

def inicializar_bd():
    """Crea la base de datos y almacena los usuarios con contraseñas en hash"""
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    usuarios_demo = [
        ("Nicolas Morales", "Examen2026*"),
        ("Admin", "Examen2026*")
    ]
    
    for usuario, clave in usuarios_demo:
        hash_clave = generate_password_hash(clave)
        try:
            cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (usuario, hash_clave))
        except sqlite3.IntegrityError:
            pass
            
    conexion.commit()
    conexion.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Valida los usuarios ingresados contra la base de datos"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("SELECT password_hash FROM usuarios WHERE username=?", (username,))
        resultado = cursor.fetchone()
        conexion.close()
        
        if resultado and check_password_hash(resultado[0], password):
            return f"<h3>✅ Validación exitosa: Bienvenido/a {username}.</h3>"
        else:
            return "<h3>❌ Error: Usuario o contraseña incorrectos.</h3>"
            
    return '''
        <h2>Validación de Usuarios</h2>
        <form method="POST">
            Usuario: <input type="text" name="username"><br><br>
            Contraseña: <input type="password" name="password"><br><br>
            <input type="submit" value="Validar">
        </form>
    '''

if __name__ == '__main__':
    inicializar_bd()
    print("Base de datos SQLite inicializada exitosamente.")
    
    app.run(host='0.0.0.0', port=5800)