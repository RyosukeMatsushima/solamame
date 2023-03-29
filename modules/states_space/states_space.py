#!/usr/bin/env python

import numpy as np

from modules.states_space.axis import Axis


class StatesSpace:
    def __init__(self):
        self.axes = []
        self.element_count = None
        self.values = None

    def add_axis(self, name, min_value, max_value, resolution):
        self.axes.append(Axis(name, min_value, max_value, resolution))

    def create(self):
        self.element_count = 1
        for axis in self.axes:
            self.element_count *= axis.length

        self.values = [0.0] * self.element_count

    # def gradient(self, states):

    def get_element_number(self, states):
        element_number = 0

        unit_length = 1

        for axis in self.axes:
            element_number += axis.get_point(states[axis.name]) * unit_length
            unit_length *= axis.length

        return element_number

    def set_value(self, element_number, value):
        self.values[element_number] = value

    def get_states_from(self, element_number):
        states = {}

        unit_length = self.element_count
        pointer = element_number

        for axis in self.axes:
            axis_pointer = pointer % axis.length
            pointer = (pointer - axis_pointer) / axis.length
            states.update({axis.name: axis.get_value(axis_pointer)})

        return states

    def get_gradient(self, element_number):
        unit_length = 1

        gradient_vector = []

        for axis in self.axes:
            # check in range
            upper_point = element_number + unit_length
            lower_point = element_number - unit_length

            gradient = 0

            if lower_point < 0:
                upper_value = self.values[element_number + unit_length]
                value = self.values[element_number]
                gradient = (upper_value - value) / axis.resolution

            elif lower_point >= self.element_count:
                lower_value = self.values[element_number - unit_length]
                value = self.values[element_number]
                gradient = (value - lower_value) / axis.resolution

            else:
                upper_value = self.values[element_number + unit_length]
                lower_value = self.values[element_number - unit_length]
                gradient = (upper_value - lower_value) / (axis.resolution * 2)

            gradient_vector.append(gradient)
            unit_length *= axis.length

        return np.array(gradient_vector)
