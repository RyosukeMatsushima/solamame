from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.single_pendulum.single_pendulum import SinglePendulum

from examples.single_pendulum.simulate import simulate


inputs_set = [
    0,
    -0.2,
    -0.1,
    0.1,
    0.2,
]

# Define the start and goal points
goal = (0, 0)

# create state space
statesSpace = StatesSpace()
statesSpace.add_axis("x", -1, 7, 10)
statesSpace.add_axis("x_dot", -30, 30, 2)
statesSpace.create()

dynamics = SinglePendulum([0.0, 0.0]).dynamics


def is_goal(element_number):
    state = statesSpace.get_states_from(element_number)
    return state["x"] == goal[0] and state["x_dot"] == goal[1]


def is_obstacle(element_number):
    return False


def is_edge(element_number):
    neigbors = statesSpace.get_neighbors_element_number(element_number)
    is_edge = True in [None in i for i in neigbors.values()]
    return is_edge


def stage_cost_function(element_number, inputs):
    goal_cost = 0.0 if is_goal(element_number) else 1.0
    obstacle_cost = 1.0 if is_obstacle(element_number) else 0.0
    inputs_norm = abs(inputs)
    edge_cost = 1.0 if is_edge(element_number) else 0.0
    return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100


def terminal_cost_function(element_number):
    return 0.0 if is_goal(element_number) else 100.0


def evaluate(inputs_space, cost_to_go_space):
    start_time = 0.0
    end_time = 20.0
    init_state = {"x": 3.14, "x_dot": 0}
    
    result = simulate(
        inputs_space, inputs_set, start_time, end_time, init_state
    )
    
    state_space = cost_to_go_space
    img = np.array(inputs_space.get_2d_sheet("x_dot", "x", {"x": 0, "x_dot": 0}))
    show_fig_with_path(img, state_space, result)

    img = np.array(state_space.get_2d_sheet("x_dot", "x", {"x": 0, "x_dot": 0}))
    show_fig_with_path(img, state_space, result)


    print(result["X"].to_numpy())

def show_fig_with_path(img, state_space, result):
    fig2D = Fig2D()
    
    # TODO: modify figures
    
    #state_space.values = functions.obstacle_cost_map

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
