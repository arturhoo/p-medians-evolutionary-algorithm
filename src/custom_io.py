import networkx as nx
from math import sqrt
from sys import exit, exc_info


def get_number_of_medians(file_name):
    with open(file_name) as f:
        content = f.readlines()
        f.close()
    return int(content[0].strip().split()[1])


def get_graph(file_name):
    G = nx.Graph()
    try:
        with open(file_name) as f:
            content = f.readlines()
            f.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit()
    except:
        print "Unexpected error:", exc_info()[0]
        exit()
    added_points = []
    for line in content[1:]:
        elements = line.strip().split()
        x_coord = float(elements[0])
        y_coord = float(elements[1])
        capacity = float(elements[2])
        demand = float(elements[3])
        cur_point = (x_coord, y_coord)
        assert len(cur_point) == 2
        G.add_node(cur_point, demand=demand, capacity=capacity)
        for point in added_points:
            # calculating the distance between points
            b = cur_point[1] - point[1]
            c = cur_point[0] - point[0]
            a = sqrt(b ** 2 + c ** 2)
            G.add_edge(cur_point, point, weight=a)
        added_points.append(cur_point)

    return G
