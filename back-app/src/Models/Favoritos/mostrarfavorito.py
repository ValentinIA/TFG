from mysql.connector import Error
from mysql.connector import ProgrammingError
from Models.Conexion_db import get_conexion

def mostrar_favoritos(id_usuario):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            try:
                sql = "select titulo, precio, imagen_url, url, tienda from productos_favoritos where id_usuario=%s"
                cursor.execute(sql, (id_usuario,))
                # obtenemos los resultados y los guardamos
                consultas = cursor.fetchall()
                favoritos = []

                for consulta in consultas:
                    favorito = {
                        "titulo": consulta[0],
                        "precio": str(consulta[1]),
                        "imagen_url": consulta[2],
                        "url": consulta[3],
                        "tienda": consulta[4],
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
