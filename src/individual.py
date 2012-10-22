from random import choice, randint, sample


def mutate(i, G):
    '''a random gene has its allele swapped by a random facility
    given the new facility is not present in the chromosome
    '''
    new_median = choice(G.nodes())
    while new_median in i.chromosome:
        new_median = choice(G.nodes())
    mutated_i = Individual()
    allele_to_replace = choice(list(i.chromosome))
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

    if i1.chromosome == i2.chromosome:  # if both individuals are the same
        return i1, i2
    else:
        c = randint(0, len(exchange_set1))
    child1, child2 = Individual(), Individual()
    child1.chromosome = set(list(exchange_set1)[0:c] +
                            list(exchange_set2)[c:]).union(intersection)
    child2.chromosome = set(list(exchange_set2)[0:c] +
                            list(exchange_set1)[c:]).union(intersection)
    return child1, child2


class Individual:
    def __init__(self, p=None, G=None):
        if p is None or G is None:
            self.fitness = float('inf')
            self.chromosome = set()
        else:
            self.chromosome = set(sample(set(G.nodes()), p))

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
