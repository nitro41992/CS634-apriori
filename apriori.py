import itertools as it
import csv


# create csv from data list


def to_csv(filename, dictionary, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = [dict(zip(fieldnames, [k, v])) for k, v in dictionary.items()]
        writer.writerows(data)

# Calculate support for all combinations in datalist anc check minimum support requirements


def check_support(combinations, data_list, min_supp):
    new_count = 0
    supports = {}
    data_size = len(data_list)
    for comb in combinations:
        match_count = 0
        # Checking each combination in the data list to get respective supports
        for item in data_list:

            if comb in item or set(comb).issubset(item):
                match_count += 1

        row = 0
        if match_count > 0:
            # Support calculation based on matches.
            support = round((match_count / data_size) * 100, 2)

            row = {comb: support}
            if support > min_supp:
                supports.update(row)
                new_count += 1

    return supports, new_count


def apriori(filename, min_supp, min_conf):
    # Open data file and convert to list.
    with open(filename, "rt", encoding='utf8') as f:
        reader = csv.reader(f)
        temp = list(reader)

    data_list = []
    for row in temp:
        data_list.append(row[1:])

    # Use dictionary to identify unique data for permutation calculation
    data = []
    max_length = 0
    for line in data_list:
        if len(line[1:]) > max_length:
            max_length = len(line[1:])
        for item in line:
            data.append(item)
    unique_data = list(dict.fromkeys(data))
    # print(unique_data)

    supports = {}
    met_combs = []
    combs = []
    prev_count = 0
    updated_combs = {}
    c = 3
    confidences = {}

    # Creating data list for itemsets with support values as well as a data list for isolating itemsets for confidence calculations
    print('Checking associations with dataset and calculating supports for 1st and 2nd itemsets...')
    supports, prev_count = check_support(unique_data, data_list, min_supp)

    # Creating second order itemsets
    combs.extend((it.combinations(supports.keys(), 2)))
    # print(combs)

    # Re-calculating supports for 2nd order itemsets
    supports.update(check_support(combs, data_list, min_supp)[0])

    while True:
        break_count = prev_count
        print(f'Generating association rules for itemsets of {c}...')

        # Pruning data based on commonalities of attributes
        lists = list(supports.keys())
        n = c-2
        for x in range(len(lists)):
            for y in range(x+1, len(lists)):
                if isinstance(lists[y], str) == False and sorted(lists[x][0:n]) == sorted(lists[y][0:n]) and sorted(lists[x]) != sorted(lists[y]):
                    row = lists[x] + lists[y][-1:]
                    updated_combs.update({row: None})

        # Re-calculating supports for higher order itemsets
        # Checking to make sure new supports are created for each iteration
        supports.update(check_support(updated_combs, data_list, min_supp)[0])
        prev_count = check_support(updated_combs, data_list, min_supp)[1]

        # Writing supports to csv
        to_csv(f'supports-{filename}.csv', supports,
               fieldnames=['Itemset', 'Support(%)'])

        print(f'Calculating confidences for itemsets of {c}...')
        # Loop through unique itemsets to calculate confidence
        confidence = 0
        perms = []
        for comb in supports.keys():
            den = 0
            num = 0

            if isinstance(comb, str):
                size = 1
            else:
                size = len(comb)
            # Check to make sure itemsets have more than one item in order to isolate associations itemsets
            if size > 1 and isinstance(comb, str) == False and size <= max_length:
                # Creating permutations based off of itemsets in order to create all association combinations
                perms = list(it.permutations(comb, len(comb)))
                # print(perms)

                for i in range(len(perms)):
                    for j in range(1, len(perms[i])):
                        # Isolating the left and right of each association and calculating the confidence

                        # print(keys)
                        for itemset, support in supports.items():
                            if sorted(itemset) == sorted(perms[i][j:]) or itemset == perms[i][j:][0]:
                                den = support
                            if sorted(itemset) == sorted(perms[i]):
                                num = support

                        # Making sure confidence meets the minimum requirements
                        confidence = round(((num/den) * 100), 2)
                        if confidence > min_conf:
                            confidences.update(
                                {f'{perms[i][:j]} -> {perms[i][j:]}': confidence})

        # Writing confidences to csv
        to_csv(f'confidences-{filename}.csv', confidences,
               fieldnames=['Association', 'Confidence(%)'])

        if prev_count - break_count == 0 or c == max_length:
            break

        c += 1


# # User inputs
# while True:
#     try:
#         filename = input(
#             'Enter the name of the transaction file. Include the file extension. (eg. \'.txt\') : ')
#         if(os.path.exists(filename) == False):
#             print('The file you selected does not exist, please try again')
#             continue
#         min_supp = int(input('Enter the minimum support value (0 - 100%): '))
#         min_conf = int(
#             input('Enter the minimum confidence value (0 - 100%): '))
#     except ValueError:
#         print('\n')
#         print('Please make sure the minimum support and minimum confidence values are integers between 0 and 100.')
#         print('\n')
#         continue
#     else:
#         break


# Running apriori function
for x in range(1):
    apriori(f'data{x + 1}.txt', 10, 10)


print('Process completed.')
