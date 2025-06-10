import bcrypt
from mysql.connector import Error
from mysql.connector import IntegrityError
from Models.Conexion_db import get_conexion

def crear_usuario(nombre_usuario, nombre, apellidos, email, password, foto):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            try:
                passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                sql = "insert into usuarios (nombre_usuario, nombre, apellidos, email, password, foto) values (%s,%s,%s,%s,%s,%s)"
                cursor.execute(
                    sql, (nombre_usuario, nombre, apellidos, email, passwd, foto)
                )
                conexion.commit()
                return {"exito": True}
            except IntegrityError as e:
                return {"error": True, "msg": "El usuario ya existe"}

    except Error as e:
        return {"error": True, "msg": f"Error al conectarse a la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
