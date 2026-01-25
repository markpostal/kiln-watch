import _thread
import socket
import time
import random
import json
import heapq

from Record import Record

# Configuration file
with open('config.json') as f:
	CONFIG = json.load(f)

port = CONFIG['udp_port']


def threaded(fn):
	"""
	Wrap the provided function in a thread
	"""
	def wrapper(*args, **kwargs):
		thread = _thread.start_new_thread(fn, args, kwargs)
		return thread
	return wrapper


class Observations:
	"""
	Collect Kiln Watch measurements and organize in a useful way.

	Implements the singleton pattern
	"""

	_instance = None
	_initialized = False

	def __new__(cls, *args, **kwargs):
		"""
		Create/Retrieve the singleton instance
		"""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		"""
		Constructor
		"""
		if not self._initialized:
			self._broadcast_port = port
			self._reports = []
			self._records = {}
			self._run = False
			self._initialized = True

	def stop(self):
		"""
		Stop the tread
		"""
		self._run = False

	@threaded
	def simulate(self, device_count=1):
		"""
		Simulate incoming packets from a number of devices
		"""
		self._run = True

		interval_seconds = 10
		seconds_in_hour = 60 * 60

		current_temp = device_count * [22]
		ramp = device_count * [100]

		# Add some variation to the ramp
		for i in range(0, device_count):
			ramp[i] = ramp[i] + (random.random() - 0.5) * 100.0

		while self._run:
			time.sleep(interval_seconds)
			for index in range(0, device_count):
				temperature = current_temp[index] + ramp[index] * (interval_seconds / seconds_in_hour) + (random.random() - 0.5) * 2
				current_temp[index] = temperature
				if temperature > 1093 and ramp[index] > 0:
					ramp[index] = -ramp[index]
				elif temperature < 20 and ramp[index] < 0:
					ramp[index] = -ramp[index]
				ramp[index] = ramp[i] + (random.random() - 0.5) * 5.0
				report = f"KW,kiln_watch_{index},{index},{round(temperature)}"
				print(f"Incoming report: '{report}'")
				heapq.heappush(self._reports, report)
			# print(ramp)
			# print(current_temp)

		print("Exiting simulate thread.")
		return

	@threaded
	def collect(self):
		"""
		Collect report broadcasts
		"""
		self._run = True
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		# Set the SO_BROADCAST option to allow broadcasting
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

		# Bind the socket to the port on all interfaces
		try:
			sock.bind(('', self._broadcast_port))
			print(f"Listening for UDP broadcasts on port {self._broadcast_port}...")
		except OSError as e:
			print(f"Error binding to port {self._broadcast_port}: {e}")
			return

		while self._run:
			try:
				# Retrieve the data
				data, address = sock.recvfrom(1024)
				report = data.decode('UTF-8')
				if report.startswith("KW,"):
					print(f"Incoming report: '{report}'")
					heapq.heappush(self._reports, report)
			except KeyboardInterrupt:
				print("\nStopped listening.")
				break
			except Exception as e:
				print(f"An error occurred: {e}")
				break

		sock.close()

		print("Exiting collect thread.")
		return

	@threaded
	def organize(self):
		"""
		Organize reports
		"""
		self._run = True

		while self._run:
			try:
				item = heapq.heappop(self._reports)
				# Packet: 'KW,kiln_watch_0,0,23'
				keyword, name, index, temperature = item.split(",")
				index = int(index)
				temperature = int(temperature)
				# Update the record
				if index not in self._records:
					r = Record(index, name)
					self._records[index] = r
				record = self._records[index]
				record.update(temperature)
			except IndexError:
				# Timeout
				time.sleep_ms(5000)

			# Pause the thread for a bit
			time.sleep(1)

		print("Exiting organize thread.")
		return

	def data(self) -> list:
		"""
		Retrieve the data as a list
		"""
		retval = []
		for key in sorted(self._records):
			record = self._records[key]
			retval.append(record.data())

		return retval
