MODULE=kiln_watch_service
VERSION=0.2.0

service: uninstall clean build install

build:
	sed -i 's/^version.*$$/version = "$(VERSION)"/' pyproject.toml
	poetry build

install: build
	ls -la dist/$(MODULE)-$(VERSION)*-py3-none-any.whl
	pip3 install --force-reinstall dist/$(MODULE)-$(VERSION)-py3-none-any.whl

uninstall:
	ls -la dist/$(MODULE)-$(VERSION)*-py3-none-any.whl
	pip3 uninstall -y dist/$(MODULE)-$(VERSION)*-py3-none-any.whl

clean:
	-rm -rf dist > /dev/null 2>&1
	-rm -rf $(MODULE)/__pycache__ > /dev/null 2>&1
	-rm -f typescript > /dev/null 2>&1

firmware:
	script -c "python3 -m venv vesphome; source vesphome/bin/activate; pip3 install esphome; esphome upload kiln-watch.yaml;"
