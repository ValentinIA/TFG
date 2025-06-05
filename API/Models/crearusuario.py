import mysql.connector
import bcrypt
from mysql.connector import Error
from mysql.connector import IntegrityError
from dotenv import load_dotenv
import os

def usuario_nuevo(nombre_usuario, nombre, apellidos, email, password, foto):
    try:
        # Realizamos la conexión a la base de datos
        load_dotenv()

        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
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
