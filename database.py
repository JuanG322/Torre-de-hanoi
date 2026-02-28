import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "sql123",
}

DB_NAME = "hanoi_game"


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG, database=DB_NAME)
        return conn
    except Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None


def init_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre_usuario VARCHAR(50) UNIQUE NOT NULL,
                contrasena VARCHAR(100) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                dificultad ENUM('facil', 'medio', 'dificil') NOT NULL,
                tiempo_segundos INT NOT NULL,
                completado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                UNIQUE KEY unique_mejor_resultado (usuario_id, dificultad)
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error inicializando base de datos: {e}")
        return False


def registrar_usuario(nombre_usuario, contrasena):
    conn = get_connection()
    if not conn:
        return False, "Error de conexión a la base de datos"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (%s, %s)",
            (nombre_usuario, contrasena)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Usuario registrado correctamente"
    except mysql.connector.IntegrityError:
        conn.close()
        return False, "El nombre de usuario ya existe"
    except Error as e:
        conn.close()
        return False, f"Error: {e}"


def login_usuario(nombre_usuario, contrasena):
    conn = get_connection()
    if not conn:
        return None, "Error de conexión a la base de datos"
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s",
            (nombre_usuario, contrasena)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario:
            return usuario, "Login exitoso"
        return None, "Usuario o contraseña incorrectos"
    except Error as e:
        conn.close()
        return None, f"Error: {e}"


def guardar_resultado(usuario_id, dificultad, tiempo_segundos):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resultados (usuario_id, dificultad, tiempo_segundos)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                tiempo_segundos = IF(%s < tiempo_segundos, %s, tiempo_segundos),
                completado_en = IF(%s < tiempo_segundos, NOW(), completado_en)
        """, (usuario_id, dificultad, tiempo_segundos,
              tiempo_segundos, tiempo_segundos,
              tiempo_segundos))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error guardando resultado: {e}")
        conn.close()
        return False


def obtener_ranking(dificultad):
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.nombre_usuario, r.tiempo_segundos, r.completado_en
            FROM resultados r
            JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.dificultad = %s
            ORDER BY r.tiempo_segundos ASC, r.completado_en ASC
            LIMIT 5
        """, (dificultad,))
        ranking = cursor.fetchall()
        cursor.close()
        conn.close()
        return ranking
    except Error as e:
        print(f"Error obteniendo ranking: {e}")
        conn.close()
        return []
