import random

a = ['Milk', 'Wine', 'Chips', 'Diaper', 'Cereal',
     'Eggs', 'Juice', 'Napkins', 'Ice cream', 'Grapes']

for x in range(0, 20):
    random.shuffle(a)
    print(
        str(",".join([str(x + 1)] + [x for x in a if random.randint(0, 5) != 0])))
