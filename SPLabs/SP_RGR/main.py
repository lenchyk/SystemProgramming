import os
from token import Token

def path_putter(func):
    def wrapper():
        try:
            result = func('expression1.txt')
        except FileNotFoundError:
            try:
                result = func('/Users/lenasoroka/PycharmProjects/SP_RGR')
            except FileNotFoundError:
                print("File does not exist!")
                import sys
                sys.exit(1)

        return result

    return wrapper


@path_putter
def reader(path):
    file = open(path, 'r')
    result = file.read().lower()
    file.close()

    return result


expression = reader()
print(expression)
print()

result = Token().analyzeCode(expression)
#result1 = Token().classify(result)
#for i in result1:
#    print(i)


result = Token().combine_commands(result, [])

#for i in result:
    #print(i)
    #print(' '.join(i))


if result[-1] == ['end.']:
    result = result[:-1]
    ident = 0
    for i in range(len(result)):
        try:
            err, num = Token().preview_command(result[i], i)
            print(err.format(' '.join(result[num])).replace('begin', ''))
            break
        except:
            ident += 1

    #if ident == len(result):
    #    print('Success!')

    #with open('code.py', 'r') as file:
    #    print(file.read())
    try:
        import code
        print('Main program:   b =', code.b)
        os.remove('/Users/lenasoroka/PycharmProjects/SP_RGR/code.py')
    except:
        pass

    try:
        os.remove('/Users/lenasoroka/PycharmProjects/SP_RGR/vars.txt')
        os.remove('/Users/lenasoroka/PycharmProjects/SP_RGR/vals.txt')
    except FileNotFoundError:
        pass

else:
    print('Error!\nend. in the end expected')
