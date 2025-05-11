import mysql.connector

config = {
    'host': '52.1.39.126',
    'port': 3307,
    'user': 'buypilot',
    'password': 'buypilot23',  
    'database': 'BuyPilot'
}

try:
    conn = mysql.connector.connect(**config)
    print("Conexión exitosa.")
    
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    for table in cursor:
        print(table)
    
    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print(f"Error al conectar: {err}")
