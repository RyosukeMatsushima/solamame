from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.dot_2d.dot_2d import Dot2D

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
        self.goal_state = {"x": 1, "y": 1}
        self.goal = (self.goal_state["x"], self.goal_state["y"])

        # create state space
        self.statesSpace = StatesSpace()
        self.statesSpace.add_axis("x", 0, 10, 10)
        self.statesSpace.add_axis("y", 0, 8, 10)
        self.statesSpace.create()

        self.init_state = {"x": 9, "y": 7}
        self.model = Dot2D((self.init_state["x"], self.init_state["y"]))
        self.dynamics = self.model.dynamics

    def is_obstacle_0(self, element_number):
        state = self.statesSpace.get_states_from(element_number)

        if 2 < state["x"] < 7 and 3 < state["y"] < 6:
            return 1.0

        return 0.0

    def is_obstacle_1(self, element_number):
        state = self.statesSpace.get_states_from(element_number)

        if 3 < state["x"] < 8 and 2 < state["y"] < 5:
            return 1.0

        return 0.0 

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = self.is_obstacle_0(element_number) + self.is_obstacle_1(element_number)
        inputs_norm = sum([i**2 for i in inputs]) ** 0.5
        edge_cost = self.is_edge(element_number)
        return inputs_norm * 0.5 + goal_cost * 1 + obstacle_cost * 10 + edge_cost * 1000

    def evaluate(self, inputs_space, cost_to_go_space):
        start_time = 0.0
        end_time = 20.0

        result = simulate(
            self.model, inputs_space, self.inputs_set, start_time, end_time
        )

        # TODO: modify figures
        state_space = cost_to_go_space
        self.show_fig_with_path(
            ["x", "y"],
            {"x": 0.0, "y": 0.0},
            state_space,
            result,
        )
