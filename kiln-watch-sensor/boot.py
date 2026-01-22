
import micropython
import max31856
import socket
import json
import time

import networking

micropython.mem_info()

# Configuration file
with open('config.json') as f:
	CONFIG = json.load(f)

port = CONFIG['udp_port']

csPin = 22
misoPin = 19
mosiPin = 23
clkPin = 18


sensor = max31856.max31856(csPin, misoPin, mosiPin, clkPin)

# Connect to broadcast port
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the SO_BROADCAST option to allow broadcasting
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the port on all interfaces
try:
    print("Binding socket")
    sock.bind(('', 0))
except OSError as e:
    print(f"Error binding to port 0: {e}")

while True:
    temp = sensor.readThermocoupleTemp()
    report = f"KW,kiln_watch_0,0,{int(temp)}"
    print(f"Outgoing report: {report}")
    sock.sendto(report, ("255.255.255.255", port))
    time.sleep(10)
