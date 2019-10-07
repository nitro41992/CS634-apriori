import itertools as it
import csv


# def apriori(filename, min_supp, min_conf):
def apriori(filename, min_supp):
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
        item_count = sum(x.count(item) for x in data_list)
        support = round((item_count / data_size) * 100, 2)
        if support > min_supp:
            supports.update({item: support})

    combs = list(set(it.combinations(unique_data, 2)))

    for comb in combs:
        match_count = 0
        for item in data_list:
            if set(comb).issubset(item):
                match_count += 1
        if match_count > 0:
            support = round((match_count / data_size) * 100, 2)
            if support > min_supp:
                supports.update({comb: support})
    print(supports)


    # filename = input("Enter the name of the transaction file: ")
    # min_supp = int(input("Enter the minimum support value (0 - 100%): "))
    # min_conf = int(input("Enter the minimum confidence value (0 - 100%): "))
    # apriori(filename, min_supp, min_conf)
apriori('data1', 10)
