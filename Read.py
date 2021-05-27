import RPi.GPIO as GPIO
import MFRC522
import signal
import time

# Librería para base de datos
import sqlite3

# Importar clase Estudiante
from estudiante import Estudiante

# Crear conexion base de datos
conn = sqlite3.connect('estudiantes.db')

# Crear un cursor para ejecutar instrucciones de SQL
c = conn.cursor()

# Definir un metodo para agregar estudiantes a la db


def add_student(student):
    """Este metodo agrega una instancia de estudiante a la Base de datos"""
    with conn:
        c.execute("INSERT INTO estudiantes VALUES(:nombre, :matricula, :uid, :indice)",
                  {'nombre': student.nombre, 'matricula': student.matricula, 'uid': student.uid, 'indice': student.indice})

# Definir un metodo para encontrar estudiantes por medio de su uid


def get_student_by_uid(uid):
    c.execute("SELECT * FROM estudiantes WHERE uid=:uid", {'uid': uid})
    return c.fetchall()

#estudiante_1 = Estudiante('Mario', 'A01730557', '73171579', '1')
# add_student(estudiante_1)


continue_reading = True

# Capture SIGINT for cleanup when the script is aborted


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print("Card read UID: %s,%s,%s,%s,%s" %
              (uid[0], uid[1], uid[2], uid[3], uid[4]))

        uid_str = "".join([str(pair) for pair in uid])
        print(uid_str)
        query_result = get_student_by_uid(uid_str)
        print(query_result)

        # La manera en la que autenticaremos al estudiante será comparar el UID de la tarjeta
        # con los registros guardados en la base de datos. Si se encuentra al usuario, la autenticación
        # resultó exitosa. Si la búsqueda regresa una lista vacía o None, el usuario no se encuentra
        # dentro de la base de datos

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(
            MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print("Authentication error")

        time.sleep(3)
