from math import log2
import csv
import graphviz
import random

print("Welcome to Decision Tree Generatro")

# zwraca słownik ktory ma strukture 
# {
#     ...
#     <nazwa_wartości_atrybutu>: [ 
#         <ilość_decyzji_yes>,
#         <lista_indeksów_z_tym_parameterem>
#     ]
#     ...
# }
def count_atribure_values(atribute, decision):
    atribute_dir = {}
    for idx in range(1, len(atribute)):
        if atribute[idx] not in atribute_dir:
            atribute_dir[atribute[idx]] = [
                    decision_to_int(decision[idx]),
                    [idx]
            ]
        else:
            atribute_dir[atribute[idx]][0] += decision_to_int(decision[idx])
            atribute_dir[atribute[idx]][1] += [idx]
    # print(atribute_dir)
    return atribute_dir

def intrinsic_info(atribute_dir):
    values = list(atribute_dir.values())
    res = 0
    all_vals_count = sum(len(sublist[1]) for sublist in values)
    # print(all_vals_count)
    for val in values:
        a = len(val[1])/all_vals_count
        # print(a)
        res -= a * log2(a)
        # print(a * log2(a))
    return res


def entropy_for_atribute(atribute_dir):
    values = atribute_dir.values()
    # print(values)
    all_vals_count = sum(len(sublist[1]) for sublist in values)
    
    entropy_for_atribute = 0
    for val in values:
        # print()
        # print(len(val[1]), all_vals_count)
        # print(entropy(val[0], len(val[1])))
        entropy_for_atribute += (len(val[1])/all_vals_count) * entropy(val[0], len(val[1]))
    # print(entropy_for_atribute)
    return entropy_for_atribute

# y to jest ilość yes'ow 
# a to ilość wszystkich pojawień się tej wartości 
def entropy(y, a):
    # print(y, a, (a-y))
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
        # print(row)
        for val in row:
            print(val, end="\t")
        print("")
    print("\n")

def choose_atribute(data):
    best_atribute = (None, None, None)
    bast_gain_ratio = 0
    for idx in range(0, len(data)-1):
        # print(data[idx][0])
        atribute_dir = count_atribure_values(data[idx], data[-1])
        gain = 1 - entropy_for_atribute(atribute_dir)
        # print(f"Gain for {data[idx][0]} {gain}")
        info = intrinsic_info(atribute_dir)
        # print(f"Intrinsic_info for {data[idx][0]} {info}")
        # print(atribute_dir)
        gain_ratio = gain / info
        # print(f"gain ratio {gain_ratio}")
        # print()
        if gain_ratio > bast_gain_ratio:
            bast_gain_ratio = gain_ratio
            best_atribute = (data[idx][0], atribute_dir, gain_ratio)
    # print(f"best atriburte {best_atribute[0]}\n{best_atribute[1]}")
    return best_atribute

def filrt_data_for_atribute(data, atribute):
    data =  [row for row in data if row[0] != atribute[0] ]
    data = transpose_matrix(data)
    # print_matrix(data)
    # print(atribute)
    data_set = []
    for key, value in atribute[1].items():
        indices = value[1]
        new_data = [data[i] for i in indices]
        new_data.insert(0, data[0])
        new_data = transpose_matrix(new_data)
        data_set.append(new_data)
    return data_set

def get_dominant_decision(dictionary):
    values = [v[0] for v in dictionary.values()]
    mean = sum(values) / len(values)
    # print(values)
    # print(dictionary)
    return round(mean)

def subtree(data):
    # print("\nsubtree ")
    # print_matrix(transpose_matrix(data))
    decisions = data[-1]
    # print(decisions)
    if len(set(decisions[1:])) == 1:
        return decision_to_int(data[-1][-1])
    choosen = choose_atribute(data)
    branches = {}
    # print(f"choosen {choosen[0]}")
    for n_data, name in zip(filrt_data_for_atribute(data, choosen),
                            choosen[1].keys()):
        # print("name of branch",name)
        # print(n_data)
        branches[name] = subtree(n_data)
        # print("branches", branches)
    return [choosen[0], branches]

# def print_subtree(tree):

def decision_to_int(decision):
    # return int(decision.lower() == "yes")
    return int(decision.lower() == "1")

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
        graph = graphviz.Digraph(format='png')  # Initialize graph if not provided

    # First element in the list is always the attribute (node) name
    if isinstance(tree, list):
        node_name = tree[0] + f"_{node_suffix}" # Attribute name (e.g., 'Sex', 'Parch', etc.)
        # Create the node for the current attribute
        graph.node(node_name)
        
        # If there's a parent node, add an edge from the parent to the current node
        if parent is not None:
            graph.edge(parent, node_name, label=edge_name)
        
        # The second element in the list is a dictionary containing branches
        for key, subtree in tree[1].items():
            # Recursively call the function to visualize each subtree
            node_suffix += random.random() * 100 //1
            visualize_tree(subtree, graph=graph, parent=node_name, edge_name=key, node_suffix=node_suffix)
    else:
        # Leaf nodes: When a final decision (e.g., 0 or 1) is reached
        leaf_name = f'{tree}_{node_suffix}'  # Convert leaf node (e.g., 0 or 1) to string for graphviz
        graph.node(leaf_name, shape='box')  # Display leaf nodes as boxes
        graph.edge(parent, leaf_name, label= edge_name)  # Connect leaf to its parent decision node

    print(tree)
    return graph

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
    print("\n\nTREE:")
    print(tree)

    graph = visualize_tree(tree)
    graph.render('decision_tree', view=True)  # Save and open the generated image

if __name__ == "__main__":
    main()


