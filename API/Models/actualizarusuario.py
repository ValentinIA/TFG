import mysql.connector
import bcrypt
from mysql.connector import Error
from mysql.connector import IntegrityError


def actualizarusuario(nombre_usuario, nombre, apellidos, email, password, foto, id):
    try:
        # Realizamos la conexión a la base de datos
        conexion = mysql.connector.connect(
            host="52.1.39.126",
            port=3307,
            user="buypilot",
            password="buypilot23",
            database="BuyPilot",
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            try:
                passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                sql = "update usuarios set nombre_usuario= %s, nombre = %s, apellidos = %s, email = %s, password = %s, foto = %s where id=%s "
                cursor.execute(
                    sql, (nombre_usuario, nombre, apellidos, email, passwd, foto, id)
                )
                conexion.commit()

                return {"exito": True}
            except IntegrityError as e:
                return {"error": True, "msg": "El usuario no existe"}

    except Error as e:
        return {"error": True, "msg": f"Error al conectarse a la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
