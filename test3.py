# import serial
# import time

# modem = serial.Serial("/dev/tty.usbserial-143120",  115200, bytesize=8, parity='N', stopbits=1, timeout=1, rtscts=False, dsrdtr=False)

# cmd="ATI\r\n"
# serialconsole.write(cmd.encode())

# # msg=serialconsole.read(2)

# response = serialconsole.readline()
# print(response)


# cmd="AT\r"
# serialconsole.write(cmd.encode())
# msg=serialconsole.read(64)
# print(msg)
# serialconsole.close() 



# modem = serial.Serial("/dev/tty.usbserial-143120",  115200, timeout=1)
# cmd="AT+GMI\r\n"
# modem.write(cmd.encode())
# msg=modem.read(64)
# print(msg.decode('utf-8').strip())


import time
import serial

recipient = "+1234567890"
message = "Hello, World!"

phone = serial.Serial("/dev/tty.usbserial-143120",  115200, timeout=1)
try:
    time.sleep(0.5)
    phone.write(b'ATZ\r')
    time.sleep(0.5)
    phone.write(b'AT+CMGF=1\r')
    time.sleep(0.5)
    phone.write(b'AT+CMGS="' + recipient.encode() + b'"\r')
    time.sleep(0.5)
    phone.write(message.encode() + b"\r")
    time.sleep(0.5)
    phone.write(bytes([26]))
    time.sleep(0.5)
finally:
    phone.close()