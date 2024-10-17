from math import log2
import csv
import graphviz
import random

print("Welcome to Decision Tree Generator")

# zwraca słownik ktory ma strukture 
# {
#     ...
#     <nazwa_wartości_atrybutu>: [ 
#         <ilość_decyzji_yes>,
#         <lista_indeksów_z_tym_parameterem>
#     ]
#     ...
# }
def count_attribute_values(attribute, decision):
    attribute_dir = {}
    for idx in range(1, len(attribute)):
        if attribute[idx] not in attribute_dir:
            attribute_dir[attribute[idx]] = [
                    decision_to_int(decision[idx]),
                    [idx]
            ]
        else:
            attribute_dir[attribute[idx]][0] += decision_to_int(decision[idx])
            attribute_dir[attribute[idx]][1] += [idx]
    return attribute_dir

# zwraca IntrinsicInfo dla danego atrybutu 
def intrinsic_info(attribute_dir):
    values = list(attribute_dir.values())
    res = 0
    all_vals_count = sum(len(sublist[1]) for sublist in values)
    for val in values:
        a = len(val[1])/all_vals_count
        res -= a * log2(a)
    return res

# zwraca entropy dla danego atrybutu 
def entropy_for_attribute(attribute_dir):
    values = attribute_dir.values()
    all_vals_count = sum(len(sublist[1]) for sublist in values)
    entropy_for_attribute = 0
    for val in values:
        entropy_for_attribute += (len(val[1])/all_vals_count) * entropy(val[0], len(val[1]))
    return entropy_for_attribute

# y to jest ilość yes'ow 
# a to ilość wszystkich pojawień się tej wartości 
def entropy(y, a):
    if y == 0 or y == a: return 0
    return -(y/a * log2(y/a)) -((a-y)/a * log2((a-y)/a))

def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


def get_data_from_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row)
        return data

def print_matrix(matrix):
    print(f"col:{len(matrix)} row:{len(matrix[0])}")
    for row in matrix:
        for val in row:
            print(val, end="\t")
        print("")
    print("\n")

def choose_attribute(data):
    best_attribute = (None, None, None)
    best_gain_ratio = 0
    for idx in range(0, len(data)-1):
        attribute_dir = count_attribute_values(data[idx], data[-1])
        gain = 1 - entropy_for_attribute(attribute_dir)
        info = intrinsic_info(attribute_dir)
        gain_ratio = gain / info
        if gain_ratio > best_gain_ratio:
            best_gain_ratio = gain_ratio
            best_attribute = (data[idx][0], attribute_dir, gain_ratio)
    return best_attribute

def filrt_data_for_attribute(data, attribute):
    data =  [row for row in data if row[0] != attribute[0] ]
    data = transpose_matrix(data)
    data_set = []
    for key, value in attribute[1].items():
        indices = value[1]
        new_data = [data[i] for i in indices]
        new_data.insert(0, data[0])
        new_data = transpose_matrix(new_data)
        data_set.append(new_data)
    return data_set

def get_dominant_decision(dictionary):
    values = [v[0] for v in dictionary.values()]
    mean = sum(values) / len(values)
    return round(mean)

def subtree(data):
    decisions = data[-1]
    if len(set(decisions[1:])) == 1:
        return decision_to_int(data[-1][-1])
    choosen = choose_attribute(data)
    branches = {}
    for n_data, name in zip(filrt_data_for_attribute(data, choosen),
                            choosen[1].keys()):
        branches[name] = subtree(n_data)
    return [choosen[0], branches]

def map_age_to_label(age):
    if age == 'Age': 
        return age
    age = int(age)
    if 0 <= age <= 20:
        return 'young'
    elif 20 < age <= 40:
        return 'middle'
    elif 40 < age <= 100:
        return 'old'
    else:
        return 'unknown' 

def visualize_tree(tree, graph=None, parent=None, edge_name=None, node_suffix=0):
    if graph is None:
        graph = graphviz.Digraph(format='png')  
    if isinstance(tree, list):
        node_name = tree[0] + f"_{node_suffix}" 
        graph.node(node_name)

        if parent is not None:
            graph.edge(parent, node_name, label=edge_name)
        
        for key, subtree in tree[1].items():
            node_suffix += random.random() * 100 //1
            visualize_tree(subtree, graph=graph, parent=node_name, edge_name=key, node_suffix=node_suffix)
    else:
        leaf_name = f'{tree}_{node_suffix}'  
        graph.node(leaf_name, shape='box')  
        graph.edge(parent, leaf_name, label= edge_name)

    return graph

def decision_to_int(decision):
    # return int(decision.lower() == "yes")
    return int(decision.lower() == "1")

def main():
    # data = get_data_from_file('data.csv')
    data = get_data_from_file('titanic.csv')

    print_matrix(data)
    data = transpose_matrix(data)
    data[4] = [map_age_to_label(age) for age in data[4]]
    data =  [row for row in data if row[0] != "PassengerId"]
    data =  [row for row in data if row[0] != "Name"]
    print_matrix(transpose_matrix(data))
    
    tree = subtree(data)
    print("\nTREE:\n")
    print(tree)

    graph = visualize_tree(tree)
    graph.render('decision_tree', view=True)  # Save and open the generated image

if __name__ == "__main__":
    main()
