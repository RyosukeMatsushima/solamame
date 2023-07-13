from modules.states_space.states_space import StatesSpace
from modules.tools.fig_2d import *
from submodules.physics_simulator.dot_2d.dot_2d import Dot2D

from examples.dot_2d.simulate import simulate


inputs_set = [
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
goal = (4, 2)

# create state space
statesSpace = StatesSpace()
statesSpace.add_axis("x", 0, 10, 3)
statesSpace.add_axis("y", 0, 8, 3)
statesSpace.create()

dynamics = Dot2D([0.0, 0.0]).dynamics


def is_goal(element_number):
    state = statesSpace.get_states_from(element_number)
    return state["x"] == goal[0] and state["y"] == goal[1]


def is_obstacle(element_number):
    state = statesSpace.get_states_from(element_number)

    if 1 < state["x"] < 3 and 5 < state["y"] < 6:
        return True
    if 4 < state["x"] < 7 and 5 < state["y"] < 6:
        return True
    if 2 < state["x"] < 5 and 3 < state["y"] < 4:
        return True

    return False


def is_edge(element_number):
    neigbors = statesSpace.get_neighbors_element_number(element_number)
    is_edge = True in [None in i for i in neigbors.values()]
    return is_edge


def stage_cost_function(element_number, inputs):
    goal_cost = 0.0 if is_goal(element_number) else 1.0
    obstacle_cost = 1.0 if is_obstacle(element_number) else 0.0
    inputs_norm = sum([ i ** 2 for i in inputs ]) ** 0.5
    edge_cost = 1.0 if is_edge(element_number) else 0.0
    return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 100 + edge_cost * 100


def terminal_cost_function(element_number):
    return 0.0 if is_goal(element_number) else 100.0


def evaluate(inputs_space, cost_to_go_space):
    start_time = 0.0
    end_time = 20.0
    init_state = {"x": 3, "y": 7}
    
    result = simulate(
        inputs_space, inputs_set, start_time, end_time, init_state
    )
    
    fig2D = Fig2D()
    
    # TODO: modify figures
    state_space = cost_to_go_space
    
    #state_space.values = functions.obstacle_cost_map
    
    fig2D.add_img(np.array(state_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})).T)
    fig2D.add_line(
        "path",
        [
            result["X"].to_numpy() * state_space.axis_named("x").resolution,
            result["Y"].to_numpy() * state_space.axis_named("y").resolution,
        ],
    )
    
    
    input_index = inputs_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})
    input_vector_space = np.array([[inputs_set[index] for index in l] for l in input_index])
    fig2D.add_vector_field("inputs_space", input_vector_space)

    fig2D.show()

    print(result["X"].to_numpy())
