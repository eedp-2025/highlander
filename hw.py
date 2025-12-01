import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

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

def fixed_spacing_calcs(X_points, Y_points):
    X1 = X_points[0]
    Y1 = Y_points[0]
    X2 = X_points[1]
    Y2 = Y_points[1]
    spacing = sqrt((X2-X1)**2 + (Y2-Y1)**2)**0.5
    atriangle = 0.5*spacing*sqrt(R**2-((spacing**2)/4))
    area_est = atriangle*len(X_points)
    perimeter_est = spacing*len(X_points)
    return perimeter_est, area_est
# Generates a circle depending on the method chosen. Returns points on circle.
def circle_generation(origin, R, N, method):
    X_points = []
    Y_points = []

    if method == 1: # Theta for fixed-point method
        theta = [None]*N
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
def monte_carlo_integration(R, origin, range_N = True, plot = True):
    if range_N == True:
        N = [1 + n for n in range(5000)]
    else:
        N = [10000]
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

    if plot == True:
        # Plotting relationship between number of random points and area of circle
        plt.plot(N, A_circle, label='Approximated Area')
        plt.plot([N[0], N[-1]], [np.pi * R ** 2, np.pi * R ** 2], label='Theoretical Area')
        plt.xlim(N[0], N[-1])
        plt.legend()
        plt.show()

    return A_circle[-1]


# Extra credit 3: estimating pi with Monte Carlo integration
def estimate_pi():
    # Use Monte Carlo integration on a circle with R = 10,000 and N = 5000, for higher fidelity
    A = monte_carlo_integration(10000, [0,0], range_N = False, plot = False)
    pi_est = A/(10000**2)    # Estimating pi using A = pi*R^2

    return pi_est

# Running code
initialize()
circle = circle_generation(origin, R, N, method)
monte_carlo_integration(R, origin)
pi_est = estimate_pi()
print(fixed_spacing_calcs(circle[0],circle[1]))
print(circle[0],circle[1])
print('Using Monte Carlo integration, pi is estimated to be ' + str(pi_est) + ', which has an error of ' + str(abs(100*(np.pi - pi_est)/np.pi)) + '%.')