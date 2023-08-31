import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def simulate(model, inputs_space, inputs_set, start_time, end_time):
    time = start_time
    dt = 10 ** (-3)
    max_step = int((end_time - start_time) / dt)

    df = pd.DataFrame(columns=["time"] + [axis.name for axis in inputs_space.axes])

    axes_name = [axis.name for axis in inputs_space.axes]

    # def add_data(df):
    for s in range(0, max_step):
        time = s * dt
        tmp_data = tuple([time]) + model.state
        print(time)

        state = {axes_name[i]: s for i, s in enumerate(model.state)}
        print(state)

        try:
            element_number = inputs_space.get_element_number(state)
            model.input = inputs_set[inputs_space.values[element_number]]
        except ValueError as e:
            print(e)
            break

        print(model.input)
        tmp_se = pd.Series(tmp_data, index=df.columns)
        df = df.append(tmp_se, ignore_index=True)
        model.step(dt)

    df.to_csv("./data.csv", index=False)
    plt.show()

    return df
