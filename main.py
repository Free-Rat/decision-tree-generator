print("Welcome to Decision Tree Generatro")

def entropy(parameter, decision):
    print(f"calcualting entropy for {parameter[0]}")

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
    entropy(data[0], data[-1])

if __name__ == "__main__":
    main()


