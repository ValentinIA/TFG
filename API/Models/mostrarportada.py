import mysql.connector
import random
from mysql.connector import Error
from mysql.connector import ProgrammingError


def mostrarportada():
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

                sql = "select id from productos_favoritos"
                cursor.execute(sql)
                cantidad = cursor.fetchall()

                portadas = random.sample(cantidad, 10)

                favoritos = []
                for portada in portadas:
                    sqlfinal = "select titulo, precio, imagen_url, url, tienda from productos_favoritos where id=%s"
                    cursor.execute(sqlfinal, (portada[0],))
                    consultas = cursor.fetchone()
                    favorito = {
                        "titulo": consultas[0],
                        "precio": str(consultas[1]),
                        "imagen_url": consultas[2],
                        "url": consultas[3],
                        "tienda": consultas[4],
                    }
                    favoritos.append(favorito)

                return favoritos
            except ProgrammingError as e:
                return {"error": True, "msg": "Error en la consulta"}

    except Error as e:
        return {"error": True, "msg": f"Error al conectarse a la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
