import bcrypt
from mysql.connector import Error
from Models.Conexion_db import get_conexion

def comprobar_pass(email, password):
    try:
        # Realizamos la conexión a la base de datos
        conexion = get_conexion()

        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = "select password from usuarios where email = %s"
            cursor.execute(sql, (email,))
            passwd = cursor.fetchone()
            if passwd is None:
                return {"error": True, "msg": "El usuario no existe"}
            else:
                if bcrypt.checkpw(password.encode(), passwd[0].encode()):
                    sql = "select id, nombre_usuario, nombre, apellidos, email, foto from usuarios where email = %s"
                    cursor.execute(sql, (email,))
                    datos = cursor.fetchone()

                    usuario = {
                        "id": datos[0],
                        "nombre_usuario": datos[1],
                        "nombre": datos[2],
                        "apellidos": datos[3],
                        "email": datos[4],
                        "foto": datos[5]
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
