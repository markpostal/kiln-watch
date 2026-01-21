
CHIP=esp32
#IMAGE=ESP32_GENERIC-20251209-v1.27.0.bin
IMAGE=ESP32_GENERIC-SPIRAM-20251209-v1.27.0.bin
#PORT=/dev/ttyUSB0
PORT=/dev/ttyACM0
POSITION=0x1000
SIZE=4M

#CHIP=esp32s3
#IMAGE=ESP32_GENERIC_S3-SPIRAM_OCT-20251209-v1.27.0.bin
#PORT=/dev/ttyACM0
#POSITION=0x0
#SIZE=4M

BAUD=115200
ARCH=xtensa
ESPTOOL=esptool
RSHELL=rshell -p $(PORT) -b $(BAUD)
PARTITION=/pyboard

#HEAPSIZE=7340032
HEAPSIZE=2097152
#EAPSIZE=1048576
#HEAPSIZE=262144
RESIZED_IMAGE=ESP32_GENERIC_RESIZED.bin

all: flash copy

flash: resize
	$(ESPTOOL) -p $(PORT) erase_flash
	$(ESPTOOL) -b $(BAUD) -p $(PORT) -c $(CHIP) write-flash $(POSITION) $(RESIZED_IMAGE)

copy: cross
	cd site; make
	#$(RSHELL) cp *.py ${PARTITION}/
	$(RSHELL) cp *.mpy ${PARTITION}/
	$(RSHELL) cp site/index.html ${PARTITION}/
	$(RSHELL) cp site/site.js ${PARTITION}/
	$(RSHELL) cp config.json ${PARTITION}/
	$(RSHELL) cp boot.py ${PARTITION}/

cross:
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) microdot.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) networking.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) web_app.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) Observations.py
	mpy-cross -march=$(ARCH) -X heapsize=$(HEAPSIZE) Record.py

ls:
	$(RSHELL) ls -la ${PARTITION}/

rshell:
	$(RSHELL) 

debug:
	#$(RSHELL) cp networking.py ${PARTITION}/
	$(RSHELL) cp web_app.py ${PARTITION}/

screen:
	screen $(PORT) $(BAUD)

resize:
	cp $(IMAGE) $(RESIZED_IMAGE)
	#mp-image-tool-esp32 $(IMAGE) -f $(SIZE) --resize factory=0 -o $(RESIZED_IMAGE)

clean:
	-rm *.mpy > /dev/null 2>&1
	-rm $(RESIZED_IMAGE) > /dev/null 2>&1
	cd site; make clean

