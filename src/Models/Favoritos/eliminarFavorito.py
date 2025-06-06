from mysql.connector import Error
from Models.Conexion_db import get_conexion
def eliminar_favorito(ide, titulo):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = "DELETE FROM productos_favoritos WHERE id_usuario = %s AND titulo = %s"
            cursor.execute(sql, (ide, titulo))
            conexion.commit()

            if cursor.rowcount == 0:
                return {"error": True, "msg": "El favorito no existe o ya fue eliminado"}

            return {"exito": True}

    except Error as e:
        return {"error": True, "msg": f"Error en la base de datos: {e}"}

    finally:
        if "conexion" in locals() and conexion.is_connected():
            cursor.close()
            conexion.close()
