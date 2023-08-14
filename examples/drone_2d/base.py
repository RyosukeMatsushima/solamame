from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.drone_2d.drone_2d import Drone2D

from examples.common.base_common import BaseCommon

from examples.common.simulate import simulate


class Base(BaseCommon):
    def __init__(self):
        self.inputs_set = [
            (1, 1),
            (1, 15),
            (15, 1),
            (15, 15),
        ]

        # Define the start and goal points
        self.goal_state = {
            "X": 0.0,
            "Z": 0.0,
            "theta": 0.0,
            "x_dot": 0.0,
            "z_dot": 0.0,
            "theta_dot": 0.0,
        }

        self.goal = (
            self.goal_state["X"],
            self.goal_state["Z"],
            self.goal_state["theta"],
            self.goal_state["x_dot"],
            self.goal_state["z_dot"],
            self.goal_state["theta_dot"],
        )

        # create state space
        self.statesSpace = StatesSpace()
        self.statesSpace.add_axis("X", -0.5, 0.5, 10)
        self.statesSpace.add_axis("Z", -0.5, 0.5, 10)
        self.statesSpace.add_axis("theta", -0.5, 0.5, 10)
        self.statesSpace.add_axis("x_dot", -0.5, 0.5, 4)
        self.statesSpace.add_axis("z_dot", -0.5, 0.5, 4)
        self.statesSpace.add_axis("theta_dot", -1, 1, 2)
        self.statesSpace.create()

        self.init_state = {
            "X": 0.3,
            "Z": 0.0,
            "theta": 0.0,
            "x_dot": 0.0,
            "z_dot": 0.0,
            "theta_dot": 0.0,
        }

        self.model = Drone2D(tuple(self.init_state.values()))

        self.dynamics = self.model.dynamics

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = sum([i**2 for i in inputs]) ** 0.5
        edge_cost = 1.0 if self.is_edge(element_number) else 0.0
        return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100

    def evaluate(self, inputs_space, cost_to_go_space):
        start_time = 0.0
        end_time = 20.0

        result = simulate(
            self.model, inputs_space, self.inputs_set, start_time, end_time
        )

        state_space = cost_to_go_space
        self.show_fig_with_path(
            ["X", "Z"],
            self.goal_state,
            state_space,
            result,
        )
