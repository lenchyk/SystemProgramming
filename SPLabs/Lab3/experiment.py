# Lab3

reserved_words_Pascal = ["and", "array", "begin", "case", "const",
                         "div", "do", "downto", "else", "end",
                         "file", "for", "function", "goto", "if",
                         "in", "label", "mod", "nil", "not",
                         "of", "or", "packed", "procedure", "program",
                         "record", "repeat", "set", "then", "to",
                         "type", "until", "var", "while", "with"]

special_symbols = "+ - * / = < > [ ] . , ; ( ) : ^ @ { } $ # & %".split()
special_double_symbols = ">= := += -= *= /= (* *) (. .) // << >> ** <> >< <=".split()


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

    def analise(self, input):
        variable = str()
        number = str()

        for word in input.split():
            if word in reserved_words_Pascal:
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

                elif sym in special_symbols:
                    if word.index(sym) + 1 < len(word) \
                            and sym + word[word.index(sym) + 1] in special_double_symbols:
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
                    self.undefined.add(sym)
                    self.stop(variable, number)
                    variable = number = str()

            self.stop(variable, number)
            variable = number = str()

    def check_undefined(self):
        seq = self.variables
        for test in seq:
            if test in reserved_words_Pascal:
                self.reserved_words.add(test)
                self.variables.remove(test)
            if test[0].isdigit():
                self.undefined.add(test)
                self.variables.remove(test)
        self.variables = set(self.variables)
        seq = self.numbers
        for test in seq:
            for i in test:
                if not i.isdigit():
                    self.undefined.add(test)
                    #self.numbers.remove(test)
        self.numbers = set(self.numbers)


if __name__ == "__main__":
    example = "1whil1en<>0 do be gin n:=n-1;  b:=b+a[n] en d1"
    print(example)

    analyser = Analyser()
    analyser.analise(example)
    analyser.check_undefined()

    print("Symbols: ", analyser.symbols)
    print("Double symbols: ", analyser.double_symbols)
    print("Reserved words: ", analyser.reserved_words)
    print("Variables: ", analyser.variables)
    print("Numbers: ", analyser.numbers)
    print("Undefined: ", analyser.undefined)



