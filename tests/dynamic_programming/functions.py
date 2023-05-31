import numpy as np

class Functions:

    def __init__(self, state_space, control_inputs_set, time_step, is_goal, is_obstace):
        self.element_count = state_space.element_count
        self.control_inputs_set = control_inputs_set
        self.time_step = time_step
        self.is_goal = is_goal

        obstacle_map = np.array( [ is_obstace(element_number) for element_number in range(self.element_count) ] )
        self.obstacle_cost_map = np.where(obstacle_map, 100.0, 0.0)

        control_inputs_norm_set = [ sum( [ control_input ** 2 for control_input in control_inputs ] ) ** 0.5 for control_inputs in control_inputs_set ]
        self.control_inputs_cost_map_set = [ np.ones(self.element_count) * (control_inputs_norm) for control_inputs_norm in control_inputs_norm_set ]

        self.edgi_cost_map = np.zeros(self.element_count)
        for i in range(self.element_count):
            neigbors = state_space.get_neighbors_element_number(i)
            is_edgi = True in [ None in i for i in neigbors.values()]

            if is_edgi:
                self.edgi_cost_map[i] = 100

    def terminal_cost_map(self):
        goal_map = np.array( [ self.is_goal(element_number) for element_number in range(self.element_count) ] )
        return np.where(goal_map, 0.0, 100.0)

    def stage_cost_map(self, control_inputs):
        control_inputs_cost_map = self.control_inputs_cost_map_set[ self.control_inputs_set.index(control_inputs) ]
        return self.obstacle_cost_map + self.edgi_cost_map + control_inputs_cost_map

