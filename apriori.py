import itertools as it
import csv
import os.path

# Remove duplicates from supports list


# def remove_duplicates(nested_list):
#     seen_it = set()
#     upd_list = []
#     for line in nested_list:
#         key = frozenset(line[0])
#         if key not in seen_it:
#             seen_it.add(key)
#             upd_list.append(line)
#     return upd_list

# Pruning and merging based on similarities between same order itemsets


def merge(keys, n):
    resultslist = []
    lists = list(keys)
    for x in range(len(lists)):
        for y in range(x+1, len(lists)):
            if isinstance(lists[y], str) == False and sorted(lists[x][0:n]) == sorted(lists[y][0:n]) and sorted(lists[x]) != sorted(lists[y]):
                resultslist.append(lists[x] + lists[y][-1:])
    return(resultslist)

# create csv from data list


def to_csv(filename, output_header, nested_list):
    with open(filename, 'w', newline='\n', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Association', output_header])
        wr.writerows(nested_list)

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

            # Check to append to supports list only if minumum support requirement is met and if row does not already exist
            # if isinstance(comb, str):
            #     row = {str(comb): support}
            # else:
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

        # Runnin merge function as part of the pruning process to create higher order itemsets
        # print(merge(supports.keys(), c - 2))
        
        lists = list(supports.keys())
        n = c-2
        for x in range(len(lists)):
            for y in range(x+1, len(lists)):
                if isinstance(lists[y], str) == False and sorted(lists[x][0:n]) == sorted(lists[y][0:n]) and sorted(lists[x]) != sorted(lists[y]):
                    row = lists[x] + lists[y][-1:]
                    updated_combs.update({row: None})
        
        # updated_combs = merge(supports.keys(), c - 2)

        # Re-calculating supports for higher order itemsets
        # Checking to make sure new supports are created for each iteration
        supports.update(check_support(updated_combs, data_list, min_supp)[0])
        prev_count = check_support(updated_combs, data_list, min_supp)[1]

        # upd_supports = remove_duplicates(supports)

        # Writing supports to csv
        # to_csv(f'supports-{filename}.csv', 'Supports(%)', supports)

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

        # # Removing redundant confidence permutations
        # upd_confidences = set(tuple(x) for x in confidences)
        # b = [list(x) for x in upd_confidences]

        # Writing confidences to csv
        # to_csv(f'confidences-{filename}.csv',
        #        'Confidence (%)', upd_confidences)
        print(supports)
        print(confidences)

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
    apriori(f'data{x + 1}.txt', 75, 95)


print('Process completed.')
