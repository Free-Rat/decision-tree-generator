from math import log2
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

def decision_to_int(decision):
    return int(decision.lower() == "yes")
    # return int(decision.lower() == "1")


def transpose_matrix(matrix):
    return [list(row) for row in zip(*matrix)]


def get_data_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        rows = content.split("\n")
        data = []
        for idx in range(len(rows)-1):
            row = rows[idx].split(",")
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
    data_set = []
    for i in range(0, len(atribute[1])):
        new_data = [data[i] for i in list(atribute[1].values())[i][1]]
        new_data.insert(0, data[0])
        # print_matrix(new_data)
        new_data = transpose_matrix(new_data)
        data_set.append(new_data)
    return data_set

def get_dominant_decision(dictionary):
    values = [v[0] for v in dictionary.values()]
    mean = sum(values) / len(values)
    # print(values)
    # print(dictionary)
    return round(mean)

def is_only_one_left(dictionary):
    return len(dictionary.values()) == 1


def subtree(data):
    # print("\nsubtree ")
    # print_matrix(transpose_matrix(data))
    # print(data)
    if len(data[-1]) == 2:
        return decision_to_int(data[-1][-1])
    choosen = choose_atribute(data)
    if choosen[2] >= 1.0:
        return get_dominant_decision(choosen[1]) 
        
    branches = {}
    for n_data, name in zip(filrt_data_for_atribute(data, choosen),
                            choosen[1].keys()):
        # print("name of branch",name)
        # print(n_data)
        branches[name] = subtree(n_data)
        # print("branches", branches)
        # print()
    return [choosen[0], branches]

def main():
    data = get_data_from_file('data.csv')
    print_matrix(data)
    data = transpose_matrix(data)
    tree = subtree(data)
    print("\n\nTREE:")
    print(tree)
    
    
    exit()
    best_a = choose_atribute(data)
    new_data = filrt_data_for_atribute(data, best_a)
    sec_best = choose_atribute(new_data)
    new_data = filrt_data_for_atribute(new_data, sec_best)
    third_best = choose_atribute(new_data)


if __name__ == "__main__":
    main()


