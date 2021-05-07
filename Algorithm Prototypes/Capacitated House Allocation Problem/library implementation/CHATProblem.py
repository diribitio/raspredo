# Python 3.7.3 - Capacitated House Allocation Problem
# Programmer: Paul Maier
# 
# This is the python implementation of the Capacitated House Allocation Problem with Ties and an algorithm to solve it.
# The algorithm finds a popular matching for a given instance of the Capacitated House Allocation Problem with Ties. 
#
# The algorithm is largely based on the paper 'Popular Matchings in the Capacitated House Allocation Problem' 
# by David F. Manlove and Collin T.S. Sng. For further details regarding the problem and mathematical aspects
# read the full paper. (University of Computing Science, University of Glasgow, Glasgow G12 8QQ, UK)


### Imports from python libraries ###

import matplotlib.pyplot as plt
import networkx as nx
import copy


### Class definitions ###
 
# Every agent has a name and preferences over a subset of all houses. The prferences may conrain ties and therefore need to contain only tuples
class agent:
    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences

# Every house has a name and a capacity (maximum number of agents it can hold)
class house:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

# The class Capacitated House Allocation Problem with Ties can be instanced with the agents, houses and edges and solved using the solve() function
class CHATProblem:
    def __init__(self, agents, houses, edges, debug=False, matched_weight=9999, prefernces_lenght=4):
        # Determines if debug information should be printed 
        self.debug=debug

        # The agents of class Agent
        self.A = agents
        # The houses of class House 
        self.H = houses
        # The edges in the form of (A, H) 
        self.E = edges
        
        # Dictionary of all values to be returned
        self.return_values = {}
        
        # The weight of edges which indicate a match
        self.matched_weight = matched_weight
        
        # The maximum lengh of an agnets prefernces
        self.preferences_lenght = prefernces_lenght


    ### Technical function definitions ###
    
    # Saves the given state to the return_values
    def append_to_return_matching_state(self, name, A, H, E, M):
        self.return_values[name] = [{'agents':copy.deepcopy(A)}, {'houses':copy.deepcopy(H)}, {'edges':copy.deepcopy(E)}, {'matchings':copy.deepcopy(M)}]
    
    # Gives back the house from in search_H with the house_name and None if none exists
    def find_house(self, house_name, search_H):
        for find_house in search_H:
            if find_house.name == house_name:
                return find_house
        return None
        
    # Gives back all fhouseagents in search_A for the for_house, returns [] if none exist
    def fagents(self, for_house, search_A):
        fagents = []
        for find_agent in search_A:
            for loop_preference in find_agent.preferences[0]:
                if for_house.name == loop_preference.name:
                    fagents.append(find_agent)
                    break
        return fagents

    # Gives back the current house of the search_agent and None if the agent doesn't have one
    def house_of_agent(self, search_agent, search_M):
        for matching in search_M:
            if matching[0] == search_agent:
                return matching[1]
        return None

    # Gives back the number of agents matched to the search_house, returns [] if none are matched to it
    def agents_in_house(self, search_house, search_M):
        agent_count = 0
        for matching in search_M:
            if matching[1] == search_house:
                agent_count += 1
        return agent_count

    # Gives back the number of agents in whose list the house appears, returns [] if none exist
    def agents_for_house(self, search_house, search_E):
        agent_count = 0
        for edge in search_E:
            if edge[1] == search_house.name:
                agent_count += 1
        return agent_count

    # Promotes an agent from it's current house to the to_house, returns void
    def promote(self, promote_agent, to_house, search_M):
        for matching in search_M:
            if matching[1] == promote_agent:
                search_M.remove(matching)
                matching[0].capacity += 1
        search_M.append((promote_agent, to_house))


    ### Graph function definitions ###

    # Draws (if debug) a network flow graph with the node groups A and H with the edges E and returns the max_flow_min_cost dictionary, uses the networks and matplotlib.pyplot libraries
    def draw_network_flow_graph(self, A, H, E):
        G = nx.DiGraph()
        
        G.add_node('source')
        G.nodes['source']['pos'] = pos=(0.2, 0.6)
        
        G.add_node('sink')
        G.nodes['sink']['pos'] = pos=(0.2, 0.1)

        for loop_house in H:
            G.add_node(loop_house.name)
            G.nodes[loop_house.name]['pos'] = pos=(H.index(loop_house)*0.1+0.1, 0.2)

        for loop_agent in A:
            G.add_node(loop_agent.name)
            G.nodes[loop_agent.name]['pos'] = pos=(A.index(loop_agent)*0.05+0.05, 0.5)

        for edge in E:
            G.add_edge(edge[0], edge[1], weight=edge[2], capacity=edge[3])
                
        edges_large_red = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 1]
        edges_normal = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 2]
        edges_small = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] == 3]

        pos = nx.get_node_attributes(G, 'pos')
        
        nx.draw_networkx_edges(G, pos, edgelist=edges_large_red, width=2, edge_color='r', arrows=True)
        nx.draw_networkx_edges(G, pos, edgelist=edges_normal, width=1, style='dashed', arrows=True)
        nx.draw_networkx_edges(G, pos, edgelist=edges_small, width=0.5, style='dashed', arrows=True)

        nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
        
        edge_labels = nx.get_edge_attributes(G, 'capacity')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_family='sans-serif')
        
        maximum_flow = nx.max_flow_min_cost(G, 'source', 'sink')
        
        if self.debug:
            self.return_values['maximum_flow'] = maximum_flow
        
        plt.clf()
                
        return maximum_flow


    ### Algorithm for solving CHA ###

    # Uses the algorithm from the paper (see top of page) to calculate a popular matching if one exists
    def solve(self):
        # The matchings in the form of (agent, house)
        M = []
        # Copies of A, H and E, uses the copy library
        A = copy.deepcopy(self.A)
        H = copy.deepcopy(self.H)
        E = copy.deepcopy(self.E)
        # A deep copy of the agents of A, uses the copy library
        copy_A = copy.deepcopy(A)
        # A deep copy of the houses of H, uses the copy library
        copy_H = copy.deepcopy(H)
        
        # A subset of H where each house is the most desirable house of one or multiple agent of A
        fhouses = []
        
        # Gives back (if debug) an inital graph of the given problem
        if self.debug:
            self.append_to_return_matching_state('initial', A, H, E, [])

        # Finds all fhouses and appends them to the fhouses array
        for loop_house in H:
            for loop_agent in A:
                for loop_prefernece in loop_agent.preferences[0]:
                    if loop_house.name == loop_prefernece.name and not loop_house in fhouses:
                        fhouses.append(loop_house)
                        break
        
        # Calcuates the first-choice graph, with Ef which only contains edges between first houses an their agents
        Af = copy.deepcopy(self.A)
        Hf = copy.deepcopy(self.H)
        Ef = []
        
        for edge in E:
            if edge[2] == self.preferences_lenght: # Higher number -> higher preference (the maximum preference lenght of all agents should represent the first choice)
                Ef.append(edge)
        
        # Transforms the fist choice graph to a network flow and calulates the maximum_flow
        transformed_Ef = []

        for edge in Ef:
            transformed_Ef.append((edge[0], edge[1], self.preferences_lenght-edge[2], 1)) # Max flow min cost algorithm -> weight must be small for higher prefernces (0 should represent the first choice)
        
        for loop_agent in Af:
            transformed_Ef.append(('source', loop_agent.name, 1, 1))

        for loop_house in Hf:
            transformed_Ef.append((loop_house.name, 'sink', 1, loop_house.capacity))

        maximum_flow = self.draw_network_flow_graph(Af, Hf, transformed_Ef)

        print(maximum_flow)
        
        exit()

        # Fill if possible up the fhouses with the according agents
        for fhouse in fhouses:
            if len(self.fagents(fhouse, copy_A)) <= fhouse.capacity:
                for fagent in self.fagents(fhouse, A):
                    M.append((fagent, fhouse))
                    A.remove(fagent)
                    
                    remove_edges = []
                    
                    for fagentedge in E:
                        if fagentedge[0] == fagent.name:
                            remove_edges.append(fagentedge)
                    
                    for remove_edge in remove_edges:
                        E.remove(remove_edge)

        # Gives back (if debug) the updated graph
        if self.debug:
            self.append_to_return_matching_state('fhouses filled', A, H, E, [])

        # Removes all isolated and full houses and the incident edges
        remove_edges = []
        remove_houses = []

        for loop_house in H:
            if self.agents_in_house(loop_house, M) == loop_house.capacity or self.agents_for_house(loop_house, E) == 0:
                remove_houses.append(loop_house)
                for edge in E:
                    if edge[1] == loop_house.name:
                        remove_edges.append(edge)
                        
        for remove_house in remove_houses:
            if remove_house in H:
                H.remove(remove_house)
            
        for remove_edge in remove_edges:
            if remove_edge in E:
                E.remove(remove_edge)

        # Gives back (if debug) if solved the graph with the matchings and if not the cleaned graph
        if len(A) == 0:
            edges_M = []
            
            for matching in M:
                edges_M.append((matching[0].name, matching[1].name, self.matched_weight))
            
            self.append_to_return_matching_state('solution', copy_A, copy_H, [], edges_M)
            return
        else:
            if self.debug:
                self.append_to_return_matching_state('removed filled/unwanted houses', A, H, E, [])


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

        for loop_agent in A:
            remaining_E.append(('source', loop_agent.name, 1, 1))

        for loop_house in H:
            remaining_E.append((loop_house.name, 'sink', 1, (loop_house.capacity - self.agents_in_house(loop_house, M))))

        maximum_flow = self.draw_network_flow_graph(remaining_A, remaining_H, remaining_E)

        # Applies the result of the maximum_flow to the matchings array M
        for remaining_agent in remaining_A:
            if remaining_agent.name in maximum_flow.keys():
                for preference_name in maximum_flow[remaining_agent.name]:
                    if maximum_flow[remaining_agent.name][preference_name] == 1:
                        M.append((remaining_agent, self.find_house(preference_name, copy_H)))

        # Gives back if solved the graph with the optimized matchings and if not an empty graph
        edges_M = []

        if len(M) == len(copy_A):    
            for matching in M:
                edges_M.append((matching[0].name, matching[1].name, self.matched_weight))

            #for copy_agent in copy_A:
            #    print(copy_agent.preferences)
            #    if len(self.fagents(copy_agent.preferences[0], copy_A)) > copy_agent.preferences[0].capacity and self.agents_in_house(copy_agent.preferences[0], M) < copy_agent.preferences[0].capacity and self.house_of_agent(copy_agent, M) != copy_agent.preferences[0]:
            #        self.promote(copy_agent, copy_agent.preferences[0], M)

            self.append_to_return_matching_state('solution', copy_A, copy_H, [], edges_M)
            return
        else:
            self.append_to_return_matching_state('solution', copy_A, copy_H, [], [])
            return

if __name__ == "__main__":
    h1 = house("h1", 2)
    h2 = house("h2", 1)
    h3 = house("h3", 2)

    a1 = agent("a1", [(h1, h2), (h3)])
    a2 = agent("a2", [(h3,)])
    a3 = agent("a3", [(h1, h2)])
    a4 = agent("a4", [(h3,)])
    a5 = agent("a5", [(h3,)])

    H1 = [h1, h2, h3]
    A1 = [a1, a2, a3, a4, a5]
    E1 = [("a1", "h1", 2),
          ("a1", "h2", 2),
          ("a1", "h3", 1),
          ("a2", "h3", 2),
          ("a3", "h1", 2),
          ("a3", "h2", 2),
          ("a4", "h3", 2),
          ("a5", "h3", 2)]

    chatp = CHATProblem(A1, H1, E1, False, 9999, 2)
    chatp.solve()
    print(chatp.return_values['solution'][0]['agents'], chatp.return_values['solution'][1]['houses'], chatp.return_values['solution'][3]['matchings'])
