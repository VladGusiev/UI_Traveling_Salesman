# GENETIC ALGORITHM
import matplotlib.pyplot as plt
import random


def main(points_array):
    x, y = zip(*points_array)  # Unzip the points into separate x and y arrays
    plt.plot(x, y, marker='o', linestyle='solid')
    # plt.xlabel('X-coordinate')
    # plt.ylabel('Y-coordinate')
    plt.title('Traveling Salesman')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    input_array = [[0, 0], [1, 1], [2, 3], [4, 6], [6, 8], [7, 9]]

    main(input_array)

