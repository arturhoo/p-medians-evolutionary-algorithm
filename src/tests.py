from unittest import TestCase, main as unittestMain
from custom_io import get_graph_from_input
from individual import Individual, crossover, mutate
import random


class TestIndividual(TestCase):
    p = random.randint(2, 10)
    G = get_graph_from_input('../data/SJC1.dat')
    i1 = Individual(p, G)
    i2 = Individual(p, G)

    def testMutation(self):
        i3 = mutate(self.i1, self.G)
        intersection = self.i1.chromosome.intersection(i3.chromosome)
        self.assertEqual(len(i3.chromosome), self.p)
        self.assertEqual(len(intersection), self.p - 1)
        self.assertNotEqual(self.i1, i3)

    def testCrossover(self):
        (i3, i4) = crossover(self.i1, self.i2)
        union1 = self.i1.chromosome.union(self.i2.chromosome)
        union2 = i3.chromosome.union(i4.chromosome)
        self.assertEqual(union1, union2)
        self.assertEqual(len(i3.chromosome), self.p)
        self.assertEqual(len(i4.chromosome), self.p)


if __name__ == '__main__':
    unittestMain()
