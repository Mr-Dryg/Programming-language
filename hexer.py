class Hexer:
    def __init__(self) -> None:
        pass

    def scan(self, code) -> list:
        state = 'S'
        buf = ''
        result = []
        res = []
        for n, line in enumerate(code):
            for id, i in enumerate(line):
                if state == 'DEGREE':
                    if i == '*':
                        buf += i
                        res.append(buf)
                        buf = ''
                        state = 'S'
                elif state == 'S':
                    if i in [' ', '\t', '\n']:
                        if buf:
                            res.append(buf)
                    elif i.isdigit():
                        state = 'N'
                        buf += i
                    elif i.isalpha():
                        state = 'W'
                        buf += i
                    elif i in ['{', '}', ';', '(', ')', '+', '-', '**', '*', '%', '<', '>', '=']:
                        buf = ''
                        if i == '*' and id != len(line) - 1:
                            if line[id + 1] == '*':
                                buf += i
                                state = 'DEGREE'
                            else:
                                res.append(i)
                                state = 'S'
                        elif i == '-' and id != len(line) - 1 and not res[-1].isalpha():
                            if line[id + 1].isdigit():
                                buf += i
                                state = 'N'
                        else:
                            res.append(i)
                            state = 'S'
                    elif i == '/':
                        buf += i
                        state = 'FD'
                    elif i == ':':
                        buf += i
                        state = 'AS'
                    elif i == '!':
                        buf += i
                        state = 'NE'
                    else:
                        print(n, i)
                        print('ERROR')
                        exit(1)
                elif state == 'N':
                    if i == '.':
                        buf += i
                        state = 'F'
                    elif i.isdigit():
                        buf += i
                    else:
                        res.append(int(buf))
                        buf = ''
                        state = 'S'
                        if i in [' ', '\t', '\n']:
                            pass
                        elif i in ['{', '}', ';', '(', ')', '+', '-', '*', '%', '<', '>']:
                            res.append(i)
                            state = 'S'
                        elif i == '/':
                            buf += i
                            state = 'FD'
                        elif i == ':':
                            buf += i
                            state = 'AS'
                        elif i == '!':
                            buf += i
                            state = 'NE'
                        else:
                            raise ValueError(f'line {n + 1}\nnumber entered incorrectly')
                elif state == 'F':
                    if i == '.':
                        raise ValueError(f'line {n + 1}\nfractional number entered incorrectly')
                    elif i.isdigit():
                        buf += i
                    else:
                        res.append(float(buf))
                        buf = ''
                        state = 'S'
                        if i in [' ', '\t', '\n']:
                            pass
                        elif i in ['{', '}', ';', '(', ')', '+', '-', '*', '%', '<', '>']:
                            buf = ''
                            res.append(i)
                            state = 'S'
                        elif i == '/':
                            buf += i
                            state = 'FD'
                        elif i == ':':
                            buf += i
                            state = 'AS'
                        elif i == '!':
                            buf += i
                            state = 'NE'
                        else:
                            raise ValueError(f'line {n + 1}\nfractional number entered incorrectly')
                elif state == 'W':
                    if i.isalpha():
                        buf += i
                    else:
                        res.append(buf)
                        buf = ''
                        state = 'S'
                        if i in [' ', '\t', '\n']:
                            pass
                        elif i in ['{', '}', ';', '(', ')', '+', '-', '*', '%', '<', '>', ',']:
                            res.append(i)
                            state = 'S'
                        elif i == '/':
                            buf += i
                            state = 'FD'
                        elif i == ':':
                            buf += i
                            state = 'AS'
                        elif i == '!':
                            buf += i
                            state = 'NE'
                        else:
                            raise ValueError(f'line {n+1}\nvariables can only contain letters of the alphabet')
                elif state == 'FD':
                    if i == '/':
                        buf += i
                        res.append(buf)
                        buf = ''
                        state = 'S'
                    else:
                        res.append(buf)
                        buf = ''
                        state = 'S'
                        if i in [' ', '\t', '\n']:
                            pass
                        elif i.isdigit():
                            state = 'N'
                            buf += i
                        elif i.isalpha():
                            state = 'W'
                            buf += i
                        elif i in ['{', '}', ';', '(', ')', '+', '-', '*', '%', '<', '>']:
                            buf = ''
                            res.append(i)
                            state = 'S'
                        elif i == '/':
                            buf += i
                            state = 'FD'
                        elif i == ':':
                            buf += i
                            state = 'AS'
                        elif i == '!':
                            buf += i
                            state = 'NE'
                        else:
                            print(n, i)
                            print('ERROR')
                            exit(1)
                elif state in ['AS', 'NE']:
                    if i == '=':
                        buf += i
                        res.append(buf)
                        buf = ''
                        state = 'S'
                    else:
                        res.append(buf)
                        buf = ''
                        state = 'S'
                        if i in [' ', '\t', '\n']:
                            pass
                        elif i.isdigit():
                            state = 'N'
                            buf += i
                        elif i.isalpha():
                            state = 'W'
                            buf += i
                        elif i in ['{', '}', ';', '(', ')', '+', '-', '*', '%', '<', '>']:
                            buf = ''
                            res.append(i)
                            state = 'S'
                        elif i == '/':
                            buf += i
                            state = 'FD'
                        elif i == ':':
                            buf += i
                            state = 'AS'
                        elif i == '!':
                            buf += i
                            state = 'NE'
                        else:
                            print(n, i)
                            print('ERROR')
                            exit(1)
            if buf:
                print('!!!БУФЕР НЕ ПУСТ!!!')
                print(buf)
                exit(1)
            result.append(res)
            res = []
        return result


if __name__ == '__main__':
    hexer = Hexer()
    file = 'main.plg'
    code_lines = open(file, 'r').readlines()
    try:
        print(hexer.scan(code_lines))
    except ValueError as error:
        exit(f'ValueError: {error}')
