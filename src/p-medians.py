from individual import Individual, mutate, crossover
from custom_io import get_graph, get_number_of_medians
from random import sample, random
from copy import deepcopy
from math import ceil
from argparse import ArgumentParser


def rank_population(pop, G, nodes_ordered_by_demand):
    scores = [(i.calculate_fitness(G, nodes_ordered_by_demand), i)
              for i in pop]
    scores.sort()
    return [i for (s, i) in scores]


def evolve(G, p, popsize, gener, mutprob, coprob, tsize, elitism=None):
    nodes_ordered_by_demand = sorted(G.node.items(),
                                     key=lambda t: t[1]['demand'],
                                     reverse=True)

    pop = []
    # generating first population, which will be random
    for i in range(popsize):
        individual = Individual(p, G)
        pop.append(individual)

    rank_population(pop, G, nodes_ordered_by_demand)
    best_individual = {'i': pop[0], 'generation': 0}
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
            elif random_number < coprob:  # doing crossover
                i1, i2 = crossover(subpop[0], subpop[1])
                new_pop.append(i1)
                new_pop.append(i2)
            else:  # if no mutation or crossover, insert the best individual
                new_pop.append(deepcopy(subpop[0]))
            if len(new_pop) > popsize:
                new_pop.pop()
        pop = rank_population(new_pop, G, nodes_ordered_by_demand)

        if best_individual['i'].fitness >= pop[0].fitness:
            best_individual['i'] = pop[0]
            best_individual['generation'] = generation

    print 'Best individual at generation', \
          str(best_individual['generation']), '\n', \
          'Fitness:', str(best_individual['i'].fitness)
    return best_individual


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
    for k, v in args.iteritems():
        print k + ': ' + str(v)

    G = get_graph(args['inst'])
    p = get_number_of_medians(args['inst'])
    best = evolve(G, p, args['popsize'], args['gener'], args['mutprob'],
                  args['coprob'], args['tsize'], args['elitism'])
