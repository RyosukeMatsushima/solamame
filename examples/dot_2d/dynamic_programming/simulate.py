import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from submodules.physics_simulator.dot_2d.dot_2d import Dot2D


def simulate(inputs_space, inputs_set, start_time, end_time, init_state):
    X = init_state["x"]
    Y = init_state["y"]
    init_state = (X, Y)
    dot2D = Dot2D(init_state)

    time = start_time
    dt = 10 ** (-2)
    max_step = int((end_time - start_time) / dt)

    df = pd.DataFrame(columns=["time", "X", "Y"])

    axes_name = [axis.name for axis in inputs_space.axes]

    # def add_data(df):
    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + dot2D.state
        print(time)

        state = {axes_name[i]: s for i, s in enumerate(dot2D.state)}
        element_number = inputs_space.get_element_number(state)
        dot2D.input = inputs_set[inputs_space.values[element_number]]
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        dot2D.step(dt)

    df.to_csv("./data.csv", index=False)
    df.plot(x="X", y="Y")
    df.plot(x="time", y="X")
    df.plot(x="time", y="Y")
    plt.show()

    return df
