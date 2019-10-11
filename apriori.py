import itertools as it
import csv


def merge(lists, n):
    resultslist = []  # Create the empty result list.
    for x in range(len(lists)):
        for y in range(x+1, len(lists)):
            if sorted(lists[x][0:n]) == sorted(lists[y][0:n]):
                resultslist.append(lists[x] + lists[y][-1:])
    return(resultslist)


def to_csv(filename, output_header, nested_list):
    with open(filename, 'w', newline='\n', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Association', output_header])
        wr.writerows(nested_list)


def check_support(combinations, data_list, min_supp):
    # break_counter = prev_count
    supports = []
    met_combs = []
    data_size = len(data_list)
    for comb in combinations:
        match_count = 0
        # Checking each combination in the data list to get respective supports.
        for item in data_list:
            if all(x in item for x in comb):
                match_count += 1

        row = 0
        if match_count > 0:
            # Support calculation based on matches.
            support = round((match_count / data_size) * 100, 2)

            # Check to append to supports list only if minumum support requirement is met and if row does not already exist.
            row = [list(comb), support]
            if support > min_supp:
                supports.append(row)
                met_combs.append(comb)
                # prev_count += 1

    return supports, met_combs


def apriori(filename, min_supp, min_conf):
    # Open data file and convert to list.
    with open(filename, "rt", encoding='utf8') as f:
        reader = csv.reader(f)
        data_list = list(reader)

    # Use dictionary to identify unique data for permutation calculation.
    data = []
    max_length = 0
    for line in data_list:
        if len(line[1:]) > max_length:
            max_length = len(line[1:])
        for item in line[1:]:
            data.append(item)
    unique_data = list(dict.fromkeys(data))

    supports = []
    met_combs = []
    combs = []
    updated_combs = []
    i = 1
    prev_count = 0
    confidences = []

    while True:
        print(f' --------- Generating association rules for sets of {i} ---------') if i > 1 else print(
            f' --------- Generating association rules for initial set ---------')

        # Setting parameter to check for additional itemsets that meet minimum support requirements.
        print('Checking associations with dataset and calculatind supports...')
        supports, met_combs = check_support(unique_data, data_list, min_supp)

        combs.extend(list(map(list, (it.combinations(met_combs, 2)))))
        supports.extend(check_support(combs, data_list, min_supp)[0])
        met_combs.extend(check_support(combs, data_list, min_supp)[1])

        updated_combs = merge(met_combs[(len(unique_data) - 1):], 1)
        supports.extend(check_support(updated_combs, data_list, min_supp)[0])
        met_combs.extend(check_support(updated_combs, data_list, min_supp)[1])

        # Writing supports to csv
        to_csv('supports.csv', 'Supports(%)', supports)

        print('Calculating confidences...')
        # Loop through unique itemsets to calculate confidence.
        confidence = 0
        for comb in met_combs:
            den = 0
            num = 0
            size = len(comb)
            # Check to make sure itemsets have more than one item in order to isolate associations itemsets.
            if size > 1:
                pass
                # Iterating based on itemset size in order to calculate respective supports for subset associations.
                for pos in range(size - 1, 0, -1):
                    # Gathering left item(s) and right item(s) of each respective association
                    left = [i for i in supports if i[0] == comb[:-pos]][0][0]
                    right = [i for i in supports if i[0] == comb[-pos:]][0][0]
                    print('Comb', comb)
                    print('Comb Left: ', left)
                    print('Comb Right: ', right)
                    # Gathering the support percentages for the numerator and denominator based on the confidence formula.
                    den = [i for i in supports if i[0] == comb[:-pos]][0][1]
                    num = [i for i in supports if i[0] == comb][0][1]

                    print('Den: ', den)
                    print('Num: ', num)
                    # Confidence calculation.
                    confidence = round((num / den) * 100, 2)
                    if confidence > min_conf:
                        confidences.append(
                            [f'{left} -> {right}', confidence])

        print('Removing redundant confidences...')
        upd_confidences = set(tuple(x) for x in confidences)
        b = [list(x) for x in upd_confidences]

        # Writing confidences to csv
        to_csv('confidences.csv', 'Confidences(%)', upd_confidences)

        # i += 1
        break


# User inputs.
# filename = input(
#     "Enter the name of the transaction file. Include the file extension. (eg. \".txt\") : ")
# min_supp = int(input("Enter the minimum support value (0 - 100%): "))
# min_conf = int(input("Enter the minimum confidence value (0 - 100%): "))

# Running apriori function
# apriori(filename, min_supp, min_conf)
apriori('test.txt', 30, 10)

print('Process completed.')
