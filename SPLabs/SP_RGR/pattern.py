from token import Token


class Pattern:
    command_result = None
    pattern_dict = {
        'for': [('to', 'downto'), ('do',), ('begin',), ('end;',)],
        ':=': [('+', '-', '*', '/', 'div')],
    }

    def __init__(self, line_command):
        self.state = 0
        self.command, self.line_command = line_command, line_command
        self.identifier, self.pattern = self.get_pattern()
        if self.identifier == 'for':
            self.command_result = self.conduct_for()


    def get_pattern(self):
        for i in list(self.pattern_dict.keys()):
            if i in self.line_command.split(' '):
                return i, self.pattern_dict[i]

        raise AttributeError
    def check_content(self, content):
        content_list = Token().analyzeCode(content)
        if len(content_list) == 1 and content_list[0] not in Token().token_dict['key word']:
            return {'number': content_list[0]}
        else:
            d = {}
            content = ' '.join(content_list)
            if any([i in content for i in [':=', '+', '-', '*', '/', 'div']]):
                try:
                    if ':=' in content:
                        content_before, content_after = content.split(' := ')
                        if len(Token().analyzeCode(content_before)) == 1:
                            d['identifier'] = content_before
                            d['owner word'] = ':='
                        else:
                            return '\nError in operand\n{}\nUnexpected symbol'.format(content_before)
                    else:
                        content_after = content
                except:
                    return '\nError in operand\n{}\nUnexpected symbol'.format(content)

                if len(Token().analyzeCode(content_after)) == 1:
                    d['number'] = content_after
                elif Token().parse_commands(content, 0) == None:
                    d['number'] = content_after
                else:
                    return '\nError in operand\n{}\nUnexpected symbol'.format(content_after)
            else:
                return '\nError in operand\n{}\nUnexpected symbol'.format(content)
            return d


    def check_actions(self, actions, on_begin=True):
        actions = actions.replace(';', ';\n').split('\n')
        l = []
        if len(actions) > 2 and not on_begin:
            return '\nError in operands\n{}\nOperands begin before, end after operands expected'.format(actions)
        result = Token().analyzeCode(' '.join(actions))
        result = Token().combine_commands(result, [])
        for i in range(len(result)):
            try:
                err, num = Token().preview_command(result[i], i)
                return err.format(''.join(result[num]))
            except:
                l.append(' '.join(result[i]))
        return l


    def conduct_for(self):
        #local_auto = [0, 1, 2, 3, 4]
        result = {}

        if self.state == 0:
            self.line_command = self.line_command.replace('for', '')
            self.line_command = self.line_command.strip()
            result['for'] = 'for'
            self.state = 1
        else:
            raise AttributeError

        if self.state == 1:
            for i in self.pattern_dict['for'][0]:
                if i + ' ' in self.line_command:
                    self.line_command = self.line_command.split(i)
                    result['start'] = self.check_content(self.line_command[0].strip())
                    result['vector'] = i
                    self.line_command = self.line_command[1].strip()
                    self.state = 2
                    break
            if self.state != 2:
                return '\nError in line\n{}\nOperand to or downto expected'.format(self.command)
        else:
            raise AttributeError

        if self.state == 2:
            if self.pattern_dict['for'][1][0] + ' ' in self.line_command:
                self.line_command = self.line_command.split('do')
                result['stop'] = self.check_content(self.line_command[0].strip())
                result['do'] = 'do'
                self.line_command = self.line_command[1].strip()
                self.state = 3
            if self.state != 3:
                return '\nError in line\n{}\nOperand do expected'.format(self.command)
        else:
            raise AttributeError

        if self.state == 3:
            if self.pattern_dict['for'][2][0] + ' ' in self.line_command:
                self.line_command = self.line_command.split('begin')
                if self.line_command[0] != '' and not self.line_command[0].isspace():
                    return '\nError in line\n{}\nUnexpected symbol between operands do and begin'.format(self.command)
                result['begin'] = 'begin'
                self.line_command = self.line_command[1].strip()
                self.state = 4
            if self.state != 4:
                result['actions'] = self.check_actions(self.line_command, False)
                self.state = 0
                return result
        else:
            raise AttributeError

        if self.state == 4:
            if self.pattern_dict['for'][3][0] in self.line_command:
                self.line_command = self.line_command.split('end;')
                if self.line_command[1] != '' and not self.line_command[1].isspace():
                    return '\nError in line\n{}\nUnexpected symbol after end operand'.format(self.command)
                result['actions'] = self.check_actions(self.line_command[0].strip())
                result['end'] = 'end'
                self.state = 0
                return result
            else:
                return '\nError in line\n{}\nOperand end expected'.format(self.command)
