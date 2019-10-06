import itertools as it
import csv


# def apriori(filename, min_supp, min_conf):
def apriori(filename):
    with open(filename, "rt", encoding='utf8') as f:
        reader = csv.reader(f)
        data_list = list(reader)

    data = []
    for line in data_list:
        for item in line:
            data.append(item)
    unique_data = list(dict.fromkeys(data))

    supports = {}
    count = 0
    data_size = len(data_list)
    for item in unique_data:
        count = sum(x.count(item) for x in data_list)
        support = round((count / data_size) * 100, 2)
        supports.update({item: support})
    print(supports)

    # print(list(it.combinations(unique_data, 7)))


filename = input("Enter the name of the transaction file: ")
# min_supp = int(input("Enter the minimum support value (0 - 100%): "))
# min_conf = int(input("Enter the minimum confidence value (0 - 100%): "))
# apriori(filename, min_supp, min_conf)
apriori(filename)
