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

    @staticmethod
    def is_reserved_word(word):
        return word in Dictionary.reserved_words_Pascal

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
                    self.tree.append(word)
                    continue

                flag = False

                for sym in word:
                    if flag:
                        flag = False
                        continue

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
                            self.stop(variable, number,i)
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
    variables = list()
    numbers = list()
    undefined = set()

    def stop(self, var, num):
        if len(var) != 0:
            self.variables.append(var)
        if len(num) != 0:
            self.numbers.append(num)

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
            return self.error(expr)

        if begin - end == 1:
            return self.error(expr)

        for i in range(begin + 1, end):
            lexem = expr[i]
            if lexem in self.variables:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * / [ ] ( )":
                        return self.error(expr)
                continue

            if lexem in self.numbers:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * /":
                        return self.error(expr)
                continue

            if lexem in self.symbols:
                if lexem == "[":
                    if not expr[i - 1] in self.variables:
                        return self.error(expr)
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
                            return self.error(expr)
                    continue

                if lexem == "(":
                    resp = self.parse_round(expr, i)
                    if resp:
                        return self.error(expr)
                    continue
                if lexem == ")":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "(":
                            flag = True
                            break
                        if i == 0:
                            return self.error(expr)
                    continue

                if expr[i - 1] not in self.variables.union(self.numbers):
                    return self.error(expr)
                if expr[i + 1] not in self.variables.union(self.numbers) \
                        and expr[i + 1] != ")":
                    return self.error(expr)
                continue
            else:
                return self.error(expr)

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
        if open - close != 0:
            return self.error(expr)

        if close != open:
            return self.error(expr)

        for i in range(begin + 1, end):
            lexem = expr[i]
            if lexem in self.variables:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * / [ ] ( )":
                        return self.error(expr)
                continue

            if lexem in self.numbers:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * /":
                        return self.error(expr)
                continue

            if lexem in self.symbols:
                if lexem == "[":
                    if not expr[i - 1] in self.variables:
                        return self.error(expr)
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
                            return self.error(expr)
                    continue

                if lexem == "(":
                    resp = self.parse_round(expr, i)
                    if not resp:
                        return self.error(expr)
                    continue
                if lexem == ")":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "(":
                            flag = True
                        if not flag:
                            return self.error(expr)
                    continue
                if expr[i - 1] in self.numbers:
                    return self.error(expr)
                if expr[i + 1] not in self.variables.union(self.numbers) \
                        and expr[i + 1] != ")":
                    return self.error(expr)
                continue
            else:
                return self.error(expr)

        return False

    def analyse_lex(self, input):
        variable = str()
        number = str()

        for word in input.split():
            if word in Dictionary.reserved_words_Pascal:
                self.reserved_words.add(word)
                continue

            flag = False

            for sym in word:
                if flag:
                    flag = False
                    continue

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
            if test in Dictionary.reserved_words_Pascal:
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

    def error(self, expr):
        return "Syntax error in { " + " ".join(expr) + " }\n"

    def analyse_syn(self, input):
        syn_tree = SyntaxTree(input)

        for expr in syn_tree.tree:
            for i in range(0, len(expr)):
                lexem = expr[i]
                if Dictionary.is_reserved_word(lexem):
                    continue
                if lexem in list(self.variables):
                    if i == 0:
                        if expr[i + 1] not in ":= += -= *= /=".split():
                            return self.error(expr)
                    elif i == len(expr) - 1:
                        return self.error(expr)
                    else:
                        if expr[i - 1] not in self.symbols.union(self.double_symbols) \
                                and expr[i + 1] not in self.symbols.union(self.double_symbols) or expr[i+1] in self.variables:
                            return self.error(expr)
                if lexem in list(self.numbers):
                    if i == 0:
                        return self.error(expr)
                    elif i == len(expr) - 1:
                        return self.error(expr)
                    else:
                        if expr[i - 1] not in self.symbols.union(self.double_symbols) \
                                and expr[i + 1] not in self.symbols.union(self.double_symbols):
                            return self.error(expr)

                if lexem in list(self.symbols):
                    if i == 0:
                        return self.error(expr)
                    elif i == len(expr) - 1 and not lexem == ";":
                        return self.error(expr)
                    elif lexem == "[":
                        if expr[i - 1] in self.variables:
                            resp = self.parse_square(expr, i)
                            if resp:
                                return resp
                        else:
                            return self.error(expr)
                    elif lexem == "]":
                        flag = False
                        for j in range(i, 0):
                            if expr[j] == "[":
                                flag = True
                            if not flag:
                                return self.error(expr)
                    elif lexem == "(":
                        if i == 0:
                            return self.error(expr)
                        elif expr[i+1] != "(":
                            self.error(expr)
                        else:
                            resp = self.parse_round()
                            if resp:
                                return resp
                    elif lexem == ")":
                        flag = False
                        for j in range(i, 0):
                            if expr[j] == "(":
                                flag = True
                            if not flag:
                                return self.error(expr)
                    else:
                        if expr[i - 1] not in self.numbers.union(self.variables):
                            if i != len(expr) - 1 and expr[i + 1] not in self.variables.union(self.numbers):
                                return self.error(expr)
                if lexem in list(self.double_symbols):
                    if i != 1:
                        return self.error(expr)
        return "Success"

if __name__ == "__main__":
    example = "n:=n-1;  b:=b1a(n) ;"
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
