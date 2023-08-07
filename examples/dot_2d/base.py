from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.dot_2d.dot_2d import Dot2D

from examples.common.simulate import simulate

from examples.common.base_common import BaseCommon


class Base(BaseCommon):
    def __init__(self):
        self.inputs_set = [
            (0, 0),
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
        self.goal_state = {"x": 4, "y": 2}
        self.goal = (self.goal_state["x"], self.goal_state["y"])

        # create state space
        self.statesSpace = StatesSpace()
        self.statesSpace.add_axis("x", 0, 10, 3)
        self.statesSpace.add_axis("y", 0, 8, 3)
        self.statesSpace.create()

        self.init_state = {"x": 3, "y": 7}
        self.model = Dot2D((self.init_state["x"], self.init_state["y"]))
        self.dynamics = self.model.dynamics

    def is_obstacle(self, element_number):
        state = self.statesSpace.get_states_from(element_number)

        if 1 < state["x"] < 3 and 5 < state["y"] < 6:
            return True
        if 4 < state["x"] < 7 and 5 < state["y"] < 6:
            return True
        if 2 < state["x"] < 5 and 3 < state["y"] < 4:
            return True

        return False

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

        fig2D = Fig2D()

        # TODO: modify figures
        state_space = cost_to_go_space

        # state_space.values = functions.obstacle_cost_map

        fig2D.add_img(np.array(state_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})).T)
        fig2D.add_line(
            "path",
            [
                result["X"].to_numpy() * state_space.axis_named("x").resolution,
                result["Y"].to_numpy() * state_space.axis_named("y").resolution,
            ],
        )

        input_index = inputs_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})
        input_vector_space = np.array(
            [[self.inputs_set[index] for index in l] for l in input_index]
        )
        fig2D.add_vector_field("inputs_space", input_vector_space)

        fig2D.show()

        print(result["X"].to_numpy())
