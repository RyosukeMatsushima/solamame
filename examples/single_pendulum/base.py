from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.single_pendulum.single_pendulum import SinglePendulum

from examples.common.base_common import BaseCommon

from examples.common.simulate import simulate


class Base(BaseCommon):
    def __init__(self):
        self.inputs_set = [
            0,
            -0.2,
            0.2,
        ]

        # Define the start and goal points
        self.goal_state = {"x": 0.0, "x_dot": 0.0}
        self.goal = (self.goal_state["x"], self.goal_state["x_dot"])

        # create state space
        self.statesSpace = StatesSpace()
        self.statesSpace.add_axis("x", -1, 7, 10)
        self.statesSpace.add_axis("x_dot", -30, 30, 2)
        self.statesSpace.create()

        self.init_state = {"x": 3.1416, "x_dot": 0}
        self.model = SinglePendulum((self.init_state["x"], self.init_state["x_dot"]))

        self.dynamics = self.model.dynamics

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = abs(inputs)
        edge_cost = self.is_edge(element_number)
        return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 0 + edge_cost * 100

    def evaluate(self, inputs_space, cost_to_go_space):
        start_time = 0.0
        end_time = 5.0

        result = simulate(
            self.model, inputs_space, self.inputs_set, start_time, end_time
        )

        state_space = cost_to_go_space
        state_space.values = np.where(state_space.values < 2.5, state_space.values, 2.5)

        self.show_fig_with_path(
            ["x", "x_dot"],
            {"x": 0.0, "x_dot": 0.0},
            state_space,
            result,
            aspect=0.1,
            save_path="single_pendulum_path_with_cost_function.png",
            label="cost function V(x)",
            xlabel=r"$\theta$ [rad]",
            ylabel=r"$\dot{\theta}$ [rad/s]",
        )

        self.show_fig_with_path(
            ["x", "x_dot"],
            {"x": 0.0, "x_dot": 0.0},
            inputs_space,
            result,
            aspect=0.1,
            save_path="single_pendulum_path_with_inputs.png",
            label="inputs u(x)",
            xlabel=r"$\theta$ [rad]",
            ylabel=r"$\dot{\theta}$ [rad/s]",
        )
