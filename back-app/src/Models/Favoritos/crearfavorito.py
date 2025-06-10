from mysql.connector import Error
from mysql.connector import ProgrammingError
from Models.Conexion_db import get_conexion

def favorito_nuevo(titulo, precio, imagen_url, url, id_usuario, tienda):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            try:
                sql = "insert into productos_favoritos (titulo, precio, imagen_url, url, id_usuario, tienda) values (%s,%s,%s,%s,%s,%s)"
                cursor.execute(
                    sql, (titulo, precio, imagen_url, url, id_usuario, tienda)
                )
                conexion.commit()
                return {"exito": True}
            except ProgrammingError as e:
                return {"error": True, "msg": "Usuario ya existe"}

    except Error as e:
        return {"error": True, "msg": f"Error al conectarse a la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()


