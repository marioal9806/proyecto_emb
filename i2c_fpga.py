"""
Programa para comunicarse con una tarjeta FPGA por medio del protocolo I2C
La Raspberry Pi enviará el indice del alumno, con el que la FPGA cargará
la información y brindará el acceso.

La dirección slave de la FPGA es 0x38.

La información del alumno es:
- matricula
- nombre
- id de la tarjeta
- identificador de la FPGA
"""

import smbus

class FPGA:
    """
    Clase para encapsular la funcionalidad relacionada con
    la comunicación entre la tarjeta FPGA y la Raspberry Pi
    a través del protocolo de comunicación I2C
    """
    def __init__(self, i2c_channel=1, i2c_address=0x38):
        self.i2c_address = i2c_address
        self.i2c_channel = i2c_channel
        self.bus = smbus.SMBus(self.i2c_channel)

    def send_byte(self, byte):
        """Escribir un byte de información sin pasar por ningún registro"""
        self.bus.write_byte(self.i2c_address, byte)

    def send_byte_cmd(self, byte, reg):
        """Escribir un byte de información a un registro en específico"""
        self.bus.write_byte_data(self.i2c_address, reg, byte)

    def send_index(self, index):
        """Enviar el índice del estudiante que accede a la aplicación"""
        self.bus.write_byte(self.i2c_address, index)


if __name__ == '__main__':
    # Test para comprobar funcionalidad
    fpga_board = FPGA(1, 0x38)
    fpga_board.send_index(0xFF)