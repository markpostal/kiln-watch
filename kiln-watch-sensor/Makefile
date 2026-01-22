
CHIP=esp32
IMAGE=../ESP32_GENERIC-20251209-v1.27.0.bin
PORT=/dev/ttyUSB0
POSITION=0x1000
SIZE=4M

BAUD=115200
ARCH=xtensa
ESPTOOL=esptool
RSHELL=rshell -p $(PORT) -b $(BAUD)
PARTITION=/pyboard

CONFIG=../config.json
#CONFIG=../config.json-jim
#CONFIG=../config.json-mark

all: flash copy

flash: 
	$(ESPTOOL) -p $(PORT) erase_flash
	$(ESPTOOL) -b $(BAUD) -p $(PORT) -c $(CHIP) write-flash $(POSITION) $(IMAGE)

copy: 
	$(RSHELL) cp $(CONFIG) $(PARTITION)/config.json
	$(RSHELL) cp max31856.py $(PARTITION)/
	$(RSHELL) cp networking.py $(PARTITION)/
	$(RSHELL) cp boot.py $(PARTITION)/

ls:
	$(RSHELL) ls -la $(PARTITION)/

rshell:
	$(RSHELL) 

screen:
	screen $(PORT) $(BAUD)

