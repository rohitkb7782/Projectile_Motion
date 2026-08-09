import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from physics import projectile_derivative, projectile_drag_derivative
from analysis import interpolate_ground_impact, analytical_solution, error_analysis, get_trajectory, get_optimal_angle, params_from_alpha
from solvers import euler_solver

#%% Initialize parameters.
g = 9.8        # gravity, independently defined in other functions (the code does not support altering gravity!)    [m/s^2]
v0 = 10        # initial speed   [m/s]
angle = 1      # initial angle   [rad]
model = "drag"

if model == "ideal": 
    #%% Run the simulation at different step sizes.
    step_sizes = [0.001, 0.01, 0.1, 0.3, 0.5]                            # Compare simulation accuracy when different step sizes are used
    estimate_ranges_list = []                                            # List to store each simulation's estimate of the projectile's range
    for dt in step_sizes:
        x_positions, y_positions = get_trajectory(v0, angle, dt=dt)
        estimate_ranges_list.append(x_positions[-1])
        plt.plot(x_positions, y_positions, label=str(dt)+" s")

    #%% Calculate the analytical solution to the initial value problem
    x_analytical, y_analytical = analytical_solution(v0, angle)
    plt.plot(x_analytical, y_analytical, "--", label="Analytical Solution")

    plt.xlabel("Horizontal Distance [m]")
    plt.ylabel("Vertical Height [m]")
    plt.title("Projectile Motion using Euler's Method with different step sizes")
    plt.legend()

    errors_list = estimate_ranges_list - x_analytical[-1]               # Errors in estimates of the range
    plt.figure()
    plt.plot(step_sizes, errors_list)
    plt.xlabel("Step Sizes [s]")
    plt.ylabel("Errors in Range [m]")
    plt.title("Errors in Range vs. Step Sizes for Euler's Method")

elif model == "drag":
    #%% CREATE THE FIRST GRAPH: a few trajectories with different values of c
    c_list = [0, 0.02, 0.05, 0.08]        # List of quadratic drag coefficients to loop through   [kg/m]
    m = 1                                 # Projectile mass    [kg]
    for c in c_list:
        #%% Run the simulation.
        consts = (c, m)
        x_positions, y_positions = get_trajectory(v0, angle, consts=consts)
        trajectory = plt.plot(x_positions, y_positions, label=f"c={c:.2f}")
        if c == 0:
            trajectory[0].set_linestyle("--")
        
    plt.xlabel("Horizontal Distance [m]")
    plt.ylabel("Vertical Height [m]")
    plt.title("Trajectories with different drag coefficients")
    plt.legend()
    plt.savefig("drag_trajectories.png")

    #%% CREATE THE SECOND GRAPH: optimal angle vs alpha, varying alpha via c, v0, and m.
    v0 = 10
    c_list = np.arange(0, 1.01, 0.08)
    m = 1
    optimal_angles_list = []
    for i, c in enumerate(c_list):
        if i % 4 == 0 and i != 0:
            print(f"{c*33:.0f}% done")
        
        #%% Get the optimal angle.
        consts = (c, m)
        optimal_angle, max_range = get_optimal_angle(v0, consts)
        optimal_angles_list.append(optimal_angle)

    alpha_list = c_list * v0**2 / (9.8 * m)
    plt.figure()
    plt.plot(alpha_list, optimal_angles_list, label='Varying c')
    
    v0_list = np.arange(1, 10, 0.8)
    c = 1
    m = 1
    optimal_angles_list = []
    for i, v0 in enumerate(v0_list):
        if i % 4 == 0 and i != 0:
            print(f"{33+v0*3.3:.0f}% done")

        #%% Get the optimal angle.
        consts = (c, m)
        optimal_angle, max_range = get_optimal_angle(v0, consts)
        optimal_angles_list.append(optimal_angle)

    alpha_list = c * v0_list**2 / (9.8 * m)
    plt.plot(alpha_list, optimal_angles_list, '--', label=r'Varying $v_0$')

    v0 = 10
    c = 0.1
    m_list = np.logspace(np.log10(0.1), np.log10(10), 10)
    optimal_angles_list = []
    for i, m in enumerate(m_list):
        if i % 4 == 0 and i != 0:
            print(f"{66+m*3.3:.0f}% done")

        #%% Get the optimal angle.
        consts = (c, m)
        optimal_angle, max_range = get_optimal_angle(v0, consts)
        optimal_angles_list.append(optimal_angle)

    alpha_list = c * v0**2 / (9.8 * m_list)
    plt.plot(alpha_list, optimal_angles_list, ':', label='Varying mass')

    plt.xlabel(r"Drag Parameter $\alpha$ [unitless]")
    plt.ylabel("Optimal Launch Angle [rad]")
    plt.title("Optimal Launch Angle vs. Drag Parameter")
    plt.legend()
    plt.savefig("optimal_angle_vs_drag.png")

    #%% CREATE THE THIRD GRAPH: normalized trajectories varying parameters of alpha
    plt.figure()
    #%% Set how styles will change when using different alpha or varying different parameters
    colors = { # alpha => color
        0.2: "tab:blue",
        0.5: "tab:orange",
        0.8: "tab:green"
    }
    
    linestyles = { # variation parameter => linestyle
        "c": "-",
        "v0": "--",
        "m": ":"
    }

    linewidths = { # variation parameter => linewidth
        "c": 0.5,
        "v0": 1.5,
        "m": 3
    }

    #%% Simulate trajectories with the same alphas constructed in different ways
    for alpha in [0.2, 0.5, 0.8]:
        for method in ["c", "v0", "m"]:
            c, v0, m = params_from_alpha(alpha, method)
            # simulate using c, v0, m
            x_positions, y_positions = get_trajectory(v0, angle, consts=(c, m))
            # normalize x and y by the factor g/v0^2
            normalized_x = x_positions * g / v0**2
            normalized_y = y_positions * g / v0**2
            plt.plot(
                normalized_x,
                normalized_y,
                color=colors[alpha],
                linestyle=linestyles[method],
                linewidth=linewidths[method]
            )

    #%% Manually construct two legends.
    alpha_handles = [
        Line2D([0], [0], color=colors[a], lw=2, label=fr"$\alpha={a}$")
        for a in [0.2, 0.5, 0.8]
    ]
    
    method_handles = [
        Line2D([0], [0], color="black", lw=2,
               linestyle=linestyles[m], label=label)
        for m, label in [
            ("c", r"vary $c$"),
            ("v0", r"vary $v_0$"),
            ("m", r"vary $m$")
        ]
    ]
    
    legend1 = plt.legend(handles=alpha_handles, title=r"$\alpha$")
    plt.gca().add_artist(legend1)
    plt.legend(handles=method_handles, title="Method", loc="lower right")

    plt.xlabel("Normalized Horizontal Distance [unitless]")
    plt.ylabel("Normalized Vertical Height [unitless]")
    plt.title(r"Testing Trajectory Scaling at Constant $\alpha$")
    plt.savefig("normalized_drag_trajectories_varying_alpha.png")