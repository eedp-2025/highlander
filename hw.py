import numpy as np
import matplotlib.pyplot as plt

# Initializing user inputs
def initialize():
    global origin
    global R
    global N
    global method

    origin = [0,0]
    origin[0] = int(input("X coordinate of circle's origin: "))
    origin[1] = int(input("Y coordinate of circle's origin: "))
    R = int(input("Radius of circle: "))
    N = int(input("Number of points: "))
    method = int(input("Method of calculation (1 for equally-spaced points, 2 for randomly-spaced points): "))
    while method != 1 and method != 2:
        method = int(input("Invalid input, type either 1 or 2 for method: "))

# Random number generator. The factor of 10 is to allow for non-integer values when implemented.
def rng(N):
    rand_numbers = np.random.default_rng().choice(10*N, size=N, replace=False)
    return rand_numbers

# Generates a circle depending on the method chosen. Returns points on circle.
def circle_generation(origin, R, N, method):
    X_points = []
    Y_points = []

    if method == 1: # Theta for fixed-point method
        theta = []
        for n in range(N):
            theta[n] = 2*np.pi*(n/N)

    if method == 2: # Monte Carlo method
        rand_numbers = rng(N)
        theta = [2*np.pi*n/(10*N) for n in rand_numbers]

    for n in theta:
        X_points.append(origin[0] + R*np.cos(n))   # Generating circle
        Y_points.append(origin[1] + R*np.sin(n))


    plt.figure(figsize=(5,5))       # Plotting circle
    plt.scatter(X_points, Y_points)
    plt.show()

    return X_points, Y_points


# Extra credit 2: Monte Carlo circle integration
def monte_carlo_integration(R, origin):
    N = [1 + n for n in range(5000)]
    A_circle = []

    # Iterating through different sample sizes of random points
    for n in N:
        inside_X_points = []
        inside_Y_points = []

        # Generating square of points
        rand_numbers = rng(n)
        X_points = [origin[0] - R + 2*R*i/(10*n)  for i in rand_numbers]
        rand_numbers = rng(n)
        Y_points = [origin[1] - R + 2*R*i/(10*n) for i in rand_numbers]

        # If any points in the square are within the circle, note them
        for j in range(len(X_points)-1):
            if np.sqrt((X_points[j] - origin[0])**2 + (Y_points[j] - origin[1])**2) <= R:
                inside_X_points.append(X_points[j])
                inside_Y_points.append(Y_points[j])

        # Approximating the area of the circle as the ratio of points inside the circle to total points times the area of the square
        A_square = (2*R)**2
        in_out_ratio = len(inside_X_points)/len(X_points)
        A_circle.append(A_square*in_out_ratio)

    # Plotting relationship between number of random points and area of circle
    plt.plot(N, A_circle, label = 'Approximated Area')
    plt.plot([N[0], N[-1]], [np.pi*R**2, np.pi*R**2], label = 'Theoretical Area')
    plt.xlim(N[0], N[-1])
    plt.legend()
    plt.show()

# Running code
initialize()
circle = circle_generation(origin, R, N, method)
monte_carlo_integration(R, origin)