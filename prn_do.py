from hexer import Hexer
from syntax import Parser


class Prn:
    def __init__(self, lexems, line_len) -> None:
        self.lexems = lexems
        self.line_len = line_len

    def do(self):
        self.i = 0
        stack = []
        try:
            while self.i < len(self.lexems):
                obj = self.lexems[self.i]
                if obj.type not in ['command', 'condition', 'operation']:
                    stack.append(obj)
                elif obj.type == 'command':
                    if obj.value in ['int', 'float', 'bool']:
                        while stack:
                            if not stack[-1].type is str:
                                break
                            obj.eval(stack.pop())
                    elif obj.value in ['print', 'input']:
                        obj.eval(stack.pop())
                    elif obj.value == 'goto':
                        self.i = stack.pop().value - 1
                    elif obj.value == 'not':
                        stack.append(obj.eval(stack.pop()))
                elif obj.type == 'operation':
                    if obj.value == ':=':
                        obj.eval(stack.pop(), stack.pop())
                    else:
                        stack.append(obj.eval(stack.pop(), stack.pop()))
                elif obj.type == 'condition':
                    index = stack.pop()
                    if not stack.pop().value:
                        self.i = index.value - 1
                self.i += 1
        except ValueError as e:
            line = 0
            while sum(self.line_len[:line]) <= self.i:
                line += 1
            raise ValueError(f'line {line}\n{e.args[0]}')


if __name__ == '__main__':
    file = 'main.plg'
    code_lines = open(file, 'r').readlines()
    hexer = Hexer()
    parser = Parser()
    try:
        code = hexer.scan(code_lines)
        prn_code, line_len = parser.prn(code)
        PRN = Prn(prn_code, line_len)
        PRN.do()
    except ValueError as error:
        exit(f'ValueError: {error}')
