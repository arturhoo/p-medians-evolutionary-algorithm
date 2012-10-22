import random
from io import get_graph_from_input


def crossover(individual1, individual2):
    i = random.randint(1, len(individual1.chromosome) - 2)
    child1 = Individual()
    child2 = Individual()
    child1.chromosome = set(list(individual1.chromosome)[0:i] +
                            list(individual2.chromosome)[i:])
    child2.chromosome = set(list(individual2.chromosome)[0:i] +
                            list(individual1.chromosome)[i:])
    return (child1, child2)


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
        new_median = random.choice(G.nodes())
        while new_median in self.chromosome:
            new_median = random.choice(G.nodes())
        self.chromosome.remove(random.choice(list(self.chromosome)))
        self.chromosome.add(new_median)

    def calculate_fitness(self, G):
        pass


if __name__ == '__main__':
    pass
