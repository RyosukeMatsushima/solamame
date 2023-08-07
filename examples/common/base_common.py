from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *

from examples.common.simulate import simulate


class BaseCommon:
    def is_goal(self, element_number):
        state = self.statesSpace.get_states_from(element_number)
        return state == self.goal_state

    def is_obstacle(self, element_number):
        return False

    def is_edge(self, element_number):
        neigbors = self.statesSpace.get_neighbors_element_number(element_number)
        is_edge = True in [None in i for i in neigbors.values()]
        return is_edge

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = abs(inputs)
        edge_cost = 1.0 if self.is_edge(element_number) else 0.0
        return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100

    def terminal_cost_function(self, element_number):
        return 0.0 if self.is_goal(element_number) else 100.0

    def show_fig_with_path(self, graph_axes, slice_point, state_space, result):
        img = np.array(
            state_space.get_2d_sheet(graph_axes[0], graph_axes[1], slice_point)
        )
        fig2D = Fig2D()

        aspect = 0.2

        fig2D.add_img(
            img,
            [
                state_space.axis_named(graph_axes[0]).min_value,
                state_space.axis_named(graph_axes[0]).max_value,
                state_space.axis_named(graph_axes[1]).min_value,
                state_space.axis_named(graph_axes[1]).max_value,
            ],
            aspect,
        )
        fig2D.add_line(
            "path",
            [
                result[graph_axes[0]].to_numpy(),
                result[graph_axes[1]].to_numpy(),
            ],
        )

        fig2D.show()
