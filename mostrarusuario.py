import mysql.connector
from mysql.connector import Error


def mostrar_perfil(ide):
    try:
        config = {
            "host": "52.1.39.126",
            "port": 3307,
            "user": "buypilot",
            "password": "buypilot23",
            "database": "BuyPilot",
        }
        # Realizamos la conexiÃ³n a la base de datos
        conexion = mysql.connector.connect(**config)
        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = "select nombre_usuario, nombre, apellidos, email, password, foto from usuarios where id = %s"
            cursor.execute(sql, (ide,))
            perfil = cursor.fetchone()
            if perfil is None:
                return {"error": True, "msg": "El usuario no existe"}
            else:
                usuario = {
                    "nombre_usuario": perfil[0],
                    "nombre": perfil[1],
                    "apellidos": perfil[2],
                    "email": perfil[3],
                    "foto": perfil[5]
                        }

                return {"exito": True, "data": usuario}

    except Error as e:
        return {"error": True, "msg": f"Error al conectarse a la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
