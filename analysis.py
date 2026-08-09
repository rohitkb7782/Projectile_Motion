import numpy as np
from physics import projectile_derivative, projectile_drag_derivative
from solvers import euler_solver

def interpolate_ground_impact(states):
    '''
    Uses linear interpolation to find when the projectile hits the ground in the middle of a timestep.
    Trim the states array to include before the timestep only.

    Parameters
    ----------
    states: an array of (x_pos, y_pos, x_vel, y_vel) states in chronological order

    Returns
    -------
    above_states: the input states array trimmed to include above ground indices and the final interpolated index
    '''
    below = np.where(states[:,1] < 0)[0]                     # Collect the indices of all states where y < 0

    #%% Interpolate to find the x position when the projectile reaches y = 0.
    if len(below) > 0:
        i = below[0]                                         # The first index below ground
        x1, y1 = states[i - 1, 0], states[i - 1, 1]          # The last x and y above ground
        x2, y2 = states[i, 0], states[i, 1]                  # The first x and y below ground
        alpha = y1 / (y1 - y2)                               # alpha: Fraction of the Euler step to travel in order to reach the ground
        x_ground = x1 + alpha * (x2 - x1)                    # The Euler step's estimate of x upon reaching the ground

    #%% Export a copy of the states array with above ground values only.
    above_states = states.copy()[:i+1,:]
    above_states[i,0] = x_ground
    above_states[i,1] = 0
    return above_states

def analytical_solution(speed, angle):
    '''
    Calculates the analytical solution to the projectile equations of motion:
    x = Vx t
    y = Vy t - 0.5 g t^2
    Returns the x and y values of the projectile above ground according to the analytical solution.
    '''
    times = np.arange(0, 3, 0.01)
    x_analytical = speed*np.cos(angle) * times
    y_analytical = speed*np.sin(angle) * times - 4.9 * times**2
    mask = (y_analytical >= 0)                                           # Erase values where y < 0
    return x_analytical[mask], y_analytical[mask]

def error_analysis(step_sizes, estimate_ranges_list, analytical_range):
    '''
    Calculates the error of each estimate range compared to the analytical range
    Returns the errors in a list.
    '''
    errors_list = []
    for i in range(len(step_sizes)):
        error = estimate_ranges_list[i] - analytical_range
        errors_list.append(error)
    return errors_list

def get_trajectory(speed, angle, dt=0.001, consts=(0,1)):
    '''
    '''
    initial_position = (0, 0)
    initial_velocity = (speed*np.cos(angle), speed*np.sin(angle))
    times = np.arange(0, 3 + dt, dt)                           # times at which to evaluate position and velocity   [s]
    initial_state = initial_position + initial_velocity              # Concatenate initial conditions into a 4D vector
    states = euler_solver(projectile_drag_derivative, initial_state, times, consts)          # Solve for the 4D vector at the specified times
    above_ground_trajectory = interpolate_ground_impact(states)

    return above_ground_trajectory[:,0], above_ground_trajectory[:,1],    # all x, all y

def get_optimal_angle(speed, consts):
    '''
    '''
    coarse_angles = np.linspace(0.5, 0.8, 10)
    coarse_ranges = []
    for angle in coarse_angles:
        x_positions, y_positions = get_trajectory(speed, angle, consts=consts)
        coarse_ranges.append(x_positions[-1])

    i = np.argmax(coarse_ranges)
    coarse_optimal_angle = coarse_angles[i]

    mid_angles = np.linspace(coarse_optimal_angle - 0.1, coarse_optimal_angle + 0.1, 10)
    mid_ranges = []
    for angle in mid_angles:
        x_positions, y_positions = get_trajectory(speed, angle, consts=consts)
        mid_ranges.append(x_positions[-1])

    i = np.argmax(mid_ranges)
    mid_optimal_angle = mid_angles[i]
    
    fine_angles = np.linspace(mid_optimal_angle - 0.02, mid_optimal_angle + 0.02, 10)
    fine_ranges = []
    for angle in fine_angles:
        x_positions, y_positions = get_trajectory(speed, angle, consts=consts)
        fine_ranges.append(x_positions[-1])

    i = np.argmax(fine_ranges)
    max_range = fine_ranges[i]
    fine_optimal_angle = fine_angles[i]
    
    return fine_optimal_angle, max_range

def params_from_alpha(alpha, method):
    g = 9.8
    if method == "c":
        v0 = 5
        m = 1
        c = alpha * m * g / v0**2

    elif method == "v0":
        c = 0.1
        m = 1
        v0 = np.sqrt(alpha * m * g / c)

    elif method == "m":
        c = 0.1
        v0 = 5
        m = c * v0**2 / (alpha * g)

    return c, v0, m