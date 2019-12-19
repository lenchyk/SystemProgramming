# Lab №1
# Written by Lena Soroka


data = ["fEnix", "COren", "FloOr", "Core", "SOrE", "sERial", "InItiAl", "DaY", "Is", "GoOd"]


# main function
def find_occurrences(key, data):
    occurrunce = {}
    for word in data:
        occurrunce[word] = find_substring(key, word)
    return occurrunce


# find similar symbols
#todo correct algorithm
def find_substring(a, b):
    a1 = [i for i in a.lower()]
    b1 = [i for i in b.lower()]
    count = 0
    for i in a1:
        for j in b1:
            if i == j:
                b1.remove(j)
                count += 1
                break
            else:
                continue
    return count


# maximum amount of occurrences
def max_value(dictionary):
    dict_items = list(dictionary.items())
    values = [i[1] for i in dict_items]
    maximum = max(values)
    items = []
    for i in dict_items:
        if i[1] == maximum:
            items.append(i)
    return items


while True:
    key = input("Enter key, please. ")

    database = find_occurrences(key, data)

    print("General database:\n", database)
    print("Maximum to occur: ")

    max_of_database = max_value(database)

    # черговий!
    if len(max_of_database) > 1:
        for i in max_of_database:
            print(i)
            if input("Do you want more of such occurrences?(y/n)") != 'y':
                break
    #todo if no occurrences (everything is 0) --> correct output
    elif len(max_of_database) == 1:
        print(max_of_database[0])
        #print("No occurrences!")
    else:
        print("No occurrences!")

    if input("Continue to search?..(y/n)") != 'y':
        break

