import matplotlib.pyplot as plt
import numpy as np


#TODO: remove
def show_data(data):
    plt.figure()
    plt.imshow(data)

    plt.show()

#TODO: remove
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


class Fig2D:

    def __init__(self):
        
        self.fig, self.ax = plt.subplots()

    def add_vector_field(self, title, data):
        X, Y = np.meshgrid(range(data.shape[0]), range(data.shape[1]))
        U = data[:, :, 0]
        V = -data[:, :, 1]
        self.ax.set_title(title)
        Q = self.ax.quiver(X, Y, U.T, V.T, units="x", pivot="tip", width=0.02, scale=2)

    def add_line(self, label, data):
        self.ax.plot(data[0], data[1], label=label)

    def add_img(self, data):
        self.ax.imshow(data)

    def show(self):
        plt.legend()
        plt.show()

