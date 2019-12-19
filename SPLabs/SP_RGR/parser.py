
class Parser:

    def __init__(self, to_parse):
        self.to_parse = to_parse

    def parse_carry(self):
        result = []
        for i in self.to_parse.split('\n'):
            if i:
                result.append(i.strip().lower())

        return result

