from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from modules.states_space.transition_matrix import *

from examples.common.simulate import simulate


class BaseCommon:
    def is_goal(self, element_number):
        state = self.statesSpace.get_states_from(element_number)
        return state == self.goal_state

    def is_obstacle(self, element_number):
        return False

    def is_edge(self, element_number):
        state = self.statesSpace.get_states_from(element_number)

        # return 1.0 if each state is out of range
        for key in state.keys():
            axis = self.statesSpace.axis_named(key)
            if state[key] < axis.min_value + 2 / axis.resolution:
                return 1.0
            if axis.max_value - 2 / axis.resolution < state[key]:
                return 1.0
        return 0.0

    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = abs(inputs)
        edge_cost = 1.0 if self.is_edge(element_number) else 0.0
        return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100

    def get_stage_cost_map_set(self, time_step):
        stage_cost_map_set = np.array(
            [self.stage_cost_map(inputs, time_step) for inputs in self.inputs_set]
        )
        return stage_cost_map_set

    def stage_cost_map(self, inputs, time_step):
        return (
            np.array(
                [
                    self.stage_cost_function(element_number, inputs)
                    for element_number in range(self.statesSpace.element_count)
                ]
            )
            * time_step
        )

    def transition_function(self, element_number, inputs):
        states = list(self.statesSpace.get_states_from(element_number).values())
        return self.dynamics(states, inputs)

    def get_transition_matrix_set(self, time_step):
        transition_matrix_set = get_transition_matrix(
            self.statesSpace, self.transition_function, self.inputs_set, time_step
        )
        return transition_matrix_set

    def terminal_cost_function(self, element_number):
        return 0.0 if self.is_goal(element_number) else 100.0

    def show_fig_with_path(
        self, graph_axes, slice_point, state_space, result, aspect=1
    ):
        img = np.array(
            state_space.get_2d_sheet(graph_axes[0], graph_axes[1], slice_point)
        )
        fig2D = Fig2D()

        x_axis = state_space.axis_named(graph_axes[0])
        y_axis = state_space.axis_named(graph_axes[1])

        fig2D.add_img(
            img.T,
            [
                x_axis.min_value - 1 / x_axis.resolution * 0.5,
                x_axis.max_value + 1 / x_axis.resolution * 0.5,
                y_axis.min_value - 1 / y_axis.resolution * 0.5,
                y_axis.max_value + 1 / y_axis.resolution * 0.5,
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
