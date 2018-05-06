#!/usr/bin/env python

import unittest
from datetime import datetime, timedelta
from model import (
    BikeReservationPerHour, 
    BikeReservationPerDay, 
    BikeReservationPerWeek,
    FamilyBikeReservation,
    COST_PER_DAY, 
    COST_PER_HOUR, 
    COST_PER_WEEK, 
    FAMILY_DISCOUNT,
    InvalidAmountOfBikeReservationsOnFamiliyError,
    BikeReservationNotEndedError
)


class TestBikeReservation(unittest.TestCase):


    def test_when_rent_a_bike_per_hour_the_price_is_per_each_hour(self):
        start_date = datetime.now()
        reservation = BikeReservationPerHour(start_date)
        reserved_hours = 3
        end_date = start_date + timedelta(hours=reserved_hours)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_HOUR * reserved_hours, 
            reservation.final_price()
        )

    def test_when_rent_a_bike_per_day_the_price_is_per_each_day(self):
        start_date = datetime.now()
        reservation = BikeReservationPerDay(start_date)
        reserved_days = 5
        end_date = start_date + timedelta(days=reserved_days)
        reservation.end(end_date)
        self.assertEqual(
            COST_PER_DAY * reserved_days, 
            reservation.final_price()
        )

    def test_when_rent_a_bike_per_week_the_price_is_per_each_week(self):
        start_date = datetime.now()
        reservation = BikeReservationPerWeek(start_date)
        
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

        reservation_hour = BikeReservationPerHour(start_date)
        reservation_day = BikeReservationPerDay(start_date)
        reservation_week = BikeReservationPerWeek(start_date)
        
        family_reservation = FamilyBikeReservation(
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
            BikeReservationPerHour(start_date) 
            ,BikeReservationPerDay(start_date)
            ,BikeReservationPerDay(start_date)
            ,BikeReservationPerWeek(start_date)
            ,BikeReservationPerWeek(start_date)
            ,BikeReservationPerWeek(start_date)
        ]

        with self.assertRaises(InvalidAmountOfBikeReservationsOnFamiliyError):
            family_reservation = FamilyBikeReservation(reservation_list)


    def test_family_reservation_min_amount_of_childs(self):
        """When a family reservation has less 
        than 3 reservation childs, its fails"""
        start_date = datetime.now()

        reservation_list = [
            BikeReservationPerHour(start_date) 
            ,BikeReservationPerDay(start_date)
        ]

        with self.assertRaises(InvalidAmountOfBikeReservationsOnFamiliyError):
            family_reservation = FamilyBikeReservation(reservation_list)


    def test_cannot_have_final_price_of_not_ended_reservation(self):
        start_date = datetime.now()
        reservation = BikeReservationPerHour(start_date) 

        with self.assertRaises(BikeReservationNotEndedError):
            reservation.final_price()



    
    def test_recursive_family_reservation(self):
        start_date = datetime.now()

        reservation_hour = BikeReservationPerHour(start_date)
        reservation_day = BikeReservationPerDay(start_date)
        reservation_week = BikeReservationPerWeek(start_date)
        
        family_reserve_child, prima_value = _family_child_reserve(start_date)
        

        family_reservation = FamilyBikeReservation(
            [reservation_hour, reservation_day, reservation_week, 
            family_reserve_child]
        )

        reservation_hour.end(start_date + timedelta(hours=12))
        reservation_day.end(start_date + timedelta(days=5))
        reservation_week.end(start_date + timedelta(days=24))

        not_discounted_price =  (COST_PER_DAY * 5) + (COST_PER_WEEK * 4) \
            + (COST_PER_HOUR * 12) + prima_value
        discount = (FAMILY_DISCOUNT * not_discounted_price) / 100.0
        expected_cost = not_discounted_price - discount

        self.assertEqual(
            expected_cost,
            family_reservation.final_price()
        )


def _family_child_reserve(start_date):
    """Extract method for test"""
    
    reservation_hour_prima = BikeReservationPerHour(start_date)
    reservation_day_prima = BikeReservationPerDay(start_date)
    reservation_week_prima = BikeReservationPerWeek(start_date)

    family_reservation_child = FamilyBikeReservation(
        [reservation_day_prima, reservation_hour_prima, 
            reservation_week_prima]
    )

    reservation_hour_prima.end(start_date + timedelta(hours=3))
    reservation_day_prima.end(start_date + timedelta(days=10))
    reservation_week_prima.end(start_date + timedelta(days=30))

    prima_value_raw = (COST_PER_HOUR * 3) + \
        (COST_PER_DAY * 10) + (COST_PER_WEEK * 5)
    prima_discount = (FAMILY_DISCOUNT * prima_value_raw) / 100.0
    prima_value = prima_value_raw - prima_discount

    return family_reservation_child, prima_value


if __name__ == '__main__':
    unittest.main()