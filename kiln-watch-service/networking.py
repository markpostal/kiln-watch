import network
import utime
import json


# Configuration file
with open('config.json') as f:
	CONFIG = json.load(f)

ssid = CONFIG['ssid']
wifi_password = CONFIG['wifi_password']
hostname = CONFIG['hostname']


# enable station interface and connect to WiFi access point
wlan = network.WLAN(network.STA_IF)
network.hostname(hostname) # Set hostname before activation
wlan.active(True)
wlan.connect(ssid, wifi_password)
utime.sleep(1)

if not wlan.isconnected():
	while not wlan.isconnected():
		utime.sleep(1)

print(f"Wifi Station up and running on {hostname}.local")
