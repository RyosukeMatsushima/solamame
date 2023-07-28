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
            -0.1,
            0.1,
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
        
        self.init_state = {"x": 3.14, "x_dot": 0}
        self.model = SinglePendulum((self.init_state["x"], self.init_state["x_dot"]))
        
        self.dynamics = self.model.dynamics
    
    
    def stage_cost_function(self, element_number, inputs):
        goal_cost = 0.0 if self.is_goal(element_number) else 1.0
        obstacle_cost = 1.0 if self.is_obstacle(element_number) else 0.0
        inputs_norm = abs(inputs)
        edge_cost = 1.0 if self.is_edge(element_number) else 0.0
        return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100
    
    
    def evaluate(self, inputs_space, cost_to_go_space):
        start_time = 0.0
        end_time = 20.0
        
        result = simulate(
            self.model, inputs_space, self.inputs_set, start_time, end_time
        )
        
        state_space = cost_to_go_space
        img = np.array(inputs_space.get_2d_sheet("x_dot", "x", {"x": 0, "x_dot": 0}))
        self.show_fig_with_path(img, state_space, result)
    
        img = np.array(state_space.get_2d_sheet("x_dot", "x", {"x": 0, "x_dot": 0}))
        self.show_fig_with_path(img, state_space, result)
    
        print(result["X"].to_numpy())
    
    
    def show_fig_with_path(self, img, state_space, result):
        fig2D = Fig2D()
    
        aspect = 0.2
    
        fig2D.add_img(
            img,
            [
            state_space.axis_named("x").min_value,
            state_space.axis_named("x").max_value,
            state_space.axis_named("x_dot").min_value,
            state_space.axis_named("x_dot").max_value,
            ],
            aspect
            )
        fig2D.add_line(
            "path",
            [
                result["X"].to_numpy(),
                result["Y"].to_numpy(),
            ],
        )
    
        fig2D.show()
