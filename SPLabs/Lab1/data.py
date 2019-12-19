
def compare(a, b):
    return True if a == b else False


def find_substring(a, b):
    a1 = [i for i in a.lower()]
    b1 = [i for i in b.lower()]
    count = 0
    for i in a1:
        for j in b1:
            print(i, j)
            if i == j:
                count = find_substring(a1[a1.index(i)+1], b1[b1.index(j)+1])
                a1.remove(j)
                count += 1
                print("!!!Word after removal - ", a1)
                break

            else:
                continue
    return count

key = "Vaziant"
word = "InItiAl"
print(find_substring(key, word))
