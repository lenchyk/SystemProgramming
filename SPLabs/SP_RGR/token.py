import os


class Token:
    token_dict = {
        'parts': ['uses', 'begin', 'var', 'type', 'const'],
        'key word': ['program', 'var', 'procedure', 'function', 'while', 'repeat', 'of', 'for', 'to', 'do',
                     'if', 'then', 'else', 'begin', 'until', 'end'],
        'I/O word': ['write', 'writeln', 'readln'],
        'type word': ['integer', 'byte', 'word', 'real', 'double', 'boolean', 'char', 'string', 'text', '^', 'array'],
        'owner word': [':='],
        'binary operation': ['+', '-', '*', '/', 'div'],
        'separator': [',', ';', ':', '.', '..', '[', ']', '(', ')'],
        'brackets open': ['(', '['],
        'brackets close': [')', ']'],
        'comparing operation': ['<', '>', '<=', '>=', '<>', '='],
        'string constant': ['\'', '"']
    }


    def combine_commands(self, code, l):
        temp = []
        j = 0
        for i in range(len(code)):
            j = i
            if code[i] != ';':
                temp.append(code[i])
            else:
                temp.append(';')
                l.append(temp)
                break
        else:
            l.append(temp)
        if code[j + 1:]:
            return self.combine_commands(code[j + 1:], l)
        else:
            if l[-1] == ['']:
                l = l[:-1]
            return l


    def preview_command(self, command, command_number):
        if command[-1] == ';':
            return self.parse_commands(command[:-1], command_number)
        else:
            s = ''
            for i in command:
                s += i
            return 'Error in {}\n";" expected', command_number


    def parse_commands(self, command, command_number, state='', vars=None, cur_type=None):
        if not state and os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vars.txt'):
            with open('vars.txt', 'r') as file:
                res = file.read()
                if res[-1] != '.':
                    state = 'var'

        if state == 'const':
            for i in range(len(command)):
                if command[i] == 'begin':
                    command.pop(i)
                    with open('vars.txt', 'a') as file:
                        file.write('.')
                    return self.parse_commands(command, command_number, state='')
                elif command[i] == 'var':
                    return self.parse_commands(command, command_number, state='var')
                elif (command[i] not in [*self.token_dict['type word'], '=', *self.token_dict['separator']] and
                      command[i].isalnum() and command[i][0].isalpha()):
                    if vars:
                        text = []
                        if os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vars.txt'):
                            with open('vars.txt', 'r') as file:
                                text = file.read().split()
                        if command[i] not in [*vars, *text]: vars.append(command[i])
                        else: return 'Error in {}\nVariable have been initialized', command_number
                    else: vars = [command[i]]
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='const', vars=vars)
                elif command[i] == '=':
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='const', vars=vars)
                elif vars and command[i] not in [*self.token_dict['type word'], '=', *self.token_dict['separator']]:
                    vars.append(command[i])
                    # print(vars)
                    with open('vars.txt', 'w') as varst:
                        if vars[1].isdigit():
                            varst.write('{} {}\n'.format(vars[0], 'integer'))
                        elif vars[1].replace('.', '').isdigit():
                            varst.write('{} {}\n'.format(vars[0], 'real'))
                    with open('vals.txt', 'w') as valst:
                        valst.write('{} {}\n'.format(vars[0], vars[1]))
                    command.pop(i)
            return self.parse_commands(command, command_number, state='')

        if state == 'var':
            for i in range(len(command)):
                if command[i] == 'begin':
                    command.pop(i)
                    with open('vars.txt', 'a') as file:
                        file.write('.')
                    valsf = open('vals.txt', 'r')
                    vals = valsf.read().split('\n')
                    code, ascode = open('code.py', 'w'), open('gen_asm.txt', 'w')
                    used_vars = []
                    for j in range(len(vals) - 1):
                        eq = vals[j].index(' ')
                        if vals[j][:eq] not in used_vars:
                            code.write(vals[j][:eq] + ' = ' + vals[j][eq + 1:] + '\n')
                            used_vars.append(vals[j][:eq])
                        else:
                            return 'Error in {}\nVariable have been initialized', command_number - 1
                    code.close(); ascode.close()
                    valsf.close()
                    return self.parse_commands(command, command_number, state='')
                elif command[i] not in [*self.token_dict['type word'], *self.token_dict['separator']]:
                    if vars:
                        text = []
                        if os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vars.txt'):
                            with open('vars.txt', 'r') as file:
                                text = file.read().split()
                        if command[i] not in [*vars, *text] and command[i] != 'var': vars.append(command[i])
                        else: return 'Error in {}\nVariable have been initialized', command_number
                    elif command[i] != 'var': vars = [command[i]]
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='var', vars=vars)
                elif command[i] == ':':
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='var', vars=vars)
                elif command[i] in self.token_dict['type word']:
                    if command[i] == 'array':
                        if command[i + 1] != '[':
                            return 'Error in {}\nUnexpected symbol in array initializing', command_number
                        if not all([command[i + 2].isdigit(), command[i + 4].isdigit()]):
                            with open('vals.txt', 'r') as vals:
                                vals = vals.read().split()
                                if command[i + 2] in vals:
                                    command[i + 2] = vals[vals.index(command[i + 2]) + 1]
                                elif command[i + 4] in vals:
                                    command[i + 4] = vals[vals.index(command[i + 4]) + 1]
                                else:
                                    return 'Error in {}\nUnexpected symbol in array initializing', command_number
                                return self.parse_commands(command, command_number, state='var', vars=vars)
                        if command[i + 3] != '..':
                            return 'Error in {}\nUnexpected symbol in array initializing', command_number
                        if command[i + 5] != ']':
                            return 'Error in {}\nUnexpected symbol in array initializing', command_number
                        if command[i + 6] != 'of':
                            return 'Error in {}\nUnexpected symbol in array initializing', command_number
                        if command[i + 7] not in self.token_dict['type word']:
                            return 'Error in {}\nUnexpected type in array initializing', command_number
                        if os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vars.txt'):
                            with open('vars.txt', 'a') as file:
                                file.write(vars[0])
                                s = ''
                                for j in range(8):
                                    s += ' {}'.format(command[i + j])
                                file.write(s + '\n')
                            with open('vals.txt', 'a') as file:
                                file.write(vars[0] + ' ' + str([None] * int(command[i + 4])) + '\n')
                        else:
                            with open('vars.txt', 'w') as file:
                                file.write(vars[0])
                                s = ''
                                for j in range(8):
                                    s += ' {}'.format(command[i + j])
                                file.write(s + '\n')
                            with open('vals.txt', 'w') as file:
                                file.write(vars[0] + ' ' + str([None] * int(command[i + 4])) + '\n')
                        return self.parse_commands(command, command_number, state='var')
                    if os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vars.txt'):
                        with open('vars.txt', 'a') as file:
                            for j in vars:
                                file.write('{} {}\n'.format(j, command[i]))
                        with open('vals.txt', 'a') as file:
                            for j in vars:
                                file.write('{} None\n'.format(j))
                    else:
                        with open('vars.txt', 'w') as file:
                            for j in vars:
                                file.write('{} {}\n'.format(j, command[i]))
                        with open('vals.txt', 'w') as file:
                            for j in vars:
                                file.write('{} None\n'.format(j))
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='var')
                else:
                    return 'Error in {}\nUnexpected statement in variables initializing', command_number

        if state[:-2] == 'brackets open':
            for i in range(len(command)):
                if state[-1] == '0' and command[i] == self.token_dict['brackets close'][0]:
                    with open('vars.txt', 'r') as file:
                        text = file.read().split()
                        if command[i - 1] not in text:
                            return 'Error in {}\nUnexpected symbol1', command_number
                        if text[text.index(command[i - 1]) + 1] != 'integer':
                            return 'Error in {}\ninteger expected', command_number
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='binary operation')
                elif state[-1] == '1' and command[i] == self.token_dict['brackets close'][1]:
                    with open('vars.txt', 'r') as file:
                        text = file.read().split()
                        if command[i - 1] not in text:
                            return 'Error in {}\nUnexpected symbol2', command_number
                        if text[text.index(command[i - 1]) + 1] != 'integer' and not command[i - 1].isdigit():
                            return 'Error in {}\ninteger expected', command_number
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='binary operation')
            if state[-1] == '0': b = ')'
            else: b = ']'
            return 'Error in {}\n"' + b + '" expected', command_number

        if state == 'binary operation':
            for i in range(len(command)):
                if command[i] == self.token_dict['brackets open'][0]:
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='brackets open 0')
                if command[i] == self.token_dict['brackets open'][1]:
                    command.pop(i)
                    return self.parse_commands(command, command_number, state='brackets open 1')
                if command[i] in self.token_dict['brackets close']:
                    return 'Error in {}\nUnexpected symbol3', command_number

        if state == 'owner word':
            for i in range(len(command)):
                if command[i] in self.token_dict['binary operation']:
                    with open('vars.txt', 'r') as file:
                        text = file.read().split()
                        if '[' in command:
                            with open('vals.txt', 'r') as vals:
                                vals = vals.read()
                                vals_end = vals[:].split('\n')
                                vals = vals.split()
                            with open('vars.txt', 'r') as vars:
                                vars = vars.read().split()
                            if command[command.index('[') - 1] not in vars:
                                return 'Error in {}\nUnexpected symbol', command_number
                            elif vars[vars.index(command[command.index('[') - 1]) + 1] != 'array':
                                return 'Error in {}\nUnexpected symbol', command_number
                            if command[command.index('[') + 1] not in vars and not (command[command.index('[') + 1].isdigit() or
                                                                                    command[command.index('[') + 1] == '('):
                                return 'Error in {}\nUnexpected symbol6', command_number
                            elif vars[vars.index(command[command.index('[') + 1]) + 1] != 'integer':
                                return 'Error in {}\nUnexpected symbol7', command_number
                            elif vals[vals.index(command[command.index('[') + 1]) + 1] == 'None':
                                return 'Error in {}\nUnexpected symbol8', command_number
                            for j in vals_end:
                                if command[command.index('[') - 1] + ' [' in j:
                                    lst = eval(j[2:])
                                    if len(lst) < int(vals[vals.index(command[command.index('[') + 1]) + 1]):
                                        import code
                                        if len(lst) < code.n:
                                            return 'Error in {}\nIndex out of range', command_number
                                    elif lst[int(vals[vals.index(command[command.index('[') + 1]) + 1]) - 1] == None:
                                        return 'Error in {}\nEmpty element', command_number
                            with open('code.py', 'a') as code:
                                code.write('{} = {} {} {} {}{} - 1{}\n'.format(*command))
                            with open('gen_asm.txt', 'a') as gen_asm:
                                gen_asm.write('mov eax, {}\n'.format(command[0]))
                                used = command[0]
                                command.pop(0)
                                for i in command:
                                    if i == used: command.remove(i)
                                pointer = command.index('[')
                                gen_asm.write('mov ebx, {}\n'.format(command[pointer + 1]))
                                command.pop(pointer + 2); command.pop(pointer + 1); command.pop(pointer)
                                if '+' in command:
                                    command.remove('+')
                                    gen_asm.write('add eax, {}[ebx*4-4]\n'.format(command[0]))
                                elif '-' in command:
                                    command.remove('-')
                                    gen_asm.write('sub eax, {}[ebx*4-4]\n'.format(command[0]))
                                else:
                                    return 'Error in {}\nUnexpected operand', command_number
                                gen_asm.write('mov {}, eax\n'.format(used))

                        elif command[i - 1] in text or command[i - 1].isdigit() and command[i + 1] in text or command[i + 1].isdigit():
                            if command[i - 1] in text:
                                with open('vals.txt', 'r') as vals:
                                    vals = vals.read().split()
                                    if vals[vals.index(command[i - 1]) + 1] == 'None':
                                        import code
                                        if not eval('code.{}'.format(command[i - 1])):
                                            return 'Error in {}\nArgument without value', command_number
                            if command[i + 1] in text:
                                with open('vals.txt', 'r') as vals:
                                    vals = vals.read().split()
                                    if not command[i + 1].isdigit() and vals[vals.index(command[i + 1]) + 1] == 'None':
                                        import code
                                        if not eval('code.{}'.format(command[i + 1])):
                                            return 'Error in {}\nArgument without value', command_number
                            this_type = text[text.index(command[i - 1]) + 1]
                            index = 1
                            if text[text.index(command[i + 1]) + 1] == 'array':
                                index = 3
                                if command[i + 3] not in text:
                                    return 'Error in {}\nUnexpected symbol9', command_number
                            if this_type != text[text.index(command[i + index]) + 1] and not command[i + index].isdigit():
                                error_type = 'Type {} expected, got {} {} {}'.format(cur_type, this_type, command[i],
                                                                                     text[text.index(command[i + 1]) + 1])
                                return 'Error in {}\n' + error_type, command_number
                            with open('code.py', 'a') as code:
                                code.write('{} = {} {} {}\n'.format(*command))
                            with open('gen_asm.txt', 'a') as gen_asm:
                                gen_asm.write('mov eax, {}\n'.format(command[0]))
                                used = command[0]
                                command.pop(0)
                                for i in command:
                                    if i == used: command.remove(i)
                                gen_asm.write('mov ebx, {}\n'.format(command[-1]))
                                command.pop()
                                if '+' in command:
                                    command.remove('+')
                                    gen_asm.write('add eax, ebx\n')
                                elif '-' in command:
                                    command.remove('-')
                                    gen_asm.write('sub eax, ebx\n')
                                else:
                                    return 'Error in {}\nUnexpected operand', command_number
                                gen_asm.write('mov {}, eax\n'.format(used))
                        else:
                            return 'Error in {}\nUnexpected symbol10', command_number
                    command.pop(i)
                    if len(command) < 2:
                        return 'Error in {}\nOperand expected', command_number
                    return self.parse_commands(command, command_number, state='binary operation')

        for i in range(len(command)):
            if command[i] in self.token_dict['parts']:
                if command[i] == 'var':
                    state = 'var'
                elif command[i] == 'const':
                    state = 'const'
                elif command[i] == 'uses':
                    state = 'uses'
                elif command[i] == 'begin':
                    state = 'key word'
                command.pop(i)
                return self.parse_commands(command, command_number, state=state)
            elif command_number == 0:
                    return 'Error in {}\nUnexpected statement', command_number

        for i in range(len(command)):
            if command[i] in self.token_dict['key word']:
                command.pop(i)
                return self.parse_commands(command, command_number, state='key word')

        for i in range(len(command)):
            if command[i] in self.token_dict['owner word']:
                with open('vars.txt', 'r') as file:
                    text = file.read().split()
                    if command[i - 1] not in text:
                        return 'Error in {}\nUnexpected symbol', command_number
                    cur_type = text[text.index(command[i - 1]) + 1]
                command.pop(i)
                if len(command) == 2:
                    if command[1] in text:
                        new_type = text[text.index(command[1]) + 1]
                        if cur_type != new_type:
                            return 'Error in {}\nUnexpected type of operand', command_number
                    else:
                        if cur_type == 'integer' and not command[1].isdigit():
                            return 'Error in {}\nUnexpected type of operand', command_number
                        if cur_type in ['real', 'double'] and not command[1].replace('.', '').isdigit():
                            return 'Error in {}\nUnexpected type of operand', command_number
                        if cur_type == 'char' and not command[1][2].isalpha():
                            return 'Error in {}\nUnexpected type of operand', command_number
                    if os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vals.txt'):
                        with open('vals.txt', 'r') as vals:
                            text = vals.read().split('\n')
                            for j in text:
                                if j == '': text.remove(j)
                        for j in range(len(text)):
                            line = text[j].split()
                            if command[0] == line[0]:
                                line[1] = command[1]
                            line = ' '.join(line)
                            text[j] = line
                    else:
                        text = ['{} {}'.format(*command)]
                    with open('vals.txt', 'w') as vals:
                        vals.write('\n'.join(text))
                    with open('code.py', 'a') as code:
                        code.write('{} = {}\n'.format(*command))
                    with open('gen_asm.txt', 'a') as gen_asm:
                        gen_asm.write('mov ebx, {}\n'.format(command[-1]))
                        command.pop()
                        gen_asm.write('mov {}, ebx\n'.format(command[0]))
                        command.pop()
                if '[' in command and len(command) == 5:
                    cur_type = text[text.index(command[i - 1]) + 2]
                    if cur_type == 'integer' and not command[4].isdigit():
                        return 'Error in {}\nUnexpected type of operand', command_number
                    if cur_type in ['real', 'double'] and not command[4].replace('-', '').replace('.', '').isdigit():
                        return 'Error in {}\nUnexpected type of operand', command_number
                    if cur_type == 'char' and not command[4][2].isalpha():
                        return 'Error in {}\nUnexpected type of operand', command_number
                    if os.path.exists('/Users/lenasoroka/PycharmProjects/SP_RGR/vals.txt'):
                        with open('vals.txt', 'r') as vals:
                            text = vals.read().split('\n')
                            for j in text:
                                if j == '': text.remove(j)
                        for j in range(len(text)):
                            line = text[j].split()
                            if command[0] == line[0]:
                                new_line = eval(''.join(line[1:]))
                                try:
                                    new_line[int(command[2]) - 1] = eval(command[4])
                                    with open('code.py', 'a') as code:
                                        code.write('{}[{}] = {}\n'.format(command[0], int(command[2]) - 1, command[4]))
                                    with open('gen_asm.txt', 'a') as gen_asm:
                                        gen_asm.write('mov ebx, {}\n'.format(command[-1]))
                                        gen_asm.write('mov {}[{}], ebx\n'.format(command[0], int(command[2]) * 4 - 4))
                                except:
                                    for j in text:
                                        if command[1] + ' ' in j:
                                            new_line = eval(j[2:])[int(command[3]) - 1]
                                            with open('code.py', 'a') as code:
                                                code.write('{} = {}[{}]\n'.format(command[0], command[1], int(command[3]) - 1))
                                            with open('gen_asm.txt', 'a') as gen_asm:
                                                gen_asm.write('mov ebx, {}[{}]\n'.format(command[1], int(command[3]) * 4 - 4))
                                                gen_asm.write('mov {}, ebx\n'.format(command[0]))
                                            break
                                    else:
                                        return 'Error in {}\nUnexpected symbol', command_number
                                line = line[0] + ' ' + str(new_line)
                                text[j] = line
                    else:
                        text = ['{} {}'.format(*command)]
                    with open('vals.txt', 'w') as vals:
                        vals.write('\n'.join(text))
                if any(j in command for j in [*self.token_dict['owner word'], *self.token_dict['comparing operation']]):
                    return 'Error in {}\nUnexpected symbol', command_number
                if len(command) < 4 and any([i in command for i in self.token_dict['binary operation']]):
                    return 'Error in {}\nOperand expected', command_number
                return self.parse_commands(command, command_number, state='owner word', cur_type=cur_type)

        for i in range(len(command)):
            try:
                if command[i] + command[i + 1] in self.token_dict['comparing operation']:
                    if state != 'comparing operation':
                        return 'Error in {}\nUnexpected symbol', command_number
                    command.pop(i)
                    command.pop(i)
                    if any(j in command for j in [*self.token_dict['owner word'], *self.token_dict['comparing operation']]):
                        return 'Error in {}\nUnexpected symbol', command_number
                    return self.parse_commands(command, command_number, state='comparing operation')
            except IndexError:
                pass
            if command[i] in self.token_dict['comparing operation']:
                if state != 'comparing operation':
                    return 'Error in {}\nUnexpected symbol', command_number
                command.pop(i)
                if any(j in command for j in [*self.token_dict['owner word'], *self.token_dict['comparing operation']]):
                    return 'Error in {}\nUnexpected symbol', command_number
                if len(command) < 2:
                    return 'Error in {}\nOperand expected', command_number
                return self.parse_commands(command, command_number, state='comparing operation')


    def filter_empty(self, code_lst):
        res_lst = []
        for i in range(len(code_lst)):
            if code_lst[i]:
                res_lst.append(code_lst[i])

        return res_lst


    def analyzeCode(self, code):
        state = 0
        l = []
        res = ''
        for i in range(len(code)):
            if state == 0:
                if code[i].isalpha():
                    if res.isdigit():
                        return 'Error!'
                    else:
                        res += code[i]
                elif code[i].isdigit():
                    res += code[i]
                elif code[i] in [' ', '\n', '\t']:
                    if res != '': l.append(res)
                    res = ''
                elif code[i] == '/':
                    if code[i + 1] == '/':
                        if res != '': l.append(res)
                        res = code[i]
                        state = 1
                    else:
                        if res != '': l.append(res)
                        l.append(code[i])
                        res = ''
                elif code[i] in ['{', '\'']:
                    if res != '': l.append(res)
                    res = code[i]
                    state = 2
                elif code[i] == '.':
                    if res == 'end':
                        res = 'end.'
                        l.append(res)
                        return l
                    elif code[i + 1] == '.':
                        if res != '': l.append(res)
                        res = '.'
                    elif code[i - 1] == '.':
                        res = '..'
                        l.append(res)
                        res = ''
                    else:
                        res += code[i]
                elif code[i] == ';':
                    if res != '': l.append(res)
                    l.append(code[i])
                    res = ''

                elif code[i] == ':':
                    if res != '': l.append(res)
                    res = ''
                    if code[i + 1] == '=':
                        res = code[i]
                    else:
                        l.append(code[i])
                        res = ''
                elif code[i] == '=':
                    if code[i - 1] == ':':
                        res += code[i]
                        l.append(res)
                        res = ''
                    else:
                        if res != '': l.append(res)
                        l.append(code[i])
                        res = ''
                elif code[i - 1] == '=' and code[i] == '-' and code[i + 1].replace('.', '').isdigit():
                    res += code[i]
                elif code[i] in ['+', '-', '*', '(', ')', '[', ']', '<', '>', '=', '<=', '>=', '<>']:
                    if (code[i] == '(' and code[i - 1] == '[') or (code[i] == ')' and code[i + 1] == ']'):
                        pass
                    else:
                        if res != '': l.append(res)
                        l.append(code[i])
                        res = ''
            elif state == 1:
                if code[i] != '\n':
                    res += code[i]
                else:
                    l.append(res)
                    res = ''
                    state = 0
            elif state == 2:
                if code[i] not in ['}', '\'']:
                    res += code[i]
                else:
                    res += code[i]
                    l.append(res)
                    res = ''
                    state = 0
        l.append(res)
        return self.filter_empty(l)

    def iterate(self, lst):
        for i in lst:
            yield i

    def classify(self, lst):
        for i in self.iterate(lst):
            if i in self.token_dict['key word']:
                yield '{:>10} | key word'.format(i)
            elif i in self.token_dict['I/O word']:
                yield '{:>10} | I/O word'.format(i)
            elif i in self.token_dict['type word']:
                yield '{:>10} | type word'.format(i)
            elif i in self.token_dict['owner word']:
                yield '{:>10} | owner word'.format(i)
            elif i in self.token_dict['binary operation']:
                yield '{:>10} | binary operation'.format(i)
            elif i in self.token_dict['separator']:
                yield '{:>10} | separator'.format(i)
            elif i in self.token_dict['comparing operation']:
                yield '{:>10} | comparing operation'.format(i)
            elif all([j.isalnum() or j == '' for j in i.split('_')]) and i[0].isalpha():
                yield '{:>10} | identifier'.format(i)
            elif '.' in i and i.replace('.', '').isdigit():
                yield '{:>10} | decimal constant'.format(i)
            elif i.isdigit():
                yield '{:>10} | integer constant'.format(i)
            elif i[0] and i[-1] in self.token_dict['string constant']:
                yield '{:>10} | string constant'.format(i)
        print()
