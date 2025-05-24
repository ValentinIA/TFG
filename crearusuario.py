import mysql.connector
import bcrypt
from mysql.connector import Error
from mysql.connector import IntegrityError


def usuario_nuevo(nombre_usuario, nombre, apellidos, email, password, foto):
    try:
        config = {
            "host": "52.1.39.126",
            "port": 3307,
            "user": "buypilot",
            "password": "buypilot23",
            "database": "BuyPilot",
        }
        # Realizamos la conexión a la base de datos
        conexion = mysql.connector.connect(**config)
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


# usuario_nuevo("admin","admin","admin uno","a@a","buypilotadmin123","admin","../foto")
# usuario_nuevo("alex","Alex","Alonso Ocaña","alex@alex","buypilotadmin123","user","../foto")
