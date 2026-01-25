import math
import _thread
import time
#import copy


class Record:
	"""
	The record of temperatures over time for a single sensor.
	"""
	HOURS = 12
	RAMP_INTERVAL = 1.0

	def __init__(self, index: int, name: str):
		"""
		Constructor
		"""
		self._index = int(index)
		self._name = name
		self._reports = [[0, 0]]
		self._last_report = None
		self._lock = _thread.allocate_lock()

	def index(self) -> int:
		"""
		The sensor index
		"""
		return self._index

	def name(self) -> str:
		"""
		The sensor name
		"""
		return self._name

	def pad_report_list(self, list_to_pad, current_time_minutes):
		"""
		Pad the report list to allow for missing reports.
		"""
		retval = list_to_pad

		if self._last_report:
			missing_minutes = current_time_minutes - self._last_report
			# fill in the gaps that didn't have reports
			for i in range(0, missing_minutes):
				retval.append([0, 0])

		return retval

	def truncate_report_list(self, list_to_truncate):
		"""
		Truncate the report array as required
		"""
		retval = list_to_truncate

		max_len = Record.HOURS * 60
		if len(retval) > max_len:
			retval = retval[-max_len:]

		return retval

	def update(self, temperature: int):
		"""
		Update the record with a new temperature report
		"""

		with self._lock:

			current_time_minutes = int(math.floor(time.time()) / 60)

			# Account for missing reports
			self._reports = self.pad_report_list(self._reports, current_time_minutes)

			# Truncate the report array as required
			self._reports = self.truncate_report_list(self._reports)

			if not self._last_report:
				self._reports[-1] = [temperature, 1]
			else:
				# Temperature update to previous report
				cumulative_temperature, nreports = self._reports[-1]
				self._reports[-1] = [cumulative_temperature + temperature, nreports + 1]

			# Save the latest timestamp
			self._last_report = current_time_minutes

	def ramp(self, reports, time_late):
		"""
		Return the ramp associated with the given time late
		"""
		retval = 0

		# Filter the reports by time
		end_time = time_late
		start_time = end_time - self.RAMP_INTERVAL
		filtered_reports = list(
			filter(lambda x: start_time < x['time_late'] <= end_time, reports))
		if len(filtered_reports) > 1:
			retval = ((filtered_reports[-1]['temp'] - filtered_reports[0]['temp']) /
					  math.fabs(filtered_reports[-1]['time_late'] - filtered_reports[0]['time_late']))

		return retval

	def data(self) -> dict:
		"""
		All the data
		"""
		reports = []
		ramps = []

		with self._lock:

			copy_of_reports = self._reports # copy.deepcopy(self._reports)

			current_time_minutes = int(math.floor(time.time()) / 60)

			# Account for missing reports
			copy_of_reports = self.pad_report_list(copy_of_reports, current_time_minutes)

			# Truncate the report array as required
			copy_of_reports = self.truncate_report_list(copy_of_reports)

			for index in range(0, len(copy_of_reports)):
				cumulative_temperature, nreports = copy_of_reports[index]
				if nreports > 0:

					# Temperature in Fahrenheit
					temperature = int(float(cumulative_temperature / float(nreports) * 9.0 / 5.0) + 32.0)
					time_late = -float(len(copy_of_reports) - 1 - index) / 60.0
					if time_late == -0:
						time_late = 0

					# Truncate precision (decimal places)
					time_late = round(time_late, 4)

					# Temperature report
					reports.append({
						"time_late": time_late,
						"temp": temperature
					})

					# Ramp report
					if not index == 0:
						ramps.append({
							"time_late": time_late,
							"rate": int(self.ramp(reports, time_late))
						})

		return {
			"index": self.index(),
			"name": self.name(),
			"reports": reports,
			"ramps": ramps
		}
