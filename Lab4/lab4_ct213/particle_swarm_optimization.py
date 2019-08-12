import numpy as np
import random
from math import inf
from math import floor


class Particle:
    """
    Represents a particle of the Particle Swarm Optimization algorithm.
    """
    def __init__(self, lower_bound, upper_bound):
        """
        Creates a particle of the Particle Swarm Optimization algorithm.

        :param lower_bound: lower bound of the particle position.
        :type lower_bound: numpy array.
        :param upper_bound: upper bound of the particle position.
        :type upper_bound: numpy array.
        """
        #Definir membros da classe 
        self.delta = upper_bound - lower_bound
        self.x = np.zeros(np.size(upper_bound))
        self.v = np.zeros(np.size(upper_bound))
        self.best = self.x
        self.best_value=inf
        self.value= inf
        for i in range(len(upper_bound)) :
            self.x[i] = random.uniform(lower_bound[i],upper_bound[i])
            self.v[i] = random.uniform(-self.delta[i],self.delta[i])

        
class ParticleSwarmOptimization:
    """
    Represents the Particle Swarm Optimization algorithm.
    Hyperparameters:
        inertia_weight: inertia weight.
        cognitive_parameter: cognitive parameter.
        social_parameter: social parameter.

    :param hyperparams: hyperparameters used by Particle Swarm Optimization.
    :type hyperparams: Params.
    :param lower_bound: lower bound of particle position.
    :type lower_bound: numpy array.
    :param upper_bound: upper bound of particle position.
    :type upper_bound: numpy array.
    """
    def __init__(self, hyperparams, lower_bound, upper_bound):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.particles = np.array([])
        self.hyparam=hyperparams
        self.best_g = np.zeros(np.size(lower_bound))
        self.best_g_value=inf
        self.ale_var=0
        self.aux=0
        #criar o vetor de partículas
        for i in range(self.hyparam.num_particles) :
            self.particles = np.append(self.particles,Particle(lower_bound,upper_bound))

    def get_best_position(self):
        """
        Obtains the best position so far found by the algorithm.

        :return: the best position.
        :rtype: numpy array.
        """
        # Todo: implement
        return self.best_g

    def get_best_value(self):
        """
        Obtains the value of the best position so far found by the algorithm.

        :return: value of the best position.
        :rtype: float.
        """
        # Todo: implement
        return self.best_g_value

    def get_position_to_evaluate(self):
        """
        Obtains a new position to evaluate.

        :return: position to evaluate.
        :rtype: numpy array.
        """
        # Escolho uma variável aleatória e envio ela
        self.aux=self.ale_var
        self.ale_var=(self.ale_var+1)%(self.hyparam.num_particles)
        return self.particles[self.aux].x

    def advance_generation(self):
        """
        Advances the generation of particles.
        """
        phip = self.hyparam.cognitive_parameter
        phig = self.hyparam.social_parameter
        iw = self.hyparam.inertia_weight
        for particle in self.particles :
              if particle.value < particle.best_value :
                 particle.best = particle.x
                 particle.best_value = particle.value
                 if particle.value < self.best_g_value :
                    self.best_g = particle.x
                    self.best_g_value = particle.value
    
              rp = random.uniform(0.0 , 1.0)
              rg = random.uniform(0.0 , 1.0)
              particle.v = iw*particle.v + phip*rp*(particle.best - particle.x) + phig*rg*(self.best_g - particle.x)
              particle.x = particle.x + particle.v


    def notify_evaluation(self, value):
        """
        Notifies the algorithm that a particle position evaluation was completed.

        :param value: quality of the particle position.
        :type value: float.
        """
        value=-value
        self.particles[self.aux].value = value 
        if self.ale_var == 0:
            self.advance_generation()
        
        

