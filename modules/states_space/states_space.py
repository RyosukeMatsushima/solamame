#!/usr/bin/env python

import numpy as np
import json

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

        self.values = np.zeros(self.element_count)

    def save(self, path_to_dir):
        axes_info = [axis.get_info() for axis in self.axes]

        with open(path_to_dir + "/axes_info.json", "w") as f:
            json.dump(axes_info, f)

        np.save(path_to_dir + "/values.npy", self.values)

    def read(self, path_to_dir):
        self.__init__()

        with open(path_to_dir + "/axes_info.json") as f:
            axes_info = json.load(f)

            for axis_info in axes_info:
                self.add_axis(
                    axis_info["name"],
                    axis_info["min_value"],
                    axis_info["max_value"],
                    axis_info["resolution"],
                )

        self.create()

        self.values = np.load(path_to_dir + "/values.npy")

    def get_element_number(self, states):
        element_number = 0

        unit_length = 1

        for axis in self.axes:
            element_number += axis.get_point(states[axis.name]) * unit_length
            unit_length *= axis.length

        return element_number

    # return {"axis_name": [lower_neighbor_element_number, upper_neighbor_element_number], ...}
    def get_neighbors_element_number(self, element_number):
        neighbors = {}

        unit_length = 1
        for axis in self.axes:
            exponent_value = (element_number) % (axis.length * unit_length)

            lower_number = (
                element_number - unit_length if exponent_value >= unit_length else None
            )
            upper_number = (
                element_number + unit_length
                if (exponent_value < (axis.length - 1) * unit_length)
                else None
            )

            neighbors.update({axis.name: [lower_number, upper_number]})

            unit_length *= axis.length

        return neighbors

    def add_value(self, element_number, value):
        self.values[element_number] += value

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

            if element_number % (axis.length * unit_length) < unit_length:
                upper_value = self.values[element_number + unit_length]
                value = self.values[element_number]
                gradient = (upper_value - value) / axis.resolution

            elif (
                element_number % (axis.length * unit_length)
                >= (axis.length - 1) * unit_length
            ):
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

    def axis_named(self, name):
        return [axis for axis in self.axes if axis.name == name][0]

    def get_2d_sheet(self, x_axis_name, y_axis_name, states):
        x_axis = self.axis_named(x_axis_name)
        y_axis = self.axis_named(y_axis_name)

        # TODO: chenge to ndarray.
        sheet = np.zeros((x_axis.length, y_axis.length)).tolist()

        for x_point in range(x_axis.length):
            for y_point in range(y_axis.length):
                states[x_axis_name] = x_axis.get_value(x_point)
                states[y_axis_name] = y_axis.get_value(y_point)

                element_number = self.get_element_number(states)

                sheet[x_point][y_point] = self.values[element_number]

        return sheet

    def get_axis_velues(self, axis_name, states):
        axis = self.axis_named(axis_name)
        axis_values = np.zeros(axis.length)

        for point in range(axis.length):
            states[axis_name] = axis.get_value(point)
            element_number = self.get_element_number(states)
            axis_values[point] = self.values[point]

        return axis_values
