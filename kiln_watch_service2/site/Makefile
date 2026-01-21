OUTPUT=site.js

go: clean
	cat \
		Common.js \
		TemperatureChart.js \
		RampChart.js \
		Legend.js \
	> $(OUTPUT)

clean:
	-rm $(OUTPUT) > /dev/null 2>&1
