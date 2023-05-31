import matplotlib.pyplot as plt
import numpy as np


def show_data(data):
    plt.figure()
    plt.imshow(data)

    plt.show()


def show_vector_field(data):
    X, Y = np.meshgrid(range(data.shape[0]), range(data.shape[1]))
    U = data[:, :, 0]
    V = data[:, :, 1]
    fig1, ax1 = plt.subplots()
    ax1.set_title("Arrows scale with plot width, not view")
    Q = ax1.quiver(X, Y, U.T, V.T, units="x", pivot="tip", width=0.02, scale=2)
    print(data)
    print(X, Y, U, V)
    plt.show()
