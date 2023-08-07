from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.cart_pole.cart_pole import CartPole

from examples.common.base_common import BaseCommon

from examples.common.simulate import simulate


class Base(BaseCommon):
    def __init__(self):
        self.inputs_set = [
            -1.0,
            0.0,
            1.0,
        ]

        # Define the start and goal points
        self.goal_state = {"x": 0.0, "x_dot": 0.0, "theta": 0.0, "theta_dot": 0.0}
        self.goal = (
            self.goal_state["x"],
            self.goal_state["x_dot"],
            self.goal_state["theta"],
            self.goal_state["theta_dot"],
        )

        # create state space
        self.statesSpace = StatesSpace()
        self.statesSpace.add_axis("x", -2, 2, 2)
        self.statesSpace.add_axis("x_dot", -0.5, 0.5, 5)
        self.statesSpace.add_axis("theta", -0.1, 0.1, 100)
        self.statesSpace.add_axis("theta_dot", -0.2, 0.2, 100)
        self.statesSpace.create()

        self.init_state = {"x": 0.0, "x_dot": 0.0, "theta": 0.0, "theta_dot": 0.1}
        self.model = CartPole(
            (
                self.init_state["x"],
                self.init_state["x_dot"],
                self.init_state["theta"],
                self.init_state["theta_dot"],
            )
        )

        self.dynamics = self.model.dynamics

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = abs(inputs)
        edge_cost = 1.0 if self.is_edge(element_number) else 0.0
        return inputs_norm * 1 + goal_cost * 10 + obstacle_cost * 100 + edge_cost * 100

    def evaluate(self, inputs_space, cost_to_go_space):
        start_time = 0.0
        end_time = 20.0

        result = simulate(
            self.model, inputs_space, self.inputs_set, start_time, end_time
        )

        state_space = cost_to_go_space

        self.show_fig_with_path(
            ["x", "x_dot"],
            {"x": 0, "x_dot": 0, "theta": 0, "theta_dot": 0},
            state_space,
            result,
        )
        self.show_fig_with_path(
            ["theta", "theta_dot"],
            {"x": 0.0, "x_dot": 0, "theta": 0, "theta_dot": 0},
            inputs_space,
            result,
        )
