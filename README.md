# p-Medians Evolutionary Algorithm

##

The documentation (in Portuguese) is located in the directory `doc`, and the
reference file is `doc/tp1.pdf`.

## Instances

The instances are located in the `data` dir and were obtained from this
[link][instances]. Here is a brief description:

    +-----------+-------+----+----------+
    |   File    | Nodes | P  | Optimum  |
    +-----------+-------+----+----------+
    | SJC1.dat  |   100 | 10 | 17246.53 |
    | SJC2.dat  |   200 | 15 | 33225.88 |
    | SJC3b.dat |   300 | 30 | 40635.80 |
    | SJC4a.dat |   402 | 30 | 61843.23 |
    +-----------+-------+----+----------+

## Implementation

The algorithm was implemented in Python and its code can be found at the
`src` directory. It depends on the package
[networkx][networkx].

Here is a brief description of the files:

* `custom_io.py`: responsible for "converting" the data in the instance files
(located in the `data` dir) into `networkx`'s Graphs.
* `individual.py`: contains the class of an Individual, in the evolutionary
sense of the word, together with the methods responsible for mutation and
crossover of those individuals
* `p-medians.py`: main file, contains the `evolve` method, which operates the
evolutionary "machine", reporting relevant info about the process
* `tests.py`: a few unit test for the Individual class

The way the evolutionary algorithm was implemeted allows the tuning of multiple
parameters, as follows:

    positional arguments:
      inst                  instance to be solved
      popsize               population size
      gener                 number of generations
      mutprob               probability of mutation
      coprob                probability of crossover
      tsize                 tournament size

    optional arguments:
      -h, --help            show this help message and exit
      -e ELITISM, --elitism ELITISM
                            use of elitism

Here is a sample parameters configuration:

    $ python src/p-medians.py data/SJC1.dat 200 250 0.1 0.6 2 -e 0.1

and here is the sample output explained(simplified for clarity):

    ---Parameters:
    tsize: 2
    gener: 50
    popsize: 5
    elitism: 0.1
    inst: data/SJC1.dat
    mutprob: 0.1
    coprob: 0.6
    p: 10
    ---Report:
    {'best_i': 6,  # fitness of the best individual
     'best_i_hist': [12, (...), 6],  # fitness of the best individual at each generation
     'better_sons': 40,  # total number of sons that have better fitness than their parents
     'gener_per_s': 153.37  # number of generations per second
     'generation': 44,  # generation on which first appeared the best overall individual
     'mean_fitness_history': [10, (...), 9],  # mean fitness the population at each generation
     'repeated_i_hist': [2, (...), 4]  # number of repeated individuals at each generation
     'time': 0.326,  # time spent in the evolutionary process
     'total_sons': 123,  # totnal number of sons generated through crossover
     'worst_i': 28  # fitness of the worst individual in the final generation
    }

### Configuring your Python Environment

These instruction are for the configuration of the Python environment under
Ubuntu 12.04

Firstly, certify your system is up-to-date

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get dist-upgrade

If a system restart is required, proceed

    $ sudo shutdown -r now

Then, install the Python packages

    $ sudo apt-get install python-setuptools python-pip python-dev

After that, install [`virtualenv`](http://www.virtualenv.org/), which is a tool
that allows the creating of multiple, self-contained, Python environments

    $ sudo pip install virtualenv

Let's also install
[`virtualenvwrapper`](http://www.doughellmann.com/projects/virtualenvwrapper/),
which extends `virtualenv` by making the management of these environments
easier

    $ mkdir -p ~/.virtualenvs
    $ echo 'export WORKON_HOME=~/.virtualenvs' >> ~/.bashrc
    $ source .bashrc
    $ sudo pip install virtualenvwrapper
    $ echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
    $ source .bashrc

We should now create a environment for the project
`p-medians-evolutionary-algorithm`

    $ mkvirtualenv pmea
    $ workon pmea

Every Python package we install from now on will be installed only in the
`pmea` environment. We proceed, by installing the only non-standard module

    (pmea)$ pip install networkx

That's it! The environment is now setup and we should be able to run the code

    (pmea)$ python src/p-medians.py data/SJC1.dat 200 250 0.1 0.6 2 -e 0.1

  [instances]: http://www.lac.inpe.br/~lorena/instancias.html
  [networkx]: http://networkx.lanl.gov/index.html
