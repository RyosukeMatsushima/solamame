#!/usr/bin/env python

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


"""
            axis_point = int(pointer / self.axes[axis_name].length)
            pointer -= 

            unit_length = unit_length / self.axes[axis_name].length #this should be int
            pointer = int(pointer / unit_length)
"""
