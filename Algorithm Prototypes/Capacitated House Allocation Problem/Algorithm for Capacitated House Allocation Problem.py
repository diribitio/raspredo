# Python 3.7.3 - Capacitated House Allocation Problem Algorithm
# Programmer: Paul Maier
# 
# This is the python implementation of an algorithm to solve the Capacitated House Allocation Problem.
# It finds a popular matching for a given set of agents A and houses H with a set of strict perferences E (A, H) for every agent. 
#
# The algorithm is largely based on the paper 'Popular Matchings in the Capacitated House Allocation Problem' 
# by David F. Manlove and Collin T.S. Sng. For further details regarding the problem or mathematical aspects
# read the full paper. (University of Computing Science, University of Glasgow, Glasgow G12 8QQ, UK)


### Imports from python libraries ###

from random import randint
import networkx as nx
import matplotlib.pyplot as plt
import copy


### Class definitions ###
 
# Every agent has a name and strict preferences over a subset of all houses
class agent:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences

# Every house has a name and a capacity (maximum number of agents it can hold)
class house:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity


### Technical function definitions ###
    
# Gives back the house from H with the house_name and None if none exists
def find_house(house_name):
    for house in copy_H:
        if house.name == house_name:
                return house
    return None
    
# Gives back all fhouseagents in search_A for the for_house, returns [] if none exist
def fagents(for_house, search_A):
    fagents = []
    for agent in search_A:
        if agent.preferences[0].name == for_house.name:
            fagents.append(agent)
    return fagents

# Gives back the current house of the agent and None if the agent doesn't have one
def house_of_agent(agent):
    for matching in M:
        if matching[0] == agent:
            return matching[1]
    return None

# Gives back the number of agents matched to the house, returns [] if none are matched to it
def agents_in_house(house):
    agent_count = 0
    for matching in M:
        if matching[1] == house:
            agent_count += 1
    return agent_count

# Gives back the number of agents in whose list the house appears, returns [] if none exist
def agents_for_house(house):
    agent_count = 0
    for edge in E:
        if edge[1] == house.name:
            agent_count += 1
    return agent_count

# Promotes an agent from it's current house to the to_house, returns void
def promote(agent, to_house):
    for matching in M:
        if matching[1] == agent:
            M.remove(matching)
            matching[0].capacity += 1
    M.append((agent, to_house))


### Visual funktion definitions ###

# Draws a graph with the node groups A and H with the edges E, uses the networks and matplotlib.pyplot libraries
def draw_graph(A, H, E):
    G = nx.DiGraph()

    for house in H:
        G.add_node(house.name)
        G.nodes[house.name]["pos"] = pos=(H.index(house)*0.1+0.1, 0.1)

    for agent in A:
        G.add_node(agent.name)
        G.nodes[agent.name]["pos"] = pos=(A.index(agent)*0.05+0.05, 0.5)

    for edge in E:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    edges_large_green = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 3]
    edges_large_red = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 3]
    edges_normal = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 2]
    edges_small = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 1]

    pos = nx.get_node_attributes(G, "pos")

    nx.draw_networkx_edges(G, pos, edgelist=edges_large_green, width=2, edge_color="g", arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges_large_red, width=2, edge_color="r", arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges_normal, width=1, style="dashed", arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges_small, width=0.5, style="dashed", arrows=True)

    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    
    plt.show()

# Draws a network flow graph with the node groups A and H with the edges E and returns the max_flow_min_cost dictionary, uses the networks and matplotlib.pyplot libraries
def draw_network_flow_graph(A, H, E):
    G = nx.DiGraph()
    
    G.add_node("source")
    G.nodes["source"]["pos"] = pos=(0.2, 0.6)
    
    G.add_node("sink")
    G.nodes["sink"]["pos"] = pos=(0.2, 0.1)

    for house in H:
        G.add_node(house.name)
        G.nodes[house.name]["pos"] = pos=(H.index(house)*0.1+0.1, 0.2)

    for agent in A:
        G.add_node(agent.name)
        G.nodes[agent.name]["pos"] = pos=(A.index(agent)*0.05+0.05, 0.5)

    for edge in E:
        G.add_edge(edge[0], edge[1], weight=edge[2], capacity=edge[3])
            
    edges_large_red = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 1]
    edges_normal = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 2]
    edges_small = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] == 3]

    pos = nx.get_node_attributes(G, "pos")
    
    nx.draw_networkx_edges(G, pos, edgelist=edges_large_red, width=2, edge_color="r", arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges_normal, width=1, style="dashed", arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges_small, width=0.5, style="dashed", arrows=True)

    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_family="sans-serif")
    
    maximum_flow = nx.max_flow_min_cost(G, "source", "sink")
    
    if debug:
        print(maximum_flow)
    
    plt.show()
    
    return maximum_flow


### Variable definitions ###

# Determines if debug information should be printed 
debug=False

# The matchings in the form of (A, H)
M = []

# The agents of class Agent
A = []
# The houses of class House 
H = []
# The edges in the form of (A, H) 
E = []

# A copy of the agents of A
copy_A = []
# A copy of the houses of H
copy_H = []

# A subset of H where each house is the most desirable house of one or multiple agent of A
fhouses = []


### Preparations ###

# Generates the houses
for h in range(1, 7):
    name = "h" + str(h)
    H.append(house(name, 2) ) 

# Generates the agents with a prefernce list of size 3
for a in range(1, 12):
    name = "a" + str(a)
    
    preferences = []
    
    while len(preferences) < 3:
        new_preference = H[randint(0, len(H)-1)]
        
        if not new_preference in preferences:
            E.append((name, new_preference.name, 3-len(preferences)))
            preferences.append(new_preference)
    
    A.append(agent(name, preferences))

# Finds all fhouses and appends them to the fhouses array
for house in H:
    for agent in A:
        if house == agent.preferences[0] and not house in fhouses:
            fhouses.append(house)
            
# Copies A and H, uses the copy library
copy_A = copy.deepcopy(A)
copy_H = copy.deepcopy(H)

# Draws an inital graph of the generated problem
draw_graph(A, H, E)


### Algorithm for solving CHA

# Fill if possible up the fhouses with the according agents
for fhouse in fhouses:
    if len(fagents(fhouse, copy_A)) <= fhouse.capacity:
        for fagent in fagents(fhouse, A):
            M.append((fagent, fhouse))
            A.remove(fagent)
            
            remove_edges = []
            
            for fagentedge in E:
                if fagentedge[0] == fagent.name:
                    remove_edges.append(fagentedge)
            
            for remove_edge in remove_edges:
                E.remove(remove_edge)

# Prints (if debug) each house with the number of agents it has, its capacity and the number of agents that have it in their preferences
if debug:
    for house in H:
        print(house.name, agents_in_house(house), house.capacity, agents_for_house(house))

# Draw (if debug) the updated graph
if debug:
    draw_graph(A, H, E)

# Removes all isolated and full houses and the incident edges
remove_edges = []
remove_houses = []

for house in H:
    if debug:
        print(house.name, agents_in_house(house) == house.capacity or agents_for_house(house) == 0)

    if agents_in_house(house) == house.capacity or agents_for_house(house) == 0:
        remove_houses.append(house)
        for edge in E:
            if edge[1] == house.name:
                remove_edges.append(edge)
                
for remove_house in remove_houses:
    if remove_house in H:
        H.remove(remove_house)
    
for remove_edge in remove_edges:
    if remove_edge in E:
        E.remove(remove_edge)

# Draws if solved the graph with the matchings and if not (if debug) the updated graph
if len(A) == 0:
    edges_M = []
    
    for matching in M:
        edges_M.append((matching[0].name, matching[1].name, 4))

    print("Solved!")
    draw_graph(copy_A, copy_H, edges_M)
    exit()
else:
    if debug:
        draw_graph(A, H, E)


### Tries to compute a maximum matching from the remaining agents and houses

# Copies A, H and E
remaining_A = copy.deepcopy(A)
remaining_H = copy.deepcopy(H)
remaining_E= copy.deepcopy(E)

# Transforms the graph to a network flow and calulates the maximum_flow
transformed_E = []

for edge in remaining_E:
    transformed_E.append((edge[0], edge[1], 4-edge[2], 1))

remaining_E = transformed_E

for agent in A:
    remaining_E.append(("source", agent.name, 1, 1))

for house in H:
    remaining_E.append((house.name, "sink", 1, (house.capacity - agents_in_house(house))))

maximum_flow = draw_network_flow_graph(remaining_A, remaining_H, remaining_E)

# Applies the result of the maximum_flow to the matchings array M
for agent in remaining_A:
    if agent.name in maximum_flow.keys():
        for preference_name in maximum_flow[agent.name]:
            if maximum_flow[agent.name][preference_name] == 1:
                M.append((agent, find_house(preference_name)))

# Draws if solved (and if debug) the graph with the matchings, optimises and (always) draws it again and if no errors occur
edges_M = []

if len(M) == len(copy_A):    
    for matching in M:
        edges_M.append((matching[0].name, matching[1].name, 4))
        
    print("Kind of solved...")
        
    if debug:
        draw_graph(copy_A, copy_H, edges_M)
    
    print("Optimising...")

    for agent in copy_A:
        fĥouse = agent.preferences[0]
        if len(fagents(fhouse, copy_A)) > fhouse.capacity and agents_in_house(fhouse) < fhouse.capacity and house_of_agent(agent) != fhouse:
            promote(agent, fhouse)
            
    print("Totally super duper finished!")
            
    draw_graph(copy_A, copy_H, edges_M)
    exit()
else:
    print("No popular matching exists!")
   