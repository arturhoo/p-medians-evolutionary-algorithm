import networkx as nx
import math

G = nx.Graph()

with open('../data/SJC1.dat') as f:
    content = f.readlines()
    f.close()

added_points = []
pos = {}

for line in content[1:]:
    elements = line.strip().split()
    x_coord = float(elements[0])
    y_coord = float(elements[1])
    cur_point = (x_coord, y_coord)
    assert len(cur_point) == 2
    G.add_node(cur_point)
    for point in added_points:
        b = cur_point[1] - point[1]
        c = cur_point[0] - point[0]
        a = math.sqrt(b ** 2 + c ** 2)
        G.add_edge(cur_point, point, weight=a)
    added_points.append(cur_point)
    pos[cur_point] = cur_point
