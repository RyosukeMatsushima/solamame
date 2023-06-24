from scipy.sparse import identity
from scipy.sparse.linalg import inv
from scipy.sparse import csc_matrix

# TODO: remove
from modules.tools.fig_2d import *

class FindCostToGo:
    def __init__(
        self,
        goal_probabilistic_space,
        transition_matrix,
        damping_value):

        self.goal_probabilistic_space = goal_probabilistic_space
        self.transition_matrix = transition_matrix
        self.damping_value = damping_value

    def calculate(self):
        M = csc_matrix(identity(self.goal_probabilistic_space.element_count) - self.damping_value * self.transition_matrix)

        #print(self.goal_probabilistic_space.values)

        print("calculate inversed matrix")
        M = inv(M)
        #show_data(np.where(M.toarray() > 0, 1, 0))

        print("calculate dot production")
        Q_inf = M @ self.goal_probabilistic_space.values
        print(Q_inf)

        self.goal_probabilistic_space.values = Q_inf

        sheet = self.goal_probabilistic_space.get_2d_sheet("x", "J", {"x": 0, "y": 2, "J": 10})
        threshold = 0.00001
        sheet = np.where(np.array(sheet) > threshold, threshold, sheet)
        show_data(sheet)


        for i in range(5):
            print(i)
            sheet = self.goal_probabilistic_space.get_2d_sheet("x", "y", {"x": 1, "y": 1, "J": i * 1})
            threshold = 0.000000000001
            sheet = np.where(np.array(sheet) > threshold, threshold, sheet)
            show_data(sheet)


