import random
from custom_io import get_graph_from_input


def mutate(i, G):
    '''a random gene has its allele swapped by a random facility
    given the new facility is not present in the chromosome
    '''
    new_median = random.choice(G.nodes())
    while new_median in i.chromosome:
        new_median = random.choice(G.nodes())
    mutated_i = Individual()
    to_replace = random.choice(list(i.chromosome))
    mutated_i.chromosome = set([x if x != to_replace else new_median
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
        self.fitness = -1
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

    def calculate_fitness(self, G):
        self.fitness = 0
        # creates dict of median's capacities
        median_dic = {}
        for median in self.chromosome:
            median_dic[median] = G.node[median]['capacity']
        # assign evey node of the graph to a median,
        # including the medians themselves
        for node, attr in G.node.iteritems():
            l = self.get_list_medians_ordered_by_distance(node, G)
            for median, distance in l:
                if median_dic[median] - attr['demand'] > 0:
                    self.fitness += distance
                    median_dic[median] -= attr['demand']
                    break
        return self.fitness


if __name__ == '__main__':
    G = get_graph_from_input('../data/SJC1.dat')
    popsize = 100
    maxiter = 100
    elite = 0.2
    mutprob = 0.01
    coprob = 0.6
    tournament_size = 2
    p = 10

    pop = []
    for i in range(popsize):
        individual = Individual(p, G)
        pop.append(individual)

    for i in range(maxiter):
        scores = [(i.calculate_fitness(G), i) for i in pop]
        scores.sort()
        ranked = [i for (s, i) in scores]
        print scores[0][0]

        topelite = int(elite * popsize)
        new_pop = ranked[0:topelite]
        while len(new_pop) < popsize:
            random_number = random.random()
            if random_number < mutprob:
                c = random.randint(0, popsize - 1)
                new_pop.append(mutate(pop[c], G))
            elif random_number < coprob:
                subpop = random.sample(pop, tournament_size)
                i1, i2 = crossover(subpop[0], subpop[1])
                new_pop.append(i1)
                new_pop.append(i2)
            else:
                c = random.randint(0, popsize - 1)
                new_pop.append(pop[c])
            if len(new_pop) > popsize:
                new_pop.pop()

        pop = new_pop
