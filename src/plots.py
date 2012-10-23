# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt, rcParams, rc
from datetime import datetime as dt
from cPickle import load

rc('font', **{'family': 'serif', 'serif': ['Times']})
rcParams['text.usetex'] = True
rcParams['text.latex.unicode'] = True


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


def multi_plot(data_list, xlabel, ylabel, file_name=None):
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
        l, = ax.plot(x_nums, data)
        legend_elements.append(l)
        legend_descriptions.append(legend)
    ax.set_xlim(longest_nums_list[0] - 1, longest_nums_list[-1] + 1)
    ax.autoscale_view()
    ax.grid(True)
    fig.legend(legend_elements, legend_descriptions)
    if file_name:
        plt.savefig('plots/' + file_name + '.pdf', bbox_inches='tight')
    else:
        plt.savefig('plots/test' + str(dt.now()) + '.pdf', bbox_inches='tight')


def plot_population_impact(file_name):
    f1 = load(open('dumps/100-100-0.001-0.6-2-0.01', 'r'))
    f2 = load(open('dumps/500-100-0.001-0.6-2-0.01', 'r'))
    f3 = load(open('dumps/1000-100-0.001-0.6-2-0.01', 'r'))
    multi_plot([(f1, '100'), (f2, '500'), (f3, '1000')], u'Geração',
                u'Fitness (000s)', file_name)

if __name__ == '__main__':
    plot_population_impact('population_impact')
