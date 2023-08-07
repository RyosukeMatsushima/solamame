#!/usr/bin/env python


class Axis:
    def __init__(self, name, min_value, max_value, resolution):
        self.name = name

        min_point = self.get_min_point(min_value, resolution)
        max_point = self.get_max_point(max_value, resolution)
        self.min_value = min_point / resolution
        self.max_value = max_point / resolution
        self.length = max_point - min_point + 1

        self.resolution = resolution

    def get_min_point(self, min_value, resolution):
        min_point = int(min_value * resolution)
        if min_value < 0 and min_point / resolution != min_value:
            min_point -= 1
        return min_point

    def get_max_point(self, max_value, resolution):
        max_point = int(max_value * resolution)
        if max_value > 0 and max_point / resolution != max_value:
            max_point += 1
        return max_point

    # count point from 0.
    def get_value(self, point):
        return self.min_value + point / self.resolution

    def get_point(self, value):
        if value < self.min_value:
            raise ValueError("The input value: {} is less than min value: {}".format(value, self.min_value))
        if self.max_value < value:
            raise ValueError("The input value: {} is more than max value: {}".format(value, self.min_value))
        return int((value - self.min_value) * self.resolution + 0.5)

    def get_info(self):
        return {
            "name": self.name,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "resolution": self.resolution,
        }
