#!/usr/bin/env python3
import sqlite3
from estudiante import Estudiante

def add_student(student):
    """Este metodo agrega una instancia de Estudiante a la Base de datos"""
    with con:
        cur.execute("INSERT INTO estudiantes VALUES(:nombre, :matricula, :uid, :indice)",
                  {'nombre': student.nombre, 'matricula': student.matricula, 'uid': student.uid, 'indice': student.indice})


con = sqlite3.connect("estudiantes.db")
cur = con.cursor()

# cur.execute("DELETE FROM estudiantes WHERE nombre=:nombre", {'nombre':'Mario'})
# con.commit()

cur.execute("SELECT * FROM estudiantes")
rows = cur.fetchall()
print(rows)

# Add user for card UID
student_1 = Estudiante('Mario', 'A01730557', '165432829143', 1)
add_student(student_1)

# Add user for keyring UID
student_2 = Estudiante('Alberto', 'A01730557', '64210203131218', 2)
add_student(student_2)

con.commit()
con.close()