from mysql.connector import Error
from Models.Conexion_db import get_conexion

def obtener_perfil_usuario(ide):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()
        
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
