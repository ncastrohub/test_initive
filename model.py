#!/usr/bin/env python

import datetime
from abc import ABCMeta, abstractmethod
import math

COST_PER_HOUR = 5
COST_PER_DAY = 20
COST_PER_WEEK = 60
FAMILY_DISCOUNT = 30

class AbstractReservation(metaclass=ABCMeta):
    """Abstract for reservation final_price"""
    
    @abstractmethod
    def final_price(self):
        pass


class ReservationLeaf(AbstractReservation, metaclass=ABCMeta):
    """Abstract for reservation final_price"""
    def __init__(self, start_date):
        self.start_date = start_date

    def _get_time_delta(self):
        delta = self.end_date - self.start_date
        return delta

    def end(self, end_date):
        self.end_date = end_date

    def final_price(self):
        try:
            return self._leaf_final_price()
        except AttributeError as error:
            raise ReservationNotEndedError()


    @abstractmethod
    def _leaf_final_price(self):
        pass


class FamilyReservation(AbstractReservation):
    def __init__(self, child_reservations):
        if len(child_reservations) > 5 or len(child_reservations) < 3:
            raise InvalidAmountOfReservationsOnFamiliyError()
        self.child_reservations = child_reservations

    def final_price(self):
        collector = 0
        for reservation in self.child_reservations:
            collector += reservation.final_price()
        discount = (FAMILY_DISCOUNT * collector) / 100.0
        return collector - discount



class ReservationPerHour(ReservationLeaf):
    """ A reservation that calculates its price by hour """

    def _leaf_final_price(self):
        delta = self._get_time_delta()
        hours = delta.days * 24 + delta.seconds / 3600.0
        return hours * COST_PER_HOUR


class ReservationPerDay(ReservationLeaf):
    """ A reservation that calculates its price by day """

    def _leaf_final_price(self):
        delta = self._get_time_delta()
        hours = delta.days
        return hours * COST_PER_DAY


class ReservationPerWeek(ReservationLeaf):
    """ A reservation that calculates its price by day """

    def _leaf_final_price(self):
        # When a week starts, cost a full week
        delta = self._get_time_delta()
        weeks = math.ceil(delta.days / 7)
        return weeks * COST_PER_WEEK


class ReservationNotEndedError(Exception):
    pass

class InvalidAmountOfReservationsOnFamiliyError(Exception):
    pass