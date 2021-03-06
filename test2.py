import serial
from time import sleep
 
 
def send_to_console(ser: serial.Serial, command: str, wait_time: float = 0.5):
    command_to_send = command + "\r"
    ser.write(command_to_send.encode('utf-8'))
    sleep(wait_time)
    print(ser.read(ser.inWaiting()).decode('utf-8'), end="")
 
with serial.Serial("/dev/tty.usbserial-143120",  115200, timeout=5) as ser:
    print(f"Connecting to {ser.name}...")
    send_to_console(ser, "")
    send_to_console(ser, "enable")
    send_to_console(ser, "show ap summary", wait_time=2)
    print(f"Connection to {ser.name} closed.")


# with serial.Serial("/dev/tty.usbserial-143120",  115200, timeout=5) as ser:
#     print(f"Connecting to {ser.name}...")
#     send_to_console(ser, "")
#     send_to_console(ser, "ATI")
#     print(f"Connection to {ser.name} closed.")


with serial.Serial("/dev/tty.usbserial-143120",  115200, timeout=5):
    serial.write(ser, b"ATI\r\n")
    serial.read(32798)
    response = serial.readline()
    print(response)
    serial.close() 