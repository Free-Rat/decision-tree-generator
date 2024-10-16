from math import log2
print("Welcome to Decision Tree Generatro")

# zwraca słownik ktory ma strukture 
# {
#     <nazwa_wartości_atrybutu>: [ 
#         <ilość_decyzji_yes>,
#         <lista_indeksów_z_tym_parameterem>
#     ]
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

def intrinsic_info(values):
    print(values[0])
    res = 0
    all_vals_count = sum(len(sublist[1]) for sublist in values)
    print(all_vals_count)
    for i in values[1]:
        res += i/all_vals_count
    print(res)

    return 
    # for val in values:
    #     up = 


def entropy_for_atribute(values):
    print(values)
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
    # print(y, a)
    if y == 0: return 0
    return -(y/a * log2(y/a)) -((a-y)/a * log2((a-y)/a))

def decision_to_int(decision):
    return int(decision.lower() == "yes")


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

def main():
    data = get_data_from_file('data.csv')
    print_matrix(data)
    data = transpose_matrix(data)
    # print_matrix(data)

    for idx in range(0, len(data)-1):
        print(data[idx][0])
        atribute_dir = count_atribure_values(data[idx], data[-1])
        # print("entropia " ,entropy_for_atribute(atribute_dir))
        gain = 1 - entropy_for_atribute(atribute_dir.values())
        print(f"Gain for {data[idx][0]} {gain}")
        # print(intrinsic_info(atribute_dir.values()))

if __name__ == "__main__":
    main()


