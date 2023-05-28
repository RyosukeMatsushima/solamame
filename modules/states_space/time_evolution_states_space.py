#!/usr/bin/env python

import copy

from modules.states_space.axis import Axis


class TimeEvolutionStatesSpace:
    def __init__(self, states_space, time_resolution, start_time, finish_time):
        self.time_axis = Axis("time", start_time, finish_time, time_resolution)
        self.values = [None] * self.time_axis.length
        self.init_states_space = states_space

    def set_value(self, time, values):
        point = self.time_axis.get_point(time)
        self.values[point] = values

    def get_state_space(self, time):
        states_space = copy.deepcopy(self.init_states_space)
        states_space.values = self.values[self.time_axis.get_point(time)]
        print(self.values)
        print(self.values[self.time_axis.get_point(time)])
        return states_space

