"""Testing code."""

from itertools import combinations
# from math import sqrt
from random import random
from deap import benchmarks
import numpy as np
from deap.tools import cxSimulatedBinaryBounded, mutPolynomialBounded
from optproblems import dtlz, zdt
from scipy.special import comb
from pyDOE import lhs
from RVEA import rvea


class Problem():
    """Defines the problem."""

    def __init__(
            self, name, num_of_variables, upper_limits, lower_limits,
            num_of_objectives, num_of_constraints):
        """Pydocstring is ruthless."""
        self.name = name
        self.num_of_variables = num_of_variables
        self.num_of_objectives = num_of_objectives
        self.num_of_constraints = num_of_constraints
        if name == 'ZDT1':
            self.obj_func = zdt.ZDT1()
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'ZDT2':
            self.obj_func = zdt.ZDT2()
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'ZDT3':
            self.obj_func = zdt.ZDT3()
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'ZDT4':
            self.obj_func = zdt.ZDT4()
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'ZDT5':
            self.obj_func = zdt.ZDT5()
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'ZDT6':
            self.obj_func = zdt.ZDT6()
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'DTLZ1':
            self.obj_func = dtlz.DTLZ1(num_of_objectives, num_of_variables)
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'DTLZ2':
            self.obj_func = dtlz.DTLZ2(num_of_objectives, num_of_variables)
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'DTLZ3':
            self.obj_func = benchmarks.dtlz3
            self.lower_limits = 0
            self.upper_limits = 1
        if name == 'DTLZ4':
            self.obj_func = dtlz.DTLZ4(num_of_objectives, num_of_variables)
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'DTLZ5':
            self.obj_func = dtlz.DTLZ5(num_of_objectives, num_of_variables)
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'DTLZ6':
            self.obj_func = dtlz.DTLZ6(num_of_objectives, num_of_variables)
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds
        if name == 'DTLZ7':
            self.obj_func = dtlz.DTLZ7(num_of_objectives, num_of_variables)
            self.lower_limits = self.obj_func.min_bounds
            self.upper_limits = self.obj_func.max_bounds

    def objectives(self, decision_variables) ->list:
        """Use this method to calculate objective functions."""
        # if self.name == 'ZDT1':
        #    obj1 = decision_variables[0]
        #    g = 1 + (9/29)*sum(decision_variables[1:])
        #    obj2 = g*(1 - sqrt(obj1/g))
        #    return([obj1, obj2])
        if self.name == 'DTLZ3':
            return(self.obj_func(decision_variables, self.num_of_objectives))
        return(self.obj_func(decision_variables))

    def constraints(self, decision_variables, objective_variables):
        """Calculate constraint violation."""
        print('Error: Constraints not supported yet.')


class Parameters():
    """This object contains the parameters necessary for evolution."""

    def __init__(
            self,
            population_size,
            lattice_resolution,
            algorithm_name='RVEA',
            *args):
        """Initialize the parameters class."""
        self = {}
        if algorithm_name == 'RVEA':
            self['RVEA'].population_size = population_size
            self['RVEA'].lattice_resolution = lattice_resolution
            self['RVEA'].algorithm = rvea
            self['RVEA'].generations = 100
            self['RVEA'].Alpha = 2
            self['RVEA'].refV_adapt_frequency = 0.1
            self['RVEA'].mut_type = 'PolyMut'
            self['RVEA'].xover_type = 'SBX'
            self['RVEA'].mutation = \
                Parameters.MutationParameters(self['RVEA'].mut_type)
            self['RVEA'].crossover = \
                Parameters.CrossoverParameters(self['RVEA'].xover_type)

    class MutationParameters():
        """This object contains the parameters necessary for mutation.

        Currently supported: Bounded Polynomial mutation as implimented
        in NSGA-II by Deb.

        Parameters
        ----------
        eta: Crowding degree of mutation for polynomial mutation.
        High values results in smaller mutations.

        indpb: Independent probability of mutation.

        """

        def __init__(self, mutation_type, eta=20, indpb=0.3):
            """Define mutation type and parameters."""
            if mutation_type == "PolyMut":
                self.mut_type = 'PolyMut'
                self.crowding_degree_of_mutation = eta
                self.independent_probability_of_mutation = indpb
            elif mutation_type == "SelfAdapt":
                print('Error: Self Adaptive Mutation not defined yet.')
            else:
                print('Error: Mutation type not defined.')

    class CrossoverParameters():
        """This object contains the parameters necessary for crossover.

        Currently supported: Simulated Binary Crossover

        """

        def __init__(self, xover_type):
            """Define crossover type and parameters."""
            if xover_type == 'SBX':
                self.xover_type = 'SBX'
                self.crowding_degree_of_crossover = 0.3
            else:
                print('Error: Crossover type not defined')


class Individual():
    """Defines an individual."""

    def __init__(self, problem, assign_type='RandomAssign', variable_values=0):
        """Initialize an individual with zeros.

        parameter: problem is a Problem object.
        parameter: assignType defines how the individual is created.
        parameter: varuableValues contains the values of the variables.
        """
        self.variables = np.zeros(problem.num_of_variables)
        self.objectives = [0]*problem.num_of_objectives
        self.constraint_violation = [0]

        if assign_type == 'RandomAssign':
            self.random_assign(problem)
        elif assign_type == 'LHSDesign':
            pass
        elif assign_type == 'CustomAssign':
            self.custom_assign(problem, variable_values)
        else:
            print('Error: assignType not defined')

    def random_assign(self, problem):
        """Assign random values to individual."""
        for i in range(len(self.variables)):
            self.variables[i] = random()

    def LHS_assign(self, population, problem):
        """LHS design of experiment for individuals."""
        pass

    def custom_assign(self, problem, variable_values):
        """Use to create custom individuals, such as after mating."""
        self.variables = variable_values

    def evaluate(self, problem):
        """Evaluate the individual.

        Updates self.objectives and self.constraint_violation variables.
        """
        self.objectives = problem.objectives(self.variables)
        if problem.num_of_constraints:
            self.constraint_violation = problem.Constraints(self.variables)
        return([self.objectives + self.constraint_violation])

    def mate(self, other, problem, parameters):
        """Perform Crossover and mutation on parents and return 2 children."""
        crossover_parameters = parameters.crossover
        mutation_parameters = parameters.mutation
        # Crossover
        parent1 = np.copy(self.variables)
        parent2 = np.copy(other.variables)
        child1, child2 = cxSimulatedBinaryBounded(
            parent1, parent2,
            crossover_parameters.crowding_degree_of_crossover,
            problem.lower_limits, problem.upper_limits)
        # Mutation
        if mutation_parameters.mut_type == 'PolyMut':
            # test
            mutation_parameters.independent_probability_of_mutation = 1/len(child1)
            child1 = mutPolynomialBounded(
                child1, mutation_parameters.crowding_degree_of_mutation,
                problem.lower_limits, problem.upper_limits,
                mutation_parameters.independent_probability_of_mutation)[0]
            child1 = Individual(

                problem, assign_type='CustomAssign', variable_values=child1)
            child2 = mutPolynomialBounded(
                child2, mutation_parameters.crowding_degree_of_mutation,
                problem.lower_limits, problem.upper_limits,
                mutation_parameters.independent_probability_of_mutation)[0]
            child2 = Individual(
                problem, assign_type='CustomAssign', variable_values=child2)
            return child1, child2


class Population():
    """Define the population."""

    def __init__(self,
                 problem: Problem,
                 parameters: Parameters,
                 assign_type: str='RandomAssign',
                 *args):
        """Initialize the population.

        Parameters:
        ------------
            problem: An object of the class Problem

            parameters: An object of the class Parameters

            assign_type: Define the method of creation of population.
                If 'assign_type' is 'RandomAssign' the population is generated
                randomly.
                If 'assign_type' is 'LHSDesign', the population is generated
                via Latin Hypercube Sampling.
                If 'assign_type' is 'custom', the population is imported from
                file.
                If assign_type is 'empty', create blank population.

        """
        pop_size = parameters.population_size
        num_var = problem.num_of_variables
        if assign_type == 'RandomAssign':
            self.individuals = np.random.random((pop_size, num_var))
        elif assign_type == 'LHSDesign':
            self.individuals = lhs(num_var, samples=pop_size)
        elif assign_type == 'custom':
            print('Error: Custom assign type not supported yet.')
        elif assign_type == 'empty':
            self.individuals = []
            self.objectives = []
            self.fitness = []
            self.constraint_violation = []
        if not self.individuals:
            pop_eval = self.evaluate(Problem)
            self.objectives = pop_eval['objectives']
            self.constraint_violation = pop_eval['cons']
            self.fitness = pop_eval['fitness']

    def evaluate(self, problem: Problem):
        """Evaluate and return objective values."""
        pop = self.individuals
        objs = None
        cons = None
        for ind in pop:
            if objs is None:
                objs = np.asarray(problem.objectives(ind))
            else:
                objs = np.vstack(obj, problem.objectives(ind))
        if problem.num_of_constraints:
            for ind, obj in zip(pop, obj):
                if cons is None:
                    cons = problem.constraints(ind, obj)
                else:
                    cons = np.vstack(cons, problem.constraints(ind, obj))
            fitness = self.eval_fitness(pop, objs)
        else:
            cons = np.zeros(pop.shape[0], 1)
            fitness = objs
        return({"objectives": objs,
                "constraint violation": cons,
                "fitness": fitness})

    def eval_fitness(self, pop, objs):
        """Return fitness values. Maybe add maximization support here."""
        pass

    def append(self, new_pop: np.ndarray, problem: Problem):
        """Evaluate and add individuals to the population."""
        if new_pop.ndim == 1:
            self.append_individual(self, new_pop, problem)
        elif new_pop.ndim == 2:
            for ind in new_pop:
                self.append_individual(self, ind, problem)
        else:
            print('Error while adding new individuals. Check dimensions.')

    def append_individual(self, ind: np.ndarray, problem: Problem):
        """Evaluate and add individual to the population."""
        self.individuals = np.vstack(self.individuals, ind)
        obj, CV, fitness = self.evaluate_individual(ind)
        self.objectives = np.vstack(self.objectives, obj)
        self.constraint_violation = np.vstack(self.constraint_violation, CV)
        self.fitness = np.vstack(self.fitness, fitness)

    def evaluate_individual(self, ind: np.ndarray, problem: Problem):
        """
        Evaluate individual.

        Returns objective values, constraint violation, and fitness.
        """
        obj = problem.objectives(ind)
        CV = 0
        fitness = obj
        if problem.constraints:
            CV = problem.constraints(ind, obj)
            fitness = self.eval_fitness(ind, obj)
        return(obj, CV, fitness)

    def evolve(self, problem: Problem, parameters: Parameters):
        """Evolve and return the population."""
        evolved_population = parameters.algorithm(self, problem, parameters)
        return(evolved_population)


class ReferenceVectors():
    """Class object for reference vectors."""

    def __init__(self, lattice_resolution: int, number_of_objectives):
        """Create a simplex lattice."""
        number_of_vectors = comb(
            lattice_resolution + number_of_objectives - 1,
            number_of_objectives - 1, exact=True)
        temp1 = range(1, number_of_objectives + lattice_resolution)
        temp1 = np.array(list(combinations(temp1, number_of_objectives-1)))
        temp2 = np.array([range(number_of_objectives-1)]*number_of_vectors)
        temp = temp1 - temp2 - 1
        weight = np.zeros((number_of_vectors, number_of_objectives), dtype=int)
        weight[:, 0] = temp[:, 0]
        for i in range(1, number_of_objectives-1):
            weight[:, i] = temp[:, i] - temp[:, i-1]
        weight[:, -1] = lattice_resolution - temp[:, -1]
        self.values = weight/lattice_resolution
        self.initial_values = self.values
        self.number_of_objectives = number_of_objectives
        self.lattice_resolution = lattice_resolution
        self.number_of_vectors = number_of_vectors
        self.normalize()

    def normalize(self):
        """Normalize the reference vectors."""
        norm = np.linalg.norm(self.values, axis=1)
        norm = np.repeat(norm, self.number_of_objectives).reshape(
            self.number_of_vectors, self.number_of_objectives)
        self.values = np.divide(self.values, norm)

    def neighbouring_angles(self) -> np.ndarray:
        """Calculate neighbouring angles for normalization."""
        cosvv = np.dot(self.values, self.values.transpose())
        cosvv.sort(axis=1)
        cosvv = np.flip(cosvv, 1)
        acosvv = np.arccos(cosvv[:, 1])
        return(acosvv)

    def adapt(self, max_val, min_val):
        """Adapt reference vectors."""
        self.values = np.multiply(self.initial_values,
                                  np.tile(np.subtract(max_val, min_val),
                                          (self.number_of_vectors, 1)))
        self.normalize()
