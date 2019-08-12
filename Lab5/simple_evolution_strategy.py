import numpy as np


class SimpleEvolutionStrategy:
    """
    Represents a simple evolution strategy optimization algorithm.
    The mean and covariance of a gaussian distribution are evolved at each generation.
    """
    def __init__(self, m0, C0, mu, population_size):
        """
        Constructs the simple evolution strategy algorithm.

        :param m0: initial mean of the gaussian distribution.
        :type m0: numpy array of floats.
        :param C0: initial covariance of the gaussian distribution.
        :type C0: numpy matrix of floats.
        :param mu: number of parents used to evolve the distribution.
        :type mu: int.
        :param population_size: number of samples at each generation.
        :type population_size: int.
        """
        self.m = m0
        self.C = C0
        self.mu = mu
        self.population_size = population_size
        self.samples = np.random.multivariate_normal(self.m, self.C, self.population_size)

    def ask(self):
        """
        Obtains the samples of this generation to be evaluated.
        The returned matrix has dimension (population_size, n), where n is the problem dimension.

        :return: samples to be evaluated.
        :rtype: numpy array of floats.
        """
        return self.samples

    def tell(self, fitnesses):
        """
        Tells the algorithm the evaluated fitnesses. The order of the fitnesses in this array
        must respect the order of the samples.

        :param fitnesses: array containing the value of fitness of each sample.
        :type fitnesses: numpy array of floats.
        """
        #selecionar os um melhores
        indices = np.argsort(fitnesses)
        best_samples = self.samples[indices[0:self.mu], :]
        #Evoluir a média
        soma = np.zeros(np.size(best_samples[0]))
        for i in range(self.mu):
            soma = soma + best_samples[i]
        media = soma/self.mu
        #Evoluir a matriz de covariância
        soma = np.zeros(np.size(best_samples[0]))
        soma = np.matrix(soma)
        soma = soma.transpose()*soma 
        for i in range(self.mu):
            matrix = np.matrix(best_samples[i] - self.m)
            soma = soma +(matrix.transpose())*matrix
        covar=soma/self.mu
        #Atualizar as geraçãoes
        self.m = media
        self.C = covar
        self.samples = np.random.multivariate_normal(self.m, self.C, self.population_size)
        





