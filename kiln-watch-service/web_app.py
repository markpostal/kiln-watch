from Observations import Observations
from microdot import Microdot
import json

# Configuration file
with open('config.json') as f:
	CONFIG = json.load(f)
port = CONFIG['http_port']

# Data collection
observations = Observations()
observations.collect()
observations.organize()

# Cache static files
STATIC_CACHE = {
	'index.html' : None,
	'site.js' : None,
}
for filename in STATIC_CACHE.keys():
	print(f"Caching: {filename}")
	with open(filename, 'r') as f:
		STATIC_CACHE[filename] = f.read()

CONTENT_TYPE = {
	'html' : 'text/html',
	'js' : 'text/javascript',
	'json' : 'application/json',
}

# Create an instance of the Flask class
app = Microdot()

@app.route("/")
async def index(request):
	filename = "index.html"
	extension = filename.split('.')[-1]
	content_type = CONTENT_TYPE[extension]
	return STATIC_CACHE[filename], 200,{'Content-Type': content_type}

@app.route("/records")
async def get_data(request):
	"""
	Retrieve the recorded temperature measurements
	"""
	data = Observations().data()
	extension = "js"
	content_type = CONTENT_TYPE[extension]
	return json.dumps(data), 200, {'Content-Type': content_type}

@app.route('/<filename>')
async def static_file(request, filename):
	if filename in STATIC_CACHE:
		extension = filename.split('.')[-1]
		content_type = CONTENT_TYPE[extension]
		return STATIC_CACHE[filename], 200, {'Content-Type': content_type}

	return "N/A", 404, {'Content-Type': 'text/plain'}


print(f"Web App listening on port: {port}")
app.run(host='0.0.0.0', port=port)

