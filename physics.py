import numpy as np

def projectile_derivative(position_and_velocity, t, consts=()):
    '''
    The only force acting on the projectile is GRAVITY.
    Takes in the position and velocity of a projectile, packaged in one vector, and the current time.
    Returns its velocity and acceleration, packaged in one vector.

    Parameters
    ----------
    position_and_velocity: a four-element tuple or array (x_pos, y_pos, x_vel, y_vel) representing the current position and velocity state
    time: a float representing the current time
    consts: a tuple that will not be used; it is here to match the parameters of projectile_drag_derivative

    Returns
    -------
    velocity_and_acceleration: a four-element array (x_vel, y_vel, x_acc, y_acc) representing the current velocity and acceleration
    '''
    #%% Set constants.
    g = 9.8                               # gravitational acceleration     [m/s^2]

    #%% Unpack the vector's components.
    x_pos = position_and_velocity[0]
    y_pos = position_and_velocity[1]
    x_vel = position_and_velocity[2]
    y_vel = position_and_velocity[3]

    #%% Compute the derivatives.
    velocity_and_acceleration = np.zeros(4)                 # Create a list to store derivatives.
    velocity_and_acceleration[2] = 0                        # x-acceleration
    velocity_and_acceleration[3] = -g                       # y-acceleration
    velocity_and_acceleration[0] = x_vel                    # x-velocity
    velocity_and_acceleration[1] = y_vel                    # y_velocity
    return velocity_and_acceleration

def projectile_drag_derivative(position_and_velocity, t, consts):
    '''
    The forces acting on the projectile are GRAVITY and QUADRATIC DRAG.
    Takes in the position and velocity of a projectile, packaged in one vector, and the current time.
    Returns its velocity and acceleration, packaged in one vector.

    Parameters
    ----------
    position_and_velocity: a four-element array (x_pos, y_pos, x_vel, y_vel) representing the current position and velocity state
    time: a float representing the current time
    consts: a tuple (g, c, m) representing gravity, the quadratic drag coefficient and the projectile mass

    Returns
    -------
    velocity_and_acceleration: a four-element array (x_vel, y_vel, x_acc, y_acc) representing the current velocity and acceleration
    '''
    #%% Set constants.
    g = 9.8                               # gravitational acceleration     [m/s^2]
    c = consts[0]                         # quadratic drag coefficient     [kg/m]
    m = consts[1]                         # mass                           [kg]

    #%% Unpack the vector's components.
    x_pos = position_and_velocity[0]
    y_pos = position_and_velocity[1]
    x_vel = position_and_velocity[2]
    y_vel = position_and_velocity[3]

    #%% Calculate drag force in each direction
    speed = np.sqrt( x_vel**2 + y_vel**2 )
    x_drag = c * x_vel * speed
    y_drag = c * y_vel * speed

    #%% Compute the derivatives
    velocity_and_acceleration = np.zeros(4)                      # Create a list to store derivatives.
    velocity_and_acceleration[2] = -x_drag / m                   # x-acceleration
    velocity_and_acceleration[3] = -y_drag / m - g               # y-acceleration
    velocity_and_acceleration[0] = x_vel                         # x-velocity
    velocity_and_acceleration[1] = y_vel                         # y_velocity
    return velocity_and_acceleration