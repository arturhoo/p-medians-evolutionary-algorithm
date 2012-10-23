# -*- coding: utf-8 -*-
from individual import Individual, mutate, crossover
from custom_io import get_graph, get_number_of_medians
from random import sample, random
from copy import deepcopy
from math import ceil
from argparse import ArgumentParser
from pprint import pprint
from time import clock


def unique_individuals(pop):
    seen = set()
    return len([x for x in pop if frozenset(x.chromosome) not in seen
                and not seen.add(frozenset(x.chromosome))])


def rank_population(pop):
    scores = [(i.fitness, i) for i in pop]
    scores.sort()
    return [i for (s, i) in scores]


def evolve(G, p, popsize, gener, mutprob, coprob, tsize, elitism=None):
    nodes_ordered_by_demand = sorted(G.node.items(),
                                     key=lambda t: t[1]['demand'],
                                     reverse=True)
    t1 = clock()
    pop = []
    # generating first population, which will be random
    for i in range(popsize):
        individual = Individual(p, G)
        individual.calculate_fitness(G, nodes_ordered_by_demand)
        pop.append(individual)

    rank_population(pop)
    report = {
        'worst_i': pop[-1].fitness,
        'best_i': pop[0].fitness,
        'generation': 0,
        'better_sons': 0,
        'total_sons': 0,
        'best_i_hist': [pop[0].fitness],
        'mean_fitness_hist': [sum([i.fitness for i in pop]) / popsize],
        'repeated_i_hist': [popsize - unique_individuals(pop)]
    }
    for generation in range(gener):
        # applying elitism if relevant
        if elitism:
            topelite = int(ceil(elitism * popsize))
            new_pop = pop[0:topelite]
        else:  # if no elitism specified, simply create a new population
            new_pop = []

        # while the population is not complete
        while len(new_pop) < popsize:
            random_number = random()
            subpop = sample(pop, tsize)  # tournament individuals
            if random_number < mutprob:  # mutating
                new_pop.append(mutate(subpop[0], G))
                new_pop[-1].calculate_fitness(G, nodes_ordered_by_demand)
            elif random_number < coprob:  # doing crossover
                mean_fitness = (subpop[0].fitness + subpop[1].fitness) / 2.0
                i1, i2 = crossover(subpop[0], subpop[1])
                i1.calculate_fitness(G, nodes_ordered_by_demand)
                if i1.fitness > mean_fitness:
                    report['better_sons'] += 1
                report['total_sons'] += 1
                new_pop.append(i1)
                if i2 is not None:
                    i2.calculate_fitness(G, nodes_ordered_by_demand)
                    if i2.fitness > mean_fitness:
                        report['better_sons'] += 1
                    new_pop.append(i2)
                    report['total_sons'] += 1
            else:  # if no mutation or crossover, insert the best individual
                new_pop.append(deepcopy(subpop[0]))
            if len(new_pop) > popsize:
                new_pop.pop()
                report['total_sons'] -= 1
        pop = rank_population(new_pop)
        report['best_i_hist'].append(pop[0].fitness)
        report['mean_fitness_hist'].append(sum([i.fitness for i in pop]) /
                                                  popsize)
        report['repeated_i_hist'].append(popsize - unique_individuals(pop))
        if report['best_i'] > pop[0].fitness:
            report['best_i'] = pop[0].fitness
            report['generation'] = generation
        if report['worst_i'] < pop[-1].fitness:
            report['worst_i'] = pop[-1].fitness

    t2 = clock()
    report['time'] = round(t2 - t1, 3)
    report['gener_per_s'] = gener / report['time']
    return report


if __name__ == '__main__':
    parser = ArgumentParser(description='''Evolutionary Algorithm for
                                           the P-Median Problem''')
    parser.add_argument('inst', help='instance to be solved')
    parser.add_argument('popsize', type=int, help='population size')
    parser.add_argument('gener', type=int, help='number of generations')
    parser.add_argument('mutprob', type=float, help='probability of mutation')
    parser.add_argument('coprob', type=float, help='probability of crossover')
    parser.add_argument('tsize', type=int, help='tournament size')
    parser.add_argument('-e', '--elitism', type=float,
                        help='use of elitism')
    args = vars(parser.parse_args())

    G = get_graph(args['inst'])
    p = get_number_of_medians(args['inst'])
    print '---Parameters:'
    for k, v in args.iteritems():
        print k + ': ' + str(v)
    print 'p:', str(p)

    report = evolve(G, p, args['popsize'], args['gener'], args['mutprob'],
                    args['coprob'], args['tsize'], args['elitism'])
    print '---Report:'
    pprint(report)
