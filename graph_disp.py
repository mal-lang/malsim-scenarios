import matplotlib.pyplot as plt
import networkx as nx
import json
import os
from networkx.drawing.nx_pydot import graphviz_layout


exp = "exp0"

attack_graph = os.path.join(exp,"tmp","attack_graph.json")
file = open(attack_graph)

data = json.load(file)

G = nx.DiGraph()
color_map = []

for nodes in data: 
    node = f'"{nodes["id"]}"'
    G.add_node(node, **{'type' :nodes['type']})
    for child in nodes["children"]: 
        c = f'"{child}"'
        G.add_edge(node,c)



for key,value in nx.get_node_attributes(G,"type").items(): 
    print(key)
    if value == 'or' and 'Attacker' not in key :
        color_map.append('green')
    elif value == 'and' and 'Attacker' not in key:
        color_map.append('orange')
    elif 'Attacker' in key:
        color_map.append('red')
    else: 
        color_map.append('blue')

pos = graphviz_layout(G, prog="dot")  
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color=color_map, font_size=10, font_weight="bold", arrowsize=20)
plt.show()