class Dictionary:
    reserved_words_Pascal = ["and", "array", "begin", "case", "const",
                             "div", "do", "downto", "else", "end",
                             "file", "for", "function", "goto", "if",
                             "in", "label", "mod", "nil", "not",
                             "of", "or", "packed", "procedure", "program",
                             "record", "repeat", "set", "then", "to",
                             "type", "until", "var", "while", "with"]

    special_symbols = "+ - * / = < > [ ] . , ; ( ) : ^ @ { } $ # & %".split()
    special_double_symbols = ">= := += -= *= /= (* *) (. .) // << >> ** <> >< <=".split()
    type_words = ["integer", "real", "char", "boolean", "string", "enum", "subrange"]

    @staticmethod
    def is_typeword(word):
        return word.lower() in Dictionary.type_words

    @staticmethod
    def is_reserved_word(word):
        return word.lower() in Dictionary.reserved_words_Pascal

    @staticmethod
    def is_symbol(symbol):
        return symbol in Dictionary.special_symbols

    @staticmethod
    def is_double_symbol(symbol):
        return symbol in Dictionary.special_double_symbols


class SyntaxTree:
        tree = list()

        def __init__(self, input):
            variable = str()
            number = str()
            i = 0
            flag = False
            self.tree.append(list())
            for word in input.split():
                if flag:
                    self.tree.append(list())
                    i += 1
                    flag = False

                if Dictionary.is_reserved_word(word):
                    self.tree[i].append(word)
                    continue

                if Dictionary.is_typeword(word):
                    self.tree[i].append(word)
                    continue

                flag = False

                for sym in word:
                    if flag:
                        flag = False
                        continue
                    # ???
                    if sym.isalpha() or sym == "_":
                        if len(number) != 0:
                            number += sym
                        else:
                            variable += sym
                        continue

                    elif sym.isdigit():
                        if len(variable) == 0:
                            number += sym
                        else:
                            variable += sym
                        continue

                    elif sym in Dictionary.special_symbols:
                        if sym == ";":
                            self.stop(variable, number, i)
                            variable = number = str()
                            self.tree[i].append(sym)
                            flag = True
                            continue
                        elif word.index(sym) + 1 < len(word) \
                                and sym + word[word.index(sym) + 1] in Dictionary.special_double_symbols:
                            self.stop(variable, number, i)
                            variable = number = str()
                            self.tree[i].append(sym + word[word.index(sym) + 1])
                            flag = True
                            continue

                        self.stop(variable, number, i)
                        variable = number = str()

                        self.tree[i].append(sym)
                        continue

                self.stop(variable, number, i)
                variable = number = str()

        def stop(self, var, num, i):
            if len(var) != 0:
                self.tree[i].append(var)
            if len(num) != 0:
                self.tree[i].append(num)


class Analyser:
    symbols = set()
    double_symbols = set()
    reserved_words = set()
    type_words = set()
    variables = list()
    numbers = list()
    undefined = set()

    def stop(self, var, num):
        if len(var) != 0:
            self.variables.append(var)
        if len(num) != 0:
            self.numbers.append(num)

    # square braces : begin - index of initial square brace
    def parse_square(self, expr, begin):
        end = close = int()
        open = 1
        for i in range(begin + 1, len(expr)):
            if expr[i] == "[":
                open += 1
            if expr[i] == "]":
                close += 1
                if open == close:
                    end = i
                    break
        if open != close:
            if open > close:
                return self.error(']', " ".join(expr))
            elif open < close:
                return self.error('[', " ".join(expr))
        # ???
        if begin - end == 1:
            return self.error(expr[begin], " ".join(expr))

        for i in range(begin + 1, end):
            lexem = expr[i]
            if lexem in self.variables:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * / [ ] ( )":
                        return self.error(expr[i] + expr[i + 1], " ".join(expr))
                continue

            if lexem in self.numbers:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * /":
                        return self.error(expr[i] + expr[i + 1], " ".join(expr))
                continue

            if lexem in self.symbols:
                if lexem == "[":
                    if not expr[i - 1] in self.variables:
                        return self.error(expr[i - 1], " ".join(expr))
                    else:
                        resp = self.parse_square(expr, i)
                        if not resp:
                            return resp
                    continue
                if lexem == "]":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "[":
                            flag = True
                        if not flag:
                            return self.error("[", " ".join(expr))
                    continue

                if lexem == "(":
                    resp = self.parse_round(expr, i)
                    if resp:
                        return self.error("(", " ".join(expr))
                    continue
                if lexem == ")":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "(":
                            flag = True
                            break
                        if i == 0:
                            return self.error("(", " ".join(expr))
                    continue

                if expr[i - 1] not in self.variables.union(self.numbers):
                    return self.error(expr[i - 1], " ".join(expr))
                if expr[i + 1] not in self.variables.union(self.numbers) \
                        and expr[i + 1] != ")":
                    return self.error(expr[i - 1] + lexem + expr[i + 1], " ".join(expr))
                continue
            else:
                return self.error(lexem, " ".join(expr))

        return False

    def parse_round(self, expr, begin):
        end = close = int()
        open = 1
        for i in range(begin + 1, len(expr)):
            if expr[i] == "(":
                open += 1
            if expr[i] == ")":
                close += 1
                if close == open:
                    end = i
                    break
        if open != close:
            if open > close:
                return self.error(')', " ".join(expr))
            elif open < close:
                return self.error('(', " ".join(expr))

        for i in range(begin + 1, end):
            lexem = expr[i]
            if lexem in self.variables:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * / [ ] ( )":
                        return self.error(lexem, " ".join(expr))
                continue

            if lexem in self.numbers:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * /":
                        return self.error(lexem, " ".join(expr))
                continue

            if lexem in self.symbols:
                if lexem == "[":
                    if not expr[i - 1] in self.variables:
                        return self.error(lexem, " ".join(expr))
                    else:
                        resp = self.parse_square(expr, i)
                        if not resp:
                            return resp
                    continue
                if lexem == "]":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "[":
                            flag = True
                        if not flag:
                            return self.error("[", " ".join(expr))
                    continue

                if lexem == "(":
                    resp = self.parse_round(expr, i)
                    if not resp:
                        return self.error(lexem, " ".join(expr))
                    continue
                if lexem == ")":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "(":
                            flag = True
                        if not flag:
                            return self.error("(", " ".join(expr))
                    continue
                if expr[i - 1] in self.numbers:
                    return self.error(expr[i - 1], " ".join(expr))
                if expr[i + 1] not in self.variables.union(self.numbers) \
                        and expr[i + 1] != ")":
                    return self.error(expr[i + 1], " ".join(expr))
                continue
            else:
                return self.error(lexem, " ".join(expr))

        return False

    def analyse_lex(self, input):
        variable = str()
        number = str()

        for word in input.split():
            if Dictionary.is_reserved_word(word):
                self.reserved_words.add(word)
                continue

            if Dictionary.is_typeword(word):
                self.type_words.add(word)
                continue

            flag = False

            for sym in word:
                if flag:
                    flag = False
                    continue
                # ???
                if sym.isalpha() or sym == "_":
                    if len(number) != 0:
                        number += sym
                    else:
                        variable += sym
                    continue

                elif sym.isdigit():
                    if len(variable) == 0:
                        number += sym
                    else:
                        variable += sym
                    continue

                elif sym in Dictionary.special_symbols:
                    if word.index(sym) + 1 < len(word) \
                            and sym + word[word.index(sym) + 1] in Dictionary.special_double_symbols:
                        self.double_symbols.add(sym + word[word.index(sym) + 1])
                        flag = True

                        self.stop(variable, number)
                        variable = number = str()
                        continue

                    self.stop(variable, number)
                    variable = number = str()
                    self.symbols.add(sym)
                    continue
                else:
                    return "Lexical error at { " + word + " }\n"

            self.stop(variable, number)
            variable = number = str()
        return self.check_undefined()

    def check_undefined(self):
        seq = self.variables
        for test in seq:
            if Dictionary.is_reserved_word(test):
                self.reserved_words.add(test)
                self.variables.remove(test)
            if test[0].isdigit():
                return "Lexical error at { " + test + " }\n"
        self.variables = set(self.variables)
        seq = self.numbers
        for test in seq:
            for i in test:
                if not i.isdigit():
                    return "Lexical error at { " + test + " }\n"
        self.numbers = set(self.numbers)
        return "Success"

    def error(self, lexem, expr):
        return "Syntax error at << {0} >> in  <<{1}>>  \n".format(lexem, expr)

    def analyse_syn(self, input):
        syn_tree = SyntaxTree(input)
        #print(syn_tree.tree)

        for expr in syn_tree.tree:
            for i in range(0, len(expr)):
                lexem = expr[i]

                if Dictionary.is_reserved_word(lexem):
                    if lexem.lower() == "begin":
                        if "end" not in self.reserved_words:
                            return self.error(lexem, " ".join(expr))

                    if lexem.lower() == "end" and lexem in self.reserved_words:
                        if expr[i+1] != ';' and syn_tree.tree.index(expr) != len(syn_tree.tree)-1:
                            return self.error(lexem, " ".join(expr))
                        if "begin" not in self.reserved_words:
                            return self.error(lexem, " ".join(expr))

                    # checking for <for ... to ... do> construction
                    if lexem.lower() == "to":
                        if expr[i+1] not in self.variables.union(self.numbers):
                            return self.error(lexem + " " + expr[i+1], " ".join(expr))
                    count = 0
                    if lexem.lower() == "for" and lexem in self.reserved_words:
                        count += 1
                        if "to" in self.reserved_words:
                            count += 1
                            if "do" in self.reserved_words:
                                count += 1
                    if count == 0:
                        pass
                    elif count == 1:
                        return self.error("to", " ".join(expr))
                    elif count == 2:
                        return self.error("do", " ".join(expr))
                    elif count == 3:
                        pass
                    continue

                if lexem in list(self.variables):
                    if i == 0:
                        if syn_tree.tree.index(expr) == 0:
                            return self.error(expr[i + 1], " ".join(expr))

                        # todo checking for symbols after a variable
                        # if expr[i + 1] not in ":= += -= *= /=".split() or :
                        #    return self.error(expr[i + 1], " ".join(expr))
                    elif i == len(expr) - 1:
                        return self.error(lexem, " ".join(expr))
                    else:
                        if expr[i - 1] not in self.symbols.union(self.double_symbols, self.reserved_words, self.type_words)  \
                                and expr[i + 1] not in self.symbols.union(self.double_symbols, self.reserved_words):
                            return self.error(lexem, " ".join(expr))
                        elif expr[i+1] in self.variables:
                            if expr[i-1] in self.reserved_words:
                                continue
                            else:
                                return self.error(expr[i + 1], " ".join(expr))

                if lexem in list(self.numbers):
                    if i == 0:
                        return self.error(lexem, " ".join(expr))
                    elif i == len(expr) - 1:
                        return self.error(lexem, " ".join(expr))
                    else:
                        if expr[i - 1] not in self.symbols.union(self.double_symbols) \
                                and expr[i + 1] not in self.symbols.union(self.double_symbols):
                            return self.error(lexem, " ".join(expr))

                if lexem in list(self.symbols):
                    # at the beginning
                    if i == 0:
                        return self.error(lexem, " ".join(expr))
                    # in the end
                    elif i == len(expr) - 1:
                        # if "end" is in the end of all input without '.'
                        if syn_tree.tree.index(expr) == len(syn_tree.tree)-1\
                                and expr[i - 1].lower() == "end" and lexem != '.':
                            return self.error(lexem, " ".join(expr))
                        # if 'end' is in the middle without ';'
                        elif syn_tree.tree.index(expr) != len(syn_tree.tree)-1\
                                and expr[i - 1].lower() == "end" and lexem != ';':
                            return self.error(lexem, " ".join(expr))
                        elif expr[i - 1].lower() in self.reserved_words and expr[i-1].lower() != "end":
                            return self.error(lexem, " ".join(expr))
                    # in the middle
                    elif lexem == "[":
                        if expr[i - 1] in self.variables:
                            resp = self.parse_square(expr, i)
                            if resp:
                                return resp
                        else:
                            return self.error(lexem, " ".join(expr))
                    elif lexem == "]":
                        flag = False
                        for j in range(i, 0):
                            # for close brace there is open one
                            if expr[j] == "[":
                                flag = True
                            if not flag:
                                return self.error(lexem, " ".join(expr))
                    elif lexem == "(":
                        if i == 0:
                            return self.error(lexem, " ".join(expr))
                        elif expr[i+1] != "(":
                            self.error("(", " ".join(expr))
                        else:
                            resp = self.parse_round(expr, i)
                            if resp:
                                return resp
                    elif lexem == ")":
                        flag = False
                        for j in range(i, 0):
                            if expr[j] == "(":
                                flag = True
                            if not flag:
                                return self.error(lexem, " ".join(expr))
                    else:
                        if expr[i - 1] not in self.numbers.union(self.variables):
                            if i != len(expr) - 1 and expr[i + 1] not in self.variables.union(self.numbers) or\
                               i != len(expr) - 1 and expr[i + 1] not in self.reserved_words:
                                return self.error(expr[i - 1] + expr[i] + expr[i + 1], " ".join(expr))

                        elif expr[i-1] in self.variables and expr[i+1] in self.symbols.union(self.double_symbols):
                            return self.error(expr[i - 1] + expr[i] + expr[i + 1], " ".join(expr))

                if lexem in list(self.double_symbols):
                    if expr[i-1] not in self.variables and expr[i+1] not in self.variables.union(self.numbers):
                        return self.error(lexem, " ".join(expr))

        return "Success"

if __name__ == "__main__":
    #example = "For i := 1 to do begin begin a := b[n]; end;"
    example = "var n: integer; a, b: real; n:= n - 1; b:=b+a;"
    print(example)
    analyser = Analyser()
    while True:
        resp_lex = analyser.analyse_lex(example)
        if resp_lex == "Success":
            print("Lexical analysis passed")
        else:
            print(resp_lex)
            break

        resp_syn = analyser.analyse_syn(example)
        if resp_syn == "Success":
            print("Syntax analysis passed")
        else:
            print(resp_syn)
        break
