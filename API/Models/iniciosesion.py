import mysql.connector
import bcrypt
from mysql.connector import Error


def comprobarpass(email, password):
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
            sql = "select password from usuarios where email = %s"
            cursor.execute(sql, (email,))
            passwd = cursor.fetchone()
            if passwd is None:
                return {"error": True, "msg": "El usuario no existe"}
            else:
                if bcrypt.checkpw(password.encode(), passwd[0].encode()):
                    sql = "select id from usuarios where email = %s"
                    cursor.execute(sql, (email,))
                    ide = cursor.fetchone()

                    usuario = {
                        "ide": ide[0],
                    }

                    return {"exito": True, "data": usuario}

                else:
                    return {"error": True, "msg": "contraseña incorrecta"}

    except Error as e:
        return {"error": True, "msg": f"Error al conectarse a la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
