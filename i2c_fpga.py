"""
Programa para comunicarse con una tarjeta FPGA por medio del protocolo I2C
La Raspberry Pi enviarpa el indice del alumno, con el que la FPGA cargará
la información y brindará el acceso.

La dirección slave de la FPGA es 0x11.

alumno:
- matricula
- nombre
- id de la tarjeta
- identificador de la FPGA


"""

import time
import smbus

i2c_ch = 1
i2c_address = 0x38
#i2c_address = 0x11

bus = smbus.SMBus(i2c_ch)

index = 0x00

#bus.write_byte_data(i2c_address, 0x00, index)
bus.write_byte(i2c_address, index)
