import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, dist, atan2
import time


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
    rand_numbers = np.random.default_rng(seed=42).choice(10*N, size=N, replace=False)
    return rand_numbers

# Actual circumference calc with cpu timing
def actual_circumference(radius: float) -> float:
    start = time.process_time()
    circ = 2 * np.pi * radius
    end = time.process_time()
    cpu_time = end - start
    print(f"The CPU time for the actual circumference calculation is {cpu_time:.6f} s")
    return circ

# Actual area calc with cpu timing
def actual_area(radius: float) -> float:
    start = time.process_time()
    area = np.pi * (radius ** 2)
    end = time.process_time()
    cpu_time = end - start
    print(f"The CPU time for the actual area calculation is {cpu_time:.6f} s")
    return area

# Calculate perimeter and area using fixed points
def fixed_spacing_calcs(X_points, Y_points):
    start = time.process_time()

    X1 = X_points[0]
    Y1 = Y_points[0]
    X2 = X_points[1]
    Y2 = Y_points[1]
    spacing = sqrt((X2-X1)**2 + (Y2-Y1)**2)**0.5
    atriangle = 0.5*spacing*sqrt(R**2-((spacing**2)/4))
    area_est = atriangle*len(X_points)
    perimeter_est = spacing*len(X_points)

    end = time.process_time()
    cpu_time = end - start
    print(f"The CPU time for the fixed point perimeter and area calculations is {cpu_time:.6f} s")

    return perimeter_est, area_est


# Sort the list of coordinates based on polar coord theta value (radians)
def sort_coords(X_points, Y_points, cx, cy):
    angle_dict = {}
    for i in range(len(X_points)):
        angle = atan2(Y_points[i] - cy, X_points[i] - cx)  # in radians
        angle_dict[X_points[i], Y_points[i]] = angle

    sorted_angles = dict(sorted(angle_dict.items(), key=lambda item: item[1]))
    sorted_coords = list(sorted_angles.keys())
    return sorted_coords


# Calculate perimeter and area using random points
def random_spacing_calcs(X_points, Y_points):
    perimeter_est = 0
    area_est = 0

    start = time.process_time()
    sorted_coords = sort_coords(X_points, Y_points, origin[0], origin[1])
    for i in range(len(sorted_coords) - 1):
        X1 = sorted_coords[i][0]
        Y1 = sorted_coords[i][1]
        X2 = sorted_coords[i+1][0]
        Y2 = sorted_coords[i+1][1]

        # Calculate distance between each point, sum for circle perimeter estimation
        euc_distance = dist((X1, Y1), (X2, Y2))
        perimeter_est += euc_distance

        # Calculate area of isosceles triangle between each point, sum for circle area estimation
        tri_area = 0.5*euc_distance*sqrt(R**2-((euc_distance**2)/4))
        area_est += tri_area

    end = time.process_time()
    cpu_time = end - start
    print(f"The CPU time for the random point perimeter and area calculations is {cpu_time:.6f} s")
    return perimeter_est, area_est


# Generates a circle depending on the method chosen. Returns points on circle.
def circle_generation(origin, R, N, method):
    X_points = []
    Y_points = []

    if method == 1: # Theta for fixed-point method
        theta = [None]*N
        for n in range(N):
            theta[n] = 2*np.pi*(n/N)

    if method == 2: # Monte Carlo method, random
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


if __name__ == "__main__":
    initialize()
    circle = circle_generation(origin, R, N, method)
    # print("Chosen points on circle:", circle[0], circle[1])

    if method == 1:
        fixed_pt_per, fixed_pt_area = fixed_spacing_calcs(circle[0], circle[1])
        print(f"Using equally spaced points, the perimeter is estimated as {fixed_pt_per}, "
              f"and the area is estimated as {fixed_pt_area}")
        true_circ = actual_circumference(R)
        true_area = actual_area(R)
        print(f"The actual circumference is {true_circ}")
        print(f"The actual area is {true_area}")
        print(f"The difference in actual - estimated circumference is {true_circ - fixed_pt_per}")
        print(f"The difference in actual - estimated area is {true_area - fixed_pt_area}")

    elif method == 2:
        random_pt_per, random_pt_area = random_spacing_calcs(circle[0], circle[1])
        print(f"Using equally spaced points, the perimeter is estimated as {random_pt_per}, "
              f"and the area is estimated as {random_pt_area}")
        true_circ = actual_circumference(R)
        true_area = actual_area(R)
        print(f"The actual circumference is {true_circ}")
        print(f"The actual area is {true_area}")
        print(f"The difference in actual - estimated circumference is {true_circ - random_pt_per}")
        print(f"The difference in actual - estimated area is {true_area - random_pt_area}")


    # Extra credit:
    # 2
    monte_carlo_integration(R, origin)

    # 3
    pi_est = estimate_pi()

    print()
    print('Using Monte Carlo integration, pi is estimated to be ' + str(pi_est) + ', which has an error of ' +
          str(abs(100*(np.pi - pi_est)/np.pi)) + '%.')



