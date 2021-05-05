import networkx as nx
import matplotlib.pyplot as plt
from CHAProblem import *
from random import randint

# The agents of class Agent
A = []
# The houses of class House 
H = []
# The edges in the form of (A, H) 
E = []

perferences_lenght = 3

# Generates the houses
for h in range(1, 16):
    name = "h" + str(h)
    H.append(house(name, 2) ) 

# Generates the agents with a prefernce list of size 3
for a in range(1, 30):
    name = "a" + str(a)
    
    preferences = []
    
    while len(preferences) < perferences_lenght:
        new_preference = H[randint(0, len(H)-1)]
        
        if not new_preference in preferences:
            E.append((name, new_preference.name, perferences_lenght-len(preferences)))
            preferences.append(new_preference)
    
    A.append(agent(name, preferences))

def draw_graph(A, H, E):
    oG = nx.DiGraph()

    for house in H:
        oG.add_node(house.name)
        oG.nodes[house.name]["pos"] = pos=(H.index(house)*0.1+0.1, 0.1)

    for agent in A:
        oG.add_node(agent.name)
        oG.nodes[agent.name]["pos"] = pos=(A.index(agent)*0.05+0.05, 0.5)

    for edge in E:
        oG.add_edge(edge[0], edge[1], weight=edge[2])
    
    edges_large_green = [(u, v) for (u, v, d) in oG.edges(data=True) if d["weight"] == 9999]
    edges_large_red = [(u, v) for (u, v, d) in oG.edges(data=True) if d["weight"] >= 3 and d['weight'] < 9999]
    edges_normal = [(u, v) for (u, v, d) in oG.edges(data=True) if d["weight"] == 2]
    edges_small = [(u, v) for (u, v, d) in oG.edges(data=True) if d["weight"] == 1]

    pos = nx.get_node_attributes(oG, "pos")

    nx.draw_networkx_edges(oG, pos, edgelist=edges_large_green, width=2, edge_color="g", arrows=True)
    nx.draw_networkx_edges(oG, pos, edgelist=edges_large_red, width=2, edge_color="r", arrows=True)
    nx.draw_networkx_edges(oG, pos, edgelist=edges_normal, width=1, style="dashed", arrows=True)
    nx.draw_networkx_edges(oG, pos, edgelist=edges_small, width=0.5, style="dashed", arrows=True)

    nx.draw_networkx_labels(oG, pos, font_size=10, font_family="sans-serif")
    
    plt.show()

chap = CHAProblem(A, H, E, False)
chap.solve()
draw_graph(chap.return_values['solution'][0]['agents'], chap.return_values['solution'][1]['houses'], chap.return_values['solution'][3]['matchings'])