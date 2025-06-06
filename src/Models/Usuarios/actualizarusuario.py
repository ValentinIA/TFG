from mysql.connector import Error
from mysql.connector import IntegrityError
from Models.Conexion_db import get_conexion

def actualizar_usuario(nombre_usuario, nombre, apellidos, email, id):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()
        
        if conexion.is_connected():
            cursor = conexion.cursor()
            try:
                sql = "update usuarios set nombre_usuario= %s, nombre = %s, apellidos = %s, email = %s where id=%s "
                cursor.execute(
                    sql, (nombre_usuario, nombre, apellidos, email, id)
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
