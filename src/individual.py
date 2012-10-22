import random
from custom_io import get_graph_from_input
from copy import deepcopy


def mutate(i, G):
    '''a random gene has its allele swapped by a random facility
    given the new facility is not present in the chromosome
    '''
    new_median = random.choice(G.nodes())
    while new_median in i.chromosome:
        new_median = random.choice(G.nodes())
    mutated_i = Individual()
    allele_to_replace = random.choice(list(i.chromosome))
    mutated_i.chromosome = set([x if x != allele_to_replace else new_median
                                for x in i.chromosome])
    return mutated_i


def crossover(i1, i2):
    '''does the crossover between two individual. important to consider
    that only the distinct alleles are going to be exchanged

    '''
    intersection = i1.chromosome.intersection(i2.chromosome)
    exchange_set1 = i1.chromosome - intersection
    exchange_set2 = i2.chromosome - intersection

    try:
        c = random.randint(1, len(exchange_set1) - 1)
    except ValueError:  # if both individuals are the same
        return i1, i2
    child1, child2 = Individual(), Individual()
    child1.chromosome = set(list(exchange_set1)[0:c] +
                            list(exchange_set2)[c:]).union(intersection)
    child2.chromosome = set(list(exchange_set2)[0:c] +
                            list(exchange_set1)[c:]).union(intersection)
    return child1, child2


class Individual:
    def __init__(self, p=None, G=None):
        if p is None or G is None:
            self.chromosome = set()
        else:
            self.chromosome = set(random.sample(set(G.nodes()), p))

    def __repr__(self):
        return str(self.chromosome)

    def __str__(self):
        return str(self.chromosome)

    def get_list_medians_ordered_by_distance(self, node, G):
        '''given a node and the base graph G, returns an ordered list of the
        distances between the node and the medians given by the individual's
        chromosome
        '''
        l = []
        for median in self.chromosome:
            d = 0
            if node != median:
                d = G[median][node]['weight']
            l.append((median, d))
        return sorted(l, key=lambda tup: tup[1])

    def calculate_fitness(self, G, nodes_ordered_by_demand):
        '''calculates the fitness of the individual. The heuristic used to
        allocate facilities do medians is to allocate the facilities with
        greater demand first
        '''
        self.fitness = 0
        # creates dict of median's capacities
        median_dic = {}
        for median in self.chromosome:
            median_dic[median] = G.node[median]['capacity']
        # assign evey node of the graph to a median,
        # including the medians themselves
        for node, attr in nodes_ordered_by_demand:
            l = self.get_list_medians_ordered_by_distance(node, G)
            for median, distance in l:
                if median_dic[median] - attr['demand'] >= 0:
                    self.fitness += distance
                    median_dic[median] -= attr['demand']
                    break
        return self.fitness


if __name__ == '__main__':
    G = get_graph_from_input('../data/SJC1.dat')
    nodes_ordered_by_demand = sorted(G.node.items(),
                                     key=lambda t: t[1]['demand'],
                                     reverse=True)
    popsize = 100
    maxiter = 100
    elite = 1 / popsize
    mutprob = 0.2
    coprob = 0.6
    tournament_size = 5
    p = 10

    pop = []
    for i in range(popsize):
        individual = Individual(p, G)
        pop.append(individual)

    for i in range(maxiter):
        scores = [(i.calculate_fitness(G, nodes_ordered_by_demand), i)
                  for i in pop]
        scores.sort()
        ranked = [i for (s, i) in scores]
        print scores[0][0]

        topelite = int(elite * popsize)
        new_pop = ranked[0:topelite]
        while len(new_pop) < popsize:
            random_number = random.random()
            subpop = random.sample(pop, tournament_size)
            if random_number < mutprob:
                new_pop.append(mutate(subpop[0], G))
            elif random_number < coprob:
                i1, i2 = crossover(subpop[0], subpop[1])
                new_pop.append(i1)
                new_pop.append(i2)
            else:
                new_pop.append(deepcopy(subpop[0]))
            if len(new_pop) > popsize:
                new_pop.pop()

        pop = new_pop

    pop[0].apply_medians(G)
    for node, attr in G.node.iteritems():
        print node, attr
