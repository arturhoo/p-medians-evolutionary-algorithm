# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt, rcParams, rc
from datetime import datetime as dt
from cPickle import load

rc('font', **{'family': 'serif', 'serif': ['Times'], 'size': 22})
rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = True
colors = ['b', 'r', 'g', 'k', 'm', 'c', 'y']
symbols = ['-', '--', '-.']
nc = len(colors)
ns = len(symbols)


def simple_plot(data, xlabel, ylabel):
    x = range(len(data))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(x[0] - 1, x[-1] + 1)
    ax.plot(x, data)
    ax.autoscale_view()
    ax.grid(True)
    plt.savefig('test' + str(dt.now()) + '.png')


def multi_plot(data_list, xlabel, ylabel, file_name=None, best=None):
    count = 0
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    longest_nums_list = []
    legend_elements = []
    legend_descriptions = []
    for data, legend in data_list:
        x_nums = range(len(data))
        if len(x_nums) > len(longest_nums_list):
            longest_nums_list = x_nums
        l, = ax.plot(x_nums, data, colors[count % nc] + symbols[count % ns],
                     linewidth=2)
        count += 1
        if legend is not None:
            legend_elements.append(l)
            legend_descriptions.append(legend)
    if best is not None:
        best_l = [best] * len(longest_nums_list)
        l, = ax.plot(longest_nums_list, best_l,
                     colors[count % nc] + symbols[count % ns], linewidth=2)
        count += 1
        legend_elements.append(l)
        legend_descriptions.append(u'Ótimo')
    # ax.set_xlim(longest_nums_list[0] - 1, longest_nums_list[-1] + 1)
    ax.autoscale_view()
    ax.grid(True)
    fig.legend(legend_elements, legend_descriptions, 'upper center', ncol=2)
    if file_name:
        plt.savefig('plots/' + file_name + '.pdf')
    else:
        plt.savefig('plots/test' + str(dt.now()) + '.pdf', bbox_inches='tight')


def plot_population_impact(file_name):
    f1 = load(open('dumps/100-100-0.001-0.6-2-0.01', 'r'))
    f2 = load(open('dumps/500-100-0.001-0.6-2-0.01', 'r'))
    f3 = load(open('dumps/1000-100-0.001-0.6-2-0.01', 'r'))
    multi_plot([(f1, '100'), (f2, '500'), (f3, '1000')], u'Geração',
                u'Média da melhor fitness (x1000)', file_name, 17246.53 / 1000)


def plot_generation_impact(file_name):
    f1 = load(open('dumps/200-4950-0.001-0.6-2-0.01', 'r'))
    multi_plot([(f1, '4950'), ([], None), ([], None)], u'Geração',
                u'Média da melhor fitness (x1000)', file_name, 17246.53 / 1000)


def plot_coprob_impact(file_name):
    f1 = load(open('dumps/200-250-0.001-0.25-2-0.01', 'r'))
    f2 = load(open('dumps/200-250-0.001-0.5-2-0.01', 'r'))
    f3 = load(open('dumps/200-250-0.001-0.75-2-0.01', 'r'))
    multi_plot([(f1, '0.25'), (f2, '0.50'), (f3, '0.75')], u'Geração',
                u'Média da melhor fitness (x1000)', file_name, 17246.53 / 1000)


def plot_mutprob_impact(file_name):
    f1 = load(open('dumps/200-250-0.001-0.6-2-0.01', 'r'))
    f2 = load(open('dumps/200-250-0.01-0.6-2-0.01', 'r'))
    f3 = load(open('dumps/200-250-0.1-0.6-2-0.01', 'r'))
    multi_plot([(f1, '0.001'), (f2, '0.01'), (f3, '0.1')], u'Geração',
                u'Média da melhor fitness (x1000)', file_name, 17246.53 / 1000)


def plot_tsize_impact(file_name):
    f1 = load(open('dumps/200-250-0.1-0.6-2-0.01', 'r'))
    f2 = load(open('dumps/200-250-0.1-0.6-5-0.01', 'r'))
    f3 = load(open('dumps/200-250-0.1-0.6-15-0.01', 'r'))
    multi_plot([(f1, '2'), (f2, '5'), (f3, '15')], u'Geração',
                u'Média da melhor fitness (x1000)', file_name, 17246.53 / 1000)


def plot_elitism_impact(file_name):
    f1 = load(open('dumps/200-250-0.1-0.6-2-0.0', 'r'))
    f2 = load(open('dumps/200-250-0.1-0.6-2-0.01', 'r'))
    f3 = load(open('dumps/200-250-0.1-0.6-2-0.1', 'r'))
    multi_plot([(f1, '0.0'), (f2, '0.01'), (f3, '0.1')], u'Geração',
                u'Média da melhor fitness (x1000)', file_name, 17246.53 / 1000)

if __name__ == '__main__':
    plot_population_impact('popsize_impact')
    plot_generation_impact('gener_impact')
    plot_coprob_impact('coprob_impact')
    plot_mutprob_impact('mutprob_impact')
    plot_tsize_impact('tsize_impact')
    plot_elitism_impact('elitism_impact')
