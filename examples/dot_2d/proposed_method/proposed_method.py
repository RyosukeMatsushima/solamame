import numpy as np

from modules.proposed_method.find_cost_to_go import FindCostToGo
from modules.states_space.states_space import StatesSpace
from modules.states_space.transition_matrix import *

from submodules.physics_simulator.dot_2d.dot_2d import Dot2D
from examples.dot_2d.dynamic_programming.simulate import simulate

# TODO: remove
from modules.tools.fig_2d import *

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

time_resolution = 0.01
min_cost = 0
max_cost = 300

# create state space
proballistic_space = StatesSpace()

proballistic_space.add_axis("x", 0, 10, 10)
proballistic_space.add_axis("y", 0, 8, 10)

proballistic_space.create()

def is_goal(element_number):
    state = proballistic_space.get_states_from(element_number)
    return state["x"] == goal[0] and state["y"] == goal[1]

def is_obstacle(element_number):
    state = proballistic_space.get_states_from(element_number)

    if 1 < state["x"] < 3 and 5 < state["y"] < 6:
        return True
    if 4 < state["x"] < 7 and 5 < state["y"] < 6:
        return True
    if 2 < state["x"] < 5 and 3 < state["y"] < 4:
        return True

    return False

def stage_cost_function(element_number, inputs):
    goal_cost = 0.0 if is_goal(element_number) else 1.0
    obstacle_cost = 1.0 if is_obstacle(element_number) else 0.0
    inputs_norm = sum([ i ** 2 for i in inputs ]) ** 0.5
    return inputs_norm * 1 + goal_cost * 1 + obstacle_cost * 300 + 1

def transition_function(element_number, inputs):
    states = list(proballistic_space.get_states_from(element_number).values())
    stage_cost = stage_cost_function(element_number, inputs)
    return Dot2D([0.0, 0.0]).dynamics(states, inputs) / stage_cost

# create transition matrix
print("calculate transition_matrix_set")
transition_matrix_set = get_transition_matrix(
    proballistic_space, transition_function, inputs_set, time_resolution
)

goal_element_number = proballistic_space.get_element_number({"x": goal[0], "y": goal[1]})
proballistic_space.values[goal_element_number] = 1
print(transition_matrix_set)
print(len(transition_matrix_set))

findCostToGo = FindCostToGo(
    proballistic_space,
    transition_matrix_set,
    time_resolution,
    max_cost,
    min_cost
)


print("start findCostToGo")
findCostToGo.calculate()

start_time = 0.0
end_time = 20.0
init_state = {"x": 3, "y": 7}

result = simulate(
    findCostToGo.inputs_space, inputs_set, start_time, end_time, init_state
)

fig2D = Fig2D()

# TODO: modify figures
state_space = findCostToGo.cost_to_go_space

#state_space.values = functions.obstacle_cost_map

fig2D.add_img(np.array(state_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})).T)
fig2D.add_line(
    "path",
    [
        result["X"].to_numpy() * state_space.axis_named("x").resolution,
        result["Y"].to_numpy() * state_space.axis_named("y").resolution,
    ],
)


input_index = findCostToGo.inputs_space.get_2d_sheet("x", "y", {"x": 0, "y": 0})
input_vector_space = np.array([[inputs_set[index] for index in l] for l in input_index])
fig2D.add_vector_field("inputs_space", input_vector_space)

fig2D.show()

print(result["X"].to_numpy())
