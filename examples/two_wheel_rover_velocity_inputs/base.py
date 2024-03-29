from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.two_wheel_rover_velocity_inputs.two_wheel_rover_velocity_inputs import (
    TwoWheelRover,
)

from examples.common.simulate import simulate

from examples.common.base_common import BaseCommon


class Base(BaseCommon):
    def __init__(self):
        self.inputs_set = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        # Define the start and goal points
        self.goal_state = {"x": 0, "y": 0, "yaw": 0}
        self.goal = (self.goal_state["x"], self.goal_state["y"], self.goal_state["yaw"])

        # create state space
        self.statesSpace = StatesSpace()
        self.statesSpace.add_axis("x", -1, 2, 10)
        self.statesSpace.add_axis("y", -1, 2, 10)
        self.statesSpace.add_axis("yaw", -7, 7, 10)
        self.statesSpace.create()

        self.init_state = {"x": 1.5, "y": 1.5, "yaw": 4}
        self.model = TwoWheelRover(
            (self.init_state["x"], self.init_state["y"], self.init_state["yaw"])
        )
        self.dynamics = self.model.dynamics

    def is_obstacle(self, element_number):
        state = self.statesSpace.get_states_from(element_number)

        #        if 1 < state["x"] < 3 and 5 < state["y"] < 6:
        #            return True
        #        if 4 < state["x"] < 7 and 5 < state["y"] < 6:
        #            return True
        #        if 2 < state["x"] < 5 and 3 < state["y"] < 4:
        #            return True

        return False

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = sum([i**2 for i in inputs]) ** 0.5
        edge_cost = self.is_edge(element_number)
        return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100

    def evaluate(self, inputs_space, cost_to_go_space):
        start_time = 0.0
        end_time = 20.0

        result = simulate(
            self.model, inputs_space, self.inputs_set, start_time, end_time
        )

        state_space = cost_to_go_space

        self.show_fig_with_path(
            ["x", "y"],
            {"x": 0, "y": 0, "yaw": 0},
            state_space,
            result,
        )
        self.show_fig_with_path(
            ["x", "yaw"],
            {"x": 0, "y": 0, "yaw": 0},
            inputs_space,
            result,
        )
