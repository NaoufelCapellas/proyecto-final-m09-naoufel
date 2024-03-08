from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para cifrar la sesión del usuario

# Función para conectar a la base de datos MySQL
def conectar_bd():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='naoufelbd',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para comprobar las credenciales de un usuario en la base de datos
def comprobar_credenciales(usuario, contraseña):
    connection = conectar_bd()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM usuariosbd WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
            result = cursor.fetchall()  # Leer el resultado
            if result:
                return True
            else:
                print("Credenciales inválidas.")
        except Error as e:
            print(f"Error al comprobar las credenciales: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        print("No se pudo establecer la conexión a la base de datos.")
    return False

# Función para registrar un nuevo usuario en la base de datos
def registrar_usuario(usuario, contraseña):
    connection = conectar_bd()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO usuariosbd (usuario, contraseña) VALUES (%s, %s)", (usuario, contraseña))
            connection.commit()
            print("Usuario registrado exitosamente.")
            return True
        except Error as e:
            print(f"Error al registrar usuario: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        print("No se pudo establecer la conexión a la base de datos.")
    return False

# Ruta para la página principal
@app.route('/')
def principal():
    return render_template('principal.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = ''
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if comprobar_credenciales(usuario, contraseña):
            # Almacenar el nombre de usuario en la sesión
            session['usuario'] = usuario
            # Redirigir al usuario a la página privada
            return redirect(url_for('privada'))
        else:
            mensaje = 'Usuario o contraseña incorrectos'
    return render_template('login.html', mensaje=mensaje)

@app.route('/crear_cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    mensaje = ''
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if registrar_usuario(usuario, contraseña):
            # Redirigir al usuario al inicio de sesión después de registrarse exitosamente
            return redirect(url_for('login'))
        else:
            mensaje = 'Error al registrar usuario'
    # Si es una solicitud GET, simplemente muestra la página de creación de cuenta
    return render_template('registro.html', mensaje=mensaje)

# Ruta para la página privada
@app.route('/privada')
def privada():
    # Verificar si el usuario ha iniciado sesión
    if 'usuario' in session:
        usuario = session['usuario']
        return render_template('privat.html', usuario=usuario)
    else:
        # Si el usuario no ha iniciado sesión, redirigir al inicio de sesión
        return redirect(url_for('login'))

# Ruta para la página de registro de usuarios
@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']
        if registrar_usuario(usuario, contraseña):
            # Redirigir al usuario al inicio de sesión después de registrarse exitosamente
            return redirect(url_for('login'))
        else:
            mensaje = 'Error al registrar usuario'
            return render_template('registro.html', mensaje=mensaje)
    # Si es una solicitud GET, simplemente muestra la página de registro
    return render_template('registro.html')

# Ruta para la página final
@app.route('/final', methods=['POST'])
def final():
    # Aquí puedes agregar la lógica para procesar el formulario final
    return render_template('final.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar el nombre de usuario de la sesión
    session.pop('usuario', None)
    # Redirigir al usuario al inicio de sesión
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
