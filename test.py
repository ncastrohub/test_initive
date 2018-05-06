import unittest
from datetime import date
from model import (
    ReservationPerHour, 
    ReservationPerDay, 
    ReservationPerWeek, 
    COST_PER_DAY, 
    COST_PER_HOUR, 
    COST_PER_WEEK, 
    FAMILY_DISCOUNT
)

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


class TestReservation(unittest.TestCase):


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
        
        family_reservation = FamilyReservation(
            [reservation_hour, reservation_day, reservation_week]
        )

        reservation_hour.end(start_date + datetime.timedelta(hours=12))
        reservation_day.end(start_date + datetime.timedelta(days=5))
        reservation_week.end(start_date + datetime.timedelta(days=24))

        not_discounted_price = 
            (COST_PER_DAY * 5) + 
            (COST_PER_WEEK * 4) + 
            (COST_PER_HOUR * 12)

        discount = (FAMILY_DISCOUNT * not_discounted_price) / 100.0
        expected_cost = not_discounted_price - discount
        

        self.assertEqual(
            expected_cost,
            family_reservation.final_price()
        )


    def test_family_reservation_cannot_have\
        _more_than_five_asociated_rentals(self):
        start_date = datetime.now()

        reservation_list = [
            ReservationPerHour(start_date) 
            ,ReservationPerDay(start_date)
            ,ReservationPerDay(start_date)
            ,ReservationPerWeek(start_date)
            ,ReservationPerWeek(start_date)
            ,ReservationPerWeek(start_date)
        ]

        with self.assertRaises(InvalidAmountOfReservationsOnFamiliyError):
            family_reservation = FamilyReservation(reservation_list)


    def test_family_reservation_cannot_have_\
        less_than_three_asociated_rentals(self):
        start_date = datetime.now()

        reservation_list = [
            ReservationPerHour(start_date) 
            ,ReservationPerDay(start_date)
        ]

        with self.assertRaises(InvalidAmountOfReservationsOnFamiliyError):
            family_reservation = FamilyReservation(reservation_list)


    def test_cannot_have_final_price_of_not_ended_reservation(self)
        start_date = datetime.now()
        reservation = ReservationPerHour(start_date) 

        with self.assertRaises(ReservationNotEndedError):
            reservation.final_price()


if __name__ == '__main__':
    unittest.main()