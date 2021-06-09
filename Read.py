"""
El siguiente programa es utilizado para leer el UID de una tarjeta a través del lector
RFID RC522 a través del módulo MFRC522.py.

La base de datos está implementada por medio de SQLite3 y su librería nativa de Python.
Dentro de ella, se definió una tabla llamada "estudiantes". Cada registro contiene los
siguientes campos:
- Nombre
- Matrícula
- UID
- Índice

La manera en la que autenticaremos al estudiante será comparar el UID de la tarjeta
con los registros guardados en la base de datos. Si se encuentra al usuario, la autenticación
resultó exitosa. Si la búsqueda regresa una lista vacía o None, el usuario no se encuentra
dentro de la base de datos.

Finalmente, si se cuenta con una autenticación exitosa, se enviará el índice del estudiante
al dispositivo FPGA conectado mediante el puerto I2C. Dicho índice se utilizará para desplegar
los datos del usuario.

Dependencias:
https://github.com/naleefer/SPI-Py
https://github.com/naleefer/MFRC522-python
"""

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

# Librería para base de datos
import sqlite3

# Importar clase Estudiante
from estudiante import Estudiante

# Importar clase FPGA para comunicación por I2C
from i2c_fpga import FPGA

# Inicializar conexión I2C a través del canal 1 de la Raspberry
# con la slave address 0x38
fpga_board = FPGA(1, 0x38)

# Crear conexion base de datos
conn = sqlite3.connect('estudiantes.db')

# Crear un cursor para ejecutar instrucciones de SQL
c = conn.cursor()

def get_student_by_uid(uid):
    """Busca estudiantes dentro de la base de datos por medio de su UID"""
    c.execute("SELECT * FROM estudiantes WHERE uid=:uid", {'uid': uid})
    return c.fetchone()

continue_reading = True

def end_read(signal, frame):
    """Capture SIGINT for cleanup when the script is aborted"""
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

#Botón para cerrar la puerta
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")
fpga_board.send_byte(0x00)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    cont = 0
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

        # Generate a single UID string
        uid_str = "".join([str(pair) for pair in uid])
        print(uid_str)

        # Query the Database using the UID string
        query_result = get_student_by_uid(uid_str)
        print(query_result)

        if query_result is None:
            print("Authentication failed.")
        else:
            student = Estudiante(*query_result)
            print(f"Welcome, {student.nombre} - {student.matricula}")

            # Enviar indice a la FPGA
            fpga_board.send_index(student.indice)

            while(cont < 60):
                if GPIO.input(36) == GPIO.HIGH:
                    print("Se cierra la puerta")
                    fpga_board.send_byte(0x00)
                    cont += 60
                else:
                    cont += 1
                    time.sleep(1)
        time.sleep(3)
