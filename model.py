import datetime


COST_PER_HOUR = 5


class ReservationPerHour():
	""" A reservation that calculates its price by hour """
	def __init__(self, start_date):
		self.start_date = start_date
		
	
	def end(self, end_date):
		self.end_date = end_date

	def final_price(self):
		delta = self.end_date - self.start_date
		hours = delta.days * 24 + delta.seconds / 3600.0
		return hours * COST_PER_HOUR