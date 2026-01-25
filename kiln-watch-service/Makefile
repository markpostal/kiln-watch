
CHIP=esp32
IMAGE=../ESP32_GENERIC-SPIRAM-20251209-v1.27.0.bin
PORT=/dev/ttyACM0
POSITION=0x1000
SIZE=4M

BAUD=115200
ARCH=xtensa
ESPTOOL=esptool
RSHELL=rshell -p $(PORT) -b $(BAUD)
PARTITION=/pyboard

#HEAPSIZE=7340032
HEAPSIZE=2097152
#EAPSIZE=1048576
#HEAPSIZE=262144

#CONFIG=../config.json
CONFIG=../config.json-mark
#CONFIG=../config.json-jim

MICRODOT=https://raw.githubusercontent.com/miguelgrinberg/microdot/refs/heads/main/src/microdot/microdot.py

all: flash copy

flash: 
	$(ESPTOOL) -p $(PORT) erase_flash
	$(ESPTOOL) -b $(BAUD) -p $(PORT) -c $(CHIP) write-flash $(POSITION) $(IMAGE)

copy: cross
	cd site; make
	$(RSHELL) cp *.mpy $(PARTITION)/
	$(RSHELL) cp site/index.html $(PARTITION)/
	$(RSHELL) cp site/site.js $(PARTITION)/
	$(RSHELL) cp $(CONFIG) $(PARTITION)/config.json
	$(RSHELL) cp boot.py $(PARTITION)/

cross:
	wget -O microdot.py $(MICRODOT)
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) microdot.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) networking.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) web_app.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) Observations.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) Record.py

ls:
	$(RSHELL) ls -la $(PARTITION)/

rshell:
	$(RSHELL) 

debug:
	#$(RSHELL) cp networking.py $(PARTITION)/
	$(RSHELL) cp web_app.py $(PARTITION)/

screen:
	screen $(PORT) $(BAUD)

clean:
	-rm *.mpy > /dev/null 2>&1
	-rm microdot.py > /dev/null 2>&1
	cd site; make clean

