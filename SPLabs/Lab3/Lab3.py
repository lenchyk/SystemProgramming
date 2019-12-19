import re

reserved_words_Pascal = ["and", "array", "begin", "case", "const",
                         "div", "do", "downto", "else", "end",
                         "file", "for", "function", "goto", "if",
                         "in", "label", "mod", "nil", "not",
                         "of", "or", "packed", "procedure", "program",
                         "record", "repeat", "set", "then", "to",
                         "type", "until", "var", "while", "with"]

special_symbols = "+ - * / = < > [ ] . , ; ( ) : ^ @ { } $ # & % << >> ** <> >< <= " \
                  ">= := += -= *= /= (* *) (. .) //".split()


# checking function for cyrillic symbols that we cannot use
def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


# function that find reserved words of Pascal programming language
# that we cannot use for variable names
def find_reserved_words(string):
    return [i for i in string.split() if i in reserved_words_Pascal]


def find_special_symbols(input_code):
    specials = set()
    special_symbols = "+ - * / = < > [ ] . , ; ( ) : ^ @ { } $ # & % << >> ** <> >< <= " \
                      ">= := += -= *= /= (* *) (. .) //".split()
    misunderstood_symbols = "<< >> ** <> >< <= >= := += -= *= /= (* *) (. .) //".split()
    expressions = input_code.split()
    for reserved_word in find_reserved_words(input_code):
        expressions.remove(reserved_word)
    for i in expressions:
        for j in special_symbols:
            if j in i:
                specials.add(j)
    for i in misunderstood_symbols:
        if i in specials:
            for j in i:
                specials.remove(j)
    return specials


def find_variables(correct_split_list):
    return [i for i in correct_split_list if not i.isdigit()]


def find_numbers(correct_split_list):
    return [i for i in correct_split_list if i.isdigit()]


# main function that is used everywhere and splits input string into vars and numbers
def correct_split(string):
    result = set()
    split_string = string.split()
    reserved_words = find_reserved_words(string)
    for i in reserved_words:
        split_string.remove(i)  # there are only expressions after that
    regexPattern = '|'.join(map(re.escape, special_symbols))
    updated_string = []
    for i in split_string:
        updated_string.append(re.split(regexPattern, i))
    for i in updated_string:
        for j in i:
            if j != '':
                result.add(j)
    return result

def correct_split_v2(string):
    result = set()
    split_string = string.split()



def correct_variables(all_variables):
    for i in all_variables:
        if i in reserved_words_Pascal or i[0] in "@!#^&*()-+:;/0123456789_":
            all_variables.remove(i)
    return all_variables

def syntax_check(correct_split_list, variables):
    vars = len(variables)
    difference = correct_split_list - set(variables)
    digits = len(difference)
    for i in difference:
        for j in i:
            if j.isdigit():
                continue
            digits -= 1
    for i in variables:
        for j in i:
            if j.isdigit() or j.isalpha() or j == "_":
                continue
            vars -= 1
    return True if digits == len(difference) and vars == len(variables) else False

def classify(input_code):
    reserved = set(find_reserved_words(input_code))
    specials = set(find_special_symbols(input_code))
    correct_split_list = correct_split(input_code)
    print(correct_split_list)
    all_variables = set(find_variables(correct_split_list))
    numbers = set(find_numbers(correct_split_list))
    variables = set(correct_variables(all_variables))
    all = reserved | specials | numbers | variables
    print(all)
    print("Symbols: ", ", ".join(specials))
    print("Your variables: ", ", ".join(variables))
    print("Numbers you have: ", ", ".join(numbers))
    print("Reserved words: ", ", ".join(reserved))
    #print("Undefined: ", ", ".join(undefined))



if __name__ == '__main__':
    #input_code = input("Write your code, please:\n")
    input_code = "while n<>0 do begin n:=n-1; =  b:=b+a[nend"
    print("Write your code, please:\n", input_code, '\n')
    if has_cyrillic(input_code) != True:
        classify(input_code)
    else:
        print("You have syntax error. Please, try again!")



