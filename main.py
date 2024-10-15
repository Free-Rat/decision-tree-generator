print("Welcome to Decision Tree Generatro")

def get_data_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        print(content)
        rows = content.split("\n")
        print(rows)
        data = []
        for idx in range(len(rows)):
            row = rows[idx].split(",")
            data.append(row)
        return data

data = get_data_from_file('data.csv')
for row in data:
    print("")
    for val in row:
        print(val, end="\t")

    

