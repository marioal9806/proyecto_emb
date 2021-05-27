"""
Inicializa la base de datos con la tabla necesaria para
almacenar los estudiantes de la aplicación.
"""
import sqlite3

con = sqlite3.connect("estudiantes.db")
cur = con.cursor()

# Crear tabla estudiantes
cur.execute("""CREATE TABLE estudiantes
                (
                    nombre TEXT,
                    matricula TEXT,
                    uid TEXT,
                    indice INT
                )""")

con.commit()
con.close()