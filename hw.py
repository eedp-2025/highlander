import numpy as np
import matplotlib.pyplot as plt

origin = [0, 0]
R = 0
N = 0
method = 0
X_points = []
Y_points = []

origin[0] = int(input("X coordinate of circle's origin: "))
origin[1] = int(input("Y coordinate of circle's origin: "))
R = int(input("Radius of circle: "))
N = int(input("Number of points: "))
method = int(input("Method of calculation (1 for equally-spaced points, 2 for randomly-spaced points): "))
while method != 1 and method != 2:
    method = int(input("Invalid input, type either 1 or 2 for method: "))


# Monte-carlo method
if method == 2:
    theta = np.random.default_rng().choice(10*N, size=N, replace=False)
    theta = [2*np.pi*n/(10*N) for n in theta]

    for n in theta:
        X_points.append(origin[0] + R*np.cos(n))
        Y_points.append(origin[1] + R*np.sin(n))

    plt.figure(figsize=(5,5))
    plt.scatter(X_points, Y_points)
    plt.show()