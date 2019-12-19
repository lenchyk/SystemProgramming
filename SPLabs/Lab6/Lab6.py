class Dictionary:
    reserved_words_Pascal = ["and", "array", "begin", "case", "const",
                             "div", "do", "downto", "else", "end",
                             "file", "for", "function", "goto", "if",
                             "in", "label", "mod", "nil", "not",
                             "of", "or", "packed", "procedure", "program",
                             "record", "repeat", "set", "then", "to",
                             "type", "until", "var", "while", "with"]

    special_symbols = "+ - * / = < > [ ] . , ; ( ) : ^ @ { } $ # & % '".split()
    special_double_symbols = ">= := += -= *= /= (* *) (. .) // << >> ** <> >< <= ''".split()
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
    string = set()

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
                return self.error(']', expr)
            elif open < close:
                return self.error('[', expr)
        # ???
        if begin - end == 1:
            return self.error(expr[begin], expr)

        for i in range(begin + 1, end):
            lexem = expr[i]
            if lexem in self.variables:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * / [ ] ( )":
                        return self.error(expr[i] + expr[i + 1], expr)
                continue

            if lexem in self.numbers:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * /":
                        return self.error(expr[i] + expr[i + 1], expr)
                continue

            if lexem in self.symbols:
                if lexem == "[":
                    if not expr[i - 1] in self.variables:
                        return self.error(expr[i - 1], expr)
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
                            return self.error("[", expr)
                    continue

                if lexem == "(":
                    resp = self.parse_round(expr, i)
                    if resp:
                        return self.error("(", expr)
                    continue
                if lexem == ")":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "(":
                            flag = True
                            break
                        if i == 0:
                            return self.error("(", expr)
                    continue

                if expr[i - 1] not in self.variables.union(self.numbers):
                    return self.error(expr[i - 1], expr)
                if expr[i + 1] not in self.variables.union(self.numbers) \
                        and expr[i + 1] != ")":
                    return self.error(expr[i - 1] + lexem + expr[i + 1], expr)
                continue
            else:
                return self.error(lexem, expr)

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
                return self.error(')', expr)
            elif open < close:
                return self.error('(', expr)

        for i in range(begin + 1, end):
            lexem = expr[i]
            if lexem in self.variables:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * / [ ] ( )":
                        return self.error(lexem, expr)
                continue

            if lexem in self.numbers:
                if i + 1 == end:
                    break
                else:
                    if expr[i+1] not in "+ - * /":
                        return self.error(lexem, expr)
                continue

            if lexem in self.symbols:
                if lexem == "[":
                    if not expr[i - 1] in self.variables:
                        return self.error(lexem, expr)
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
                            return self.error("[", expr)
                    continue

                if lexem == "(":
                    resp = self.parse_round(expr, i)
                    if not resp:
                        return self.error(lexem, expr)
                    continue
                if lexem == ")":
                    flag = False
                    for j in range(i, 0, -1):
                        if expr[j] == "(":
                            flag = True
                        if not flag:
                            return self.error("(", expr)
                    continue
                if expr[i - 1] in self.numbers:
                    return self.error(expr[i - 1], expr)
                if expr[i + 1] not in self.variables.union(self.numbers) \
                        and expr[i + 1] != ")":
                    return self.error(expr[i + 1], expr)
                continue
            else:
                return self.error(lexem, expr)

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

                    if len(number) and sym == '.':
                        number += sym
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
            elif Dictionary.is_typeword(test):
                self.type_words.add(test)
                self.variables.remove(test)
            elif test[0].isdigit():
                return "Lexical error at { " + test + " }\n"
        self.variables = set(self.variables)
        seq = self.numbers
        for test in seq:
            for i in test:
                if i not in '0123456789.':
                    return "Lexical error at { " + test + " }\n"
        self.numbers = set(self.numbers)
        return "Success"

    def error(self, lexem, expr):
        return "Syntax error at << {0} >> in  <<{1}>>  \n".format(lexem, " ".join(expr))

    def check_declarations(self, expr):
        for word in expr:
            if Dictionary.is_typeword(word):
                return word
        return False

    def string_adder(self, tree):
        for expr in tree:
            for i in range(0, len(expr)):
                lexem = expr[i]
                if lexem in self.variables:
                    if expr[i - 1] == "'" and expr[i + 1] == "'":
                        self.string.add(lexem)
                        self.variables.remove(lexem)

    def check_semantics(self, tree):
        # check declarations
        if len(self.type_words) == 0:
            return "Declarations are missing or they are incorrect!"

        declared = {variable: [] for variable in self.variables}  # dictionary for declared variables
        for expr in tree:
            for i in range(0, len(expr)):
                lexem = expr[i]

                if lexem == "var":
                    if expr[i+1] not in self.variables:
                        return "Semantic error at <{0}>".format(expr[i] + expr[i+1])

                if Dictionary.is_typeword(lexem):
                    if expr[i+1] != ';':
                        return "Semantic error ar <{0}>".format(expr[i])

                # check for declarations
                if lexem in self.variables:
                    # if expr is declaration
                    if self.check_declarations(expr):
                        declared[lexem].append(self.check_declarations(expr))
                    # other expr (n:= n - 1)
                    else:
                        if not declared[lexem]:
                            return "Semantic error: variable {0} was not declared!".format(lexem)

                        # check for correct type variable use
                        var_type = declared[lexem][0]
                        for symbol in expr:
                            if symbol in self.numbers:
                                if var_type not in ['integer', 'real']:
                                    return "Semantic error: types of <{0}> are incompatible".format("".join(expr))
                                elif '.' in symbol:
                                    if expr.index(lexem) == 0:
                                        if var_type != 'real':
                                            return "Semantic error: type of {0} is incorrect".format(lexem)
                            if symbol in self.string:
                                if var_type != "char":
                                    return "Semantic error: expected type char is not found! "

                        if var_type == "integer" and expr.index(lexem) == 0:
                            for symbol in expr[1:]:
                                if symbol in self.variables:
                                    if declared[symbol][0] != "integer":
                                        return "Semantic error: type of {0} is incorrect".format(symbol)

                    # check if there no second variable declaration
                    if len(declared[lexem]) != 1:
                        return "Semantic error: variable {0} was declared more than once!".format(lexem)


        return "Success"

    def has_type_word(self, expr):
        for lexem in expr:
            if lexem in self.type_words:
                return True
        return False

    def analyse_syn(self, input):
        syn_tree = SyntaxTree(input).tree
        self.string_adder(syn_tree)

        for expr in syn_tree:
            for i in range(0, len(expr)):
                lexem = expr[i]

                if Dictionary.is_reserved_word(lexem):
                    if lexem.lower() == "begin":
                        if "end" not in self.reserved_words:
                            return self.error(lexem, expr)

                    if lexem.lower() == "end" and lexem in self.reserved_words:
                        if expr[i+1] != ';' and syn_tree.index(expr) != len(syn_tree)-1:
                            return self.error(lexem, expr)
                        if "begin" not in self.reserved_words:
                            return self.error(lexem, expr)

                    # checking for <for ... to ... do> construction
                    if lexem.lower() == "to":
                        if expr[i+1] not in self.variables.union(self.numbers):
                            return self.error(lexem + " " + expr[i+1], expr)
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
                        return self.error("to", expr)
                    elif count == 2:
                        return self.error("do", expr)
                    elif count == 3:
                        pass
                    continue

                elif lexem in list(self.type_words):
                    if expr[i - 1] != ':' or expr[i + 1] != ';':
                        return self.error(lexem + " ", expr)

                elif lexem in list(self.variables):
                    if i == 0:
                        if syn_tree.index(expr) == 0:
                            return self.error(expr[i + 1], " ".join(expr))

                        # todo checking for symbols after a variable
                        if expr[i + 1] not in ":= += -= *= /=".split():
                            if not self.has_type_word(expr):
                                return self.error(expr[i + 1], " ".join(expr))
                    elif i == len(expr) - 1:
                        return self.error(lexem, expr)
                    else:
                        if expr[i - 1] not in self.symbols.union(self.double_symbols, self.reserved_words, self.type_words)  \
                                and expr[i + 1] not in self.symbols.union(self.double_symbols, self.reserved_words):
                            return self.error(lexem, expr)
                        elif expr[i+1] in self.variables:
                            if expr[i-1] in self.reserved_words:
                                continue
                            else:
                                return self.error(expr[i + 1], expr)

                elif lexem in list(self.numbers):
                    if i == 0:
                        return self.error(lexem, expr)
                    elif i == len(expr) - 1:
                        return self.error(lexem, expr)
                    else:
                        if expr[i - 1] not in self.symbols.union(self.double_symbols) \
                                and expr[i + 1] not in self.symbols.union(self.double_symbols):
                            return self.error(lexem, expr)

                elif lexem in list(self.symbols):
                    # at the beginning
                    if i == 0:
                        return self.error(lexem, expr)
                    # in the end
                    elif i == len(expr) - 1:
                        # if "end" is in the end of all input without '.'
                        if syn_tree.index(expr) == len(syn_tree)-1\
                                and expr[i - 1].lower() == "end" and lexem != '.':
                            return self.error(lexem, expr)
                        # if 'end' is in the middle without ';'
                        elif syn_tree.index(expr) != len(syn_tree)-1\
                                and expr[i - 1].lower() == "end" and lexem != ';':
                            return self.error(lexem, expr)
                        elif expr[i - 1].lower() in self.reserved_words and expr[i-1].lower() != "end":
                            return self.error(lexem, expr)
                    # in the middle
                    elif lexem == "[":
                        if expr[i - 1] in self.variables:
                            resp = self.parse_square(expr, i)
                            if resp:
                                return resp
                        else:
                            return self.error(lexem, expr)
                    elif lexem == "]":
                        flag = False
                        for j in range(i, 0):
                            # for close brace there is open one
                            if expr[j] == "[":
                                flag = True
                            if not flag:
                                return self.error(lexem, expr)
                    elif lexem == "(":
                        if i == 0:
                            return self.error(lexem, expr)
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
                                return self.error(lexem, expr)
                    else:
                        if expr[i - 1] not in self.numbers.union(self.variables):
                            if i != len(expr) - 1 and expr[i + 1] not in self.variables.union(self.numbers) and lexem != "'" or\
                               i != len(expr) - 1 and expr[i + 1] not in self.reserved_words and lexem != "'":
                                print("here")
                                return self.error(expr[i - 1] + expr[i] + expr[i + 1], expr)

                        elif expr[i-1] in self.variables and expr[i+1] in self.symbols.union(self.double_symbols) and lexem != "'":
                            return self.error(expr[i - 1] + expr[i] + expr[i + 1], expr)

                elif lexem in list(self.double_symbols):
                    if expr[i-1] not in self.variables and expr[i+1] not in self.variables.union(self.numbers, "'"):
                        return self.error(lexem, expr)

                elif lexem in self.string:
                    if expr[i-1] != "'" and expr[i+1] != "'":
                        return self.error(lexem, expr)

                else:
                    return self.error(lexem, expr)

        return "Success", syn_tree

if __name__ == "__main__":
    # example = "float *b, a[3]; int n; n:= n - 1; b:=b+a[n];"
    example = "var n: integer; a: integer; b: integer; s: char; n:= n - 1; b:= b + a; s:='str';"
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

        if resp_syn[0] == "Success":
            print("Syntax analysis passed")
        else:
            print(resp_syn)
            break

        resp_sem = analyser.check_semantics(resp_syn[1])
        if resp_sem == "Success":
            print("Semantic analysis passed")
        else:
            print(resp_sem)
        break
