#!/usr/bin/env python

import unittest
from datetime import datetime, timedelta
from model import (
    ReservationPerHour, 
    ReservationPerDay, 
    ReservationPerWeek,
    FamilyReservation,
    COST_PER_DAY, 
    COST_PER_HOUR, 
    COST_PER_WEEK, 
    FAMILY_DISCOUNT,
    InvalidAmountOfReservationsOnFamiliyError,
    ReservationNotEndedError
)


class TestReservation(unittest.TestCase):


    def test_when_rent_a_bike_per_hour_the_price_is_per_each_hour(self):
        start_date = datetime.now()
        reservation = ReservationPerHour(start_date)
        reserved_hours = 3
        end_date = start_date + timedelta(hours=reserved_hours)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_HOUR * reserved_hours, 
            reservation.final_price()
        )

    def test_when_rent_a_bike_per_day_the_price_is_per_each_day(self):
        start_date = datetime.now()
        reservation = ReservationPerDay(start_date)
        reserved_days = 5
        end_date = start_date + timedelta(days=reserved_days)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_DAY * reserved_days, 
            reservation.final_price()
        )

    def test_when_rent_a_bike_per_week_the_price_is_per_each_week(self):
        start_date = datetime.now()
        reservation = ReservationPerWeek(start_date)
        
        #I assume that when a week starts, means a full week
        # eight days cost two weeks

        reserved_days = 8

        end_date = start_date + timedelta(days=reserved_days)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_WEEK * 2, 
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

        reservation_hour.end(start_date + timedelta(hours=12))
        reservation_day.end(start_date + timedelta(days=5))
        reservation_week.end(start_date + timedelta(days=24))

        not_discounted_price =  (COST_PER_DAY * 5) + (COST_PER_WEEK * 4) \
            + (COST_PER_HOUR * 12)

        discount = (FAMILY_DISCOUNT * not_discounted_price) / 100.0
        expected_cost = not_discounted_price - discount

        self.assertEqual(
            expected_cost,
            family_reservation.final_price()
        )


    def test_family_reservation_max_amount_of_childs(self):
        """When a family reservation has more 
        than 5 reservation childs, its fails"""
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


    def test_family_reservation_min_amount_of_childs(self):
        """When a family reservation has less 
        than 3 reservation childs, its fails"""
        start_date = datetime.now()

        reservation_list = [
            ReservationPerHour(start_date) 
            ,ReservationPerDay(start_date)
        ]

        with self.assertRaises(InvalidAmountOfReservationsOnFamiliyError):
            family_reservation = FamilyReservation(reservation_list)


    def test_cannot_have_final_price_of_not_ended_reservation(self):
        start_date = datetime.now()
        reservation = ReservationPerHour(start_date) 

        with self.assertRaises(ReservationNotEndedError):
            reservation.final_price()


if __name__ == '__main__':
    unittest.main()