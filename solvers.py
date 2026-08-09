import numpy as np

def euler_solver(derivative_function, initial_state, times, consts=()):
    '''
    Uses Euler's method to find the solution to a differential equation at specified timesteps
    
    Parameters
    ----------
    derivative_function(state, time): a function that inputs the current state and time and outputs the derivative
    initial_state: a 1D tuple or array encoding the initial conditions
    times: a 1D array of times at which the states are to be computed
    consts: a tuple of constants to be passed into derivative_function

    Returns
    -------
    states: a 1D array the same size as (times), with the states at each corresponding time
    '''
    #%% Create an array to store states at specified timesteps.
    states = np.zeros(( len(times), len(initial_state) ))
    states[0] = initial_state

    #%% Fill the states array with estimates using Euler's method.
    for i in range(len(times) - 1):
        slope = derivative_function(states[i], times[i], consts)     # Get the state's derivative at a specified time
        dt = times[i+1] - times[i]
        states[i+1] = states[i] + slope * dt                 # Use Euler's method to determine the next state
        
    return states