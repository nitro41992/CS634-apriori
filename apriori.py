import itertools as it
import csv


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
    data_size = len(data_list)
    combs = []
    updated_combs = []
    i = 1
    prev_count = 0
    confidences = []

    print(unique_data)

    while i <= max_length:
        print(f' --------- Generating association rules for sets of {i} ---------') if i > 1 else print(
            f' --------- Generating association rules for initial set ---------')
        # Calculate all permutations of unique items.
        combs.extend(map(list, (it.product(unique_data, repeat=i))))
        print('combinations found....')

        # Setting parameter to check for additional itemsets that meet minimum support requirements.
        print('Checking associations with dataset and calculatind supports...')
        break_counter = prev_count
        for comb in combs:
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
                row = [comb, support]
                if support > min_supp:
                    supports.append(row)
                    prev_count += 1

        # Break of while loop if no additional itemsets meeting the minimum requirements are found.
        if prev_count - break_counter == 0:
            print(
                f'No associations found for sets of {i} that meet the minimum requriements...')
            break

        print('Removing redundant supports...')
        # Removal of redundant support itemsets.
        seen_it = set()
        upd_sups = []
        for line in supports:
            key = frozenset(line[0])
            if key not in seen_it:
                seen_it.add(key)
                upd_sups.append(line)

        # Isolation of unique itemsets for confidence calculation
        updated_combs = [item[0] for item in upd_sups]

        print('Calculating confidences...')
        # Loop through unique itemsets to calculate confidence.
        confidence = 0
        for comb in updated_combs:
            den = 0
            num = 0
            size = len(comb)
            # Check to make sure itemsets have more than one item in order to isolate associations itemsets.
            if size > 1:
                # Iterating based on itemset size in order to calculate respective supports for subset associations.
                for pos in range(size - 1, 0, -1):
                    # Gathering left item(s) and right item(s) of each respective association
                    left = [i for i in upd_sups if i[0] == comb[:-pos]][0][0]
                    right = [i for i in upd_sups if i[0] == comb[-pos:]][0][0]

                    # Gathering the support percentages for the numerator and denominator based on the confidence formula.
                    den = [i for i in upd_sups if i[0] == comb[:-pos]][0][1]
                    num = [i for i in upd_sups if i[0] == comb][0][1]

                    # Confidence calculation.
                    confidence = round((num / den) * 100, 2)
                    if confidence > min_conf:
                        confidences.append(
                            [f'{{{", ".join(left)}}} -> {{{", ".join(right)}}}', confidence])

        # Writing supports and confidences to csv
        print('Generating confidences.csv and supports.csv...')
        with open('supports.csv', 'w', newline='\n', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(['Association', 'Support(%)'])
            wr.writerows(upd_sups)

        with open('confidences.csv', 'w', newline='\n', encoding='utf-8') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(['Association', 'Confidence(%)'])
            wr.writerows(confidences)

        i += 1


# User inputs.
filename = input(
    "Enter the name of the transaction file. Include the file extension. (eg. \".txt\") : ")
min_supp = int(input("Enter the minimum support value (0 - 100%): "))
min_conf = int(input("Enter the minimum confidence value (0 - 100%): "))

# Running apriori function
apriori(filename, min_supp, min_conf)

print('Process completed.')
