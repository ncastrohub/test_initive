import unittest
from datetime import date
from model import Bike, COST_PER_DAY

# Context
# A company rents bikes under following options:
# 1. Rental by hour, charging $5 per hour
# 2. Rental by day, charging $20 a day
# 3. Rental by week, changing $60 a week
# 4. Family Rental, is a promotion that can include from 3 to 5 Rentals (of any type) with a discount
# of 30% of the total price

# las opciones que tiene una empresa de bicicletas

# podes rentar, por hora, y te sale 5 pesos la hora
# podes rentar por dia y te sale 20$ por dia
# podes restar por semana y te sale 60$ por semana
# podes rentar familiar, que incluse de 3 a 5 autos y lo que haces
# es rentar de 3 a 5 de cualquiera de los otros tipos

# al total le resto el 30%

# 


class TestRentBikes(unittest.TestCase):


    def test_when_rent_a_bike_per_hour_the_price_is_per_each_hour(self):
        start_date = datetime.now()
        reservation = ReservationPerHour(start_date)
        reserved_hours = 3
        end_date = start_date + datetime.timedelta(hours=reserved_hours)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_HOUR * reserved_hours, 
            reservation.final_price()
        )


    def test_when_rent_a_bike_per_day_the_price_is_per_each_day(self):
        start_date = datetime.now()
        reservation = ReservationPerDay(start_date)
        start_date = date.today()
        reserved_days = 5
        end_date = start_date + datetime.timedelta(days=reserved_days)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_DAY * reserved_days, 
            reservation.final_price()
        )


    def test_when_rent_a_bike_per_week_the_price_is_per_each_week(self):
        start_date = datetime.now()
        reservation = ReservationPerWeek(start_date)
        start_date = date.today()
        reserved_days = 7
        end_date = start_date + datetime.timedelta(days=reserved_days)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_WEEK * reserved_days, 
            reservation.final_price()
        )


    def test_when_rent_type_family_the_price_is_the_total_with_discount(self):
        start_date = datetime.now()

        reservation_hour = ReservationPerHour(start_date)
        reservation_day = ReservationPerDay(start_date)
        reservation_week = ReservationPerWeek(start_date)

        family_reservation = FamilyReservation()
        
        family_reservation.add(reservation_hour)
        family_reservation.add(reservation_day)
        family_reservation.add(reservation_week)

        reservation_hour.end(start_date + datetime.timedelta(hours=12))
        reservation_day.end(start_date + datetime.timedelta(days=5))
        reservation_week.end(start_date + datetime.timedelta(days=24))

        not_discounted_price = 
            (COST_PER_DAY * 5) + 
            (COST_PER_WEEK * 4) + 
            (COST_PER_HOUR * )

        discount = (FAMILY_DISCOUNT * not_discounted_price) / 100.0
        expected_cost = not_discounted_price - discount
        reservation.end(end_date)
        self.assertEqual(
            expected_cost,
            family_reservation.final_price()
        )




if __name__ == '__main__':
    unittest.main()