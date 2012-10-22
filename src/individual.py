import random
from custom_io import get_graph_from_input


def crossover(i1, i2):
    '''accomplishes the crossover between two individual'''
    i = random.randint(1, len(i1.chromosome) - 2)
    child1, child2 = Individual(), Individual()
    child1.chromosome = set(list(i1.chromosome)[0:i] + list(i2.chromosome)[i:])
    child2.chromosome = i1.chromosome.union(i2.chromosome) - child1.chromosome
    return child1, child2


class Individual:
    def __init__(self):
        self.fitness = -1
        self.chromosome = set()

    def __repr__(self):
        return self.chromosome

    def __str__(self):
        return str(self.chromosome)

    def be_random(self, p, G):
        '''generates a random chromosome based on given graph nodes'''
        self.chromosome = set(random.sample(set(G.nodes()), p))

    def from_crossover(self, individual1, individual2):
        '''not to be used'''
        i = random.randint(1, len(individual1.chromosome) - 2)
        self.chromosome = set(list(individual1.chromosome)[0:i] +
                              list(individual2.chromosome)[i:])

    def mutate(self, G):
        '''a random gene has its allele swapped by a random facility
        given the new facility is not present in the chromosome
        '''
        new_median = random.choice(G.nodes())
        while new_median in self.chromosome:
            new_median = random.choice(G.nodes())
        self.chromosome.remove(random.choice(list(self.chromosome)))
        self.chromosome.add(new_median)

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
    i1 = Individual()
    i1.be_random(5, G)
    print i1.calculate_fitness(G)
