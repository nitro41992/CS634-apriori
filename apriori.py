import itertools as it
import csv


def apriori(filename, min_supp, min_conf):
    with open(filename, "rt", encoding='utf8') as f:
        reader = csv.reader(f)
        data_list = list(reader)

    data = []
    for line in data_list:
        for item in line:
            data.append(item)
    unique_data = list(dict.fromkeys(data))

    supports = []
    data_size = len(data_list)
    combs = []
    updated_combs = []
    i = 1
    prev_count = 0
    confidences = []
    
    while True:
        combs.extend(map(list, (it.permutations(unique_data, i))))
        
        print('Calculating supports...')
        break_counter = prev_count
        for comb in combs:
            match_count = 0
            for item in data_list:
                if set(comb).issubset(item):
                    match_count += 1
            row = 0
            if match_count > 0:
                support = round((match_count / data_size) * 100, 2)
                row = [comb, support]
                check = any(row == sl for sl in supports)
                if support > min_supp and check == False:
                    supports.append(row)
                    prev_count += 1

        if prev_count - break_counter == 0:
            break

        
        updated_combs = [item[0] for item in supports]

        print('Calculating confidences...')
        confidence = 0
        for comb in updated_combs:
            den = 0
            num = 0
            if len(comb) > 1:
                den = [i for i in supports if i[0] == comb[:-1]][0][1]
                num = [i for i in supports if i[0] == comb][0][1]
                confidence = round((num / den) * 100, 2)
                if confidence > min_conf:
                    confidences.append([comb, confidence])

        i += 1

    print('Generating confidences.csv and supports.csv...')
    with open('supports.csv', 'w', newline='\n', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Association','Support(%)'])
        wr.writerows(supports)

    with open('confidences.csv', 'w', newline='\n', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['Association','Confidence(%)'])
        wr.writerows(confidences)


filename = input("Enter the name of the transaction file. Include the file extension. (eg. \".txt\") : ")
min_supp = int(input("Enter the minimum support value (0 - 100%): "))
min_conf = int(input("Enter the minimum confidence value (0 - 100%): "))
apriori(filename, min_supp, min_conf)
print('Process completed.')

