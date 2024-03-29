from math import inf


def hill_climbing(cost_function, neighbors, theta0, epsilon, max_iterations):
    """
    Executes the Hill Climbing (HC) algorithm to minimize (optimize) a cost function.

    :param cost_function: function to be minimized.
    :type cost_function: function.
    :param neighbors: function which returns the neighbors of a given point.
    :type neighbors: list of numpy.array.
    :param theta0: initial guess.
    :type theta0: numpy.array.
    :param epsilon: used to stop the optimization if the current cost is less than epsilon.
    :type epsilon: float.
    :param max_iterations: maximum number of iterations.
    :type max_iterations: int.
    :return theta: local minimum.
    :rtype theta: numpy.array.
    :return history: history of points visited by the algorithm.
    :rtype history: list of numpy.array.
    """
    theta = theta0
    history = [theta0]
    number_of_iterations=0;
    # Todo: Implement Hill Climbing
    while not check_stopping_condition(cost_function,epsilon,max_iterations,theta,number_of_iterations):
        number_of_iterations=number_of_iterations+1
        best=[100000000,100000000]
        vizinhos=neighbors(theta)
      
        for item in vizinhos:
            if cost_function(item) < cost_function(best):
                best=item
            
        if cost_function(best)> cost_function(theta):
            return theta,history
        theta=best
        history.insert(number_of_iterations,theta)

    return theta, history

def check_stopping_condition(cost_function,epsilon,max_iterations,theta,number_of_iterations):
    return cost_function(theta)<epsilon or number_of_iterations > max_iterations

