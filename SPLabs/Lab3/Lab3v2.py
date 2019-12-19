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

example = "while 1n<>0 do begin n:=n-1; =  b:=b+a[nend"
print(example)

# checking function for cyrillic symbols that we cannot use
def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


def lexem(input):
    return [t.strip() for t in re.findall(r'\b.*?\S.*?(?:\b|$)', input)]


def symbols(lexems):
    return [i for i in lexems if i in special_symbols]


def check_var(lexem):
    if lexem[0] in "@!#^&*()-+:;/0123456789_" or lexem in reserved_words_Pascal \
            or lexem in special_symbols:
        return False
    return True


def variable(lexems):
    return [i for i in lexems if check_var(i)]


def numbers(lexems):
    return [i for i in lexems if i.isdigit()]



def reserved_words(lexems):
    return [i for i in lexems if i in reserved_words_Pascal]


def undefined(lexems):
    return 0


print(lexem(example))
