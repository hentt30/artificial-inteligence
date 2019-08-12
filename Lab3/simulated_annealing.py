from math import exp
import random


def simulated_annealing(cost_function, random_neighbor, schedule, theta0, epsilon, max_iterations):
    """
    Executes the Simulated Annealing (SA) algorithm to minimize (optimize) a cost function.

    :param cost_function: function to be minimized.
    :type cost_function: function.
    :param random_neighbor: function which returns a random neighbor of a given point.
    :type random_neighbor: numpy.array.
    :param schedule: function which computes the temperature schedule.
    :type schedule: function.
    :param theta0: initial guess.
    :type theta0: numpy.array.
    :param epsilon: used to stop the optimization if the current cost is less than epsilon.
    :type epsilon: float.
    :param max_iterations: maximum number of iterations.
    :type max_iterations: int.
    :return theta: local minimum.
    :rtype theta: np.array.
    :return history: history of points visited by the algorithm.
    :rtype history: list of np.array.
    """
    theta = theta0
    history = [theta0]
    number_of_iterations=0
    # Todo: Implement Simulated Annealing
    while not check_stopping_condition(cost_function,epsilon,max_iterations,theta,number_of_iterations):
        T=schedule(number_of_iterations)
        number_of_iterations=number_of_iterations+1
        if T < 0:
            return theta,history
        neighbor=random_neighbor(theta)
        deltaE=new_cost_function(cost_function, neighbor)-new_cost_function(cost_function,theta)

        if deltaE >0:
            theta=neighbor
            history.insert(number_of_iterations,theta)
        else:
            r=random.uniform(0,1)
           
            if r <= exp(deltaE/T):
                theta=neighbor
                history.insert(number_of_iterations,theta)            

    
    return theta, history


def check_stopping_condition(cost_function,epsilon,max_iterations,theta,number_of_iterations):
    return cost_function(theta)<epsilon or number_of_iterations > max_iterations
def new_cost_function(cost_function,theta):
    return -1*cost_function(theta)