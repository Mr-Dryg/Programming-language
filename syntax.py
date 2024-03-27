from hexer import Hexer
from prn_objects import Prn_Object


class Parser:
    def __init__(self) -> None:
        self.stack = []
        self.result = []
        self.len_lines = []
        self.variables = {}

    def lexema(self) -> str:
        return str(self.lexems[self.line][self.i])

    def next(self):
        self.i += 1
        if len(self.lexems[self.line]) == self.i:
            self.len_lines.append(len([x for x in self.lexems[self.line] if x not in ['(', ')', '{', '}', ';', ',']]))
            self.i = 0
            self.line += 1

    def prn(self, list_of_lexems):
        self.lexems = list_of_lexems
        self.line = 0
        self.i = 0
        self.B()
        return self.result, self.len_lines

    def B(self):
        if self.lexema() != '{':
            self.line += 1
            raise ValueError('line %s\nblock of statements must start with "{"' % self.line)
        self.next()
        self.S()
        if self.lexema() != ';':
            raise ValueError(f'line {self.line}\nstatement must end with ";"')
        self.next()
        try:
            while self.lexema() != '}':
                self.S()
                if self.lexema() != ';':
                    raise ValueError(f'line {self.line}\nstatement must end with ";"')
                self.next()
        except IndexError:
            self.line += 1
            raise ValueError('line %s\nblock of statements must end with "}"' % self.line)
        self.next()

    def S(self):
        if self.lexema() in ['int', 'bool', 'float']:
            self.stack.append(self.lexema())
            self.next()
            self.variables[None] = None
            self.V()
            while self.lexema() == ',':
                self.next()
                self.variables[None] = None
                self.V()
            if ';' in self.lexems[self.line] and self.lexema() != ';':
                raise ValueError(f'line {self.line}\nvariables must be separated by ","')
            while self.stack[-1] not in ['int', 'bool', 'float']:
                _ = self.stack.pop()
                self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
            _ = self.stack.pop()
            self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
        elif self.lexema() == 'if':
            self.next()
            self.E()
            index = len(self.result)
            self.result.append('_index_if_')
            self.result.append(Prn_Object('if'))
            self.B()
            self.result[index] = Prn_Object(len(self.result))
            if self.lexema() == 'else':
                self.result[index] = Prn_Object(self.result[index].value + 2)
                index = len(self.result)
                self.result.append('_index_else_')
                self.result.append(Prn_Object('goto'))
                self.next()
                self.B()
                self.result[index] = Prn_Object(len(self.result))
        elif self.lexema() == 'while':
            self.next()
            start = len(self.result)
            self.E()
            index = len(self.result)
            self.result.append('_index_w_')
            self.result.append(Prn_Object('while'))
            self.B()
            self.result.append(Prn_Object(start))
            self.result.append(Prn_Object('goto'))
            self.result[index] = Prn_Object(len(self.result))
        elif self.lexema() == 'input':
            self.stack.append(self.lexema())
            self.next()
            if self.lexema() != '(':
                raise ValueError(f'line {self.line + 1}\nafter input must go "("')
            self.next()
            self.V()
            if self.lexema() != ')':
                raise ValueError(f'line {self.line + 1}\nmaybe you forgot ")"?')
            self.next()
            while self.stack[-1] != 'input':
                _ = self.stack.pop()
                self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
            _ = self.stack.pop()
            self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
        elif self.lexema() == 'print':
            self.stack.append(self.lexema())
            self.next()
            self.E()
            while self.stack:
                if self.stack[-1] == 'print':
                    break
                _ = self.stack.pop()
                self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
            _ = self.stack.pop()
            self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
        else:
            if ':=' in self.lexems[self.line]:
                self.V()
                if self.lexema() != ':=':
                    raise ValueError(f'line {self.line + 1}\nmaybe you forgot ":="?')
                self.stack.append(self.lexema())
                self.next()
                self.E(common=0)
                while self.stack[-1] != ':=':
                    _ = self.stack.pop()
                    self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
                _ = self.stack[-2]
                self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
                _ = self.stack.pop()
                self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
                self.stack.pop()
            else:
                raise ValueError(f'line {self.line + 1}\nunexpected {self.lexema()}')

    def E(self, common=True):
        if common:
            if self.lexema() != '(':
                raise ValueError(f'line {self.line + 1}\nexpression must start with "("')
            self.next()
        self.E1()
        while self.lexema() in ['>', '<', '=', '!=']:
            self.stack.append(self.lexema())
            self.next()
            self.E1()
            _ = self.stack.pop()
            self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
        if common:
            if self.lexema() != ')':
                raise ValueError(f'line {self.line}\nexpression must end with ")"')
            self.next()

    def E1(self):
        self.T()
        while self.lexema() in ['+', '-', 'or']:
            self.stack.append(self.lexema())
            self.next()
            self.T()
            _ = self.stack.pop()
            self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)

    def T(self):
        self.F()
        while self.lexema() in ['**', '*', '/', '%', '//', 'and']:
            self.stack.append(self.lexema())
            self.next()
            self.F()
            _ = self.stack.pop()
            self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)

    def F(self):
        res = []
        g = None
        if self.lexema() == 'not':
            self.next()
            self.F()
            self.result.append(Prn_Object('not'))
        else:
            for func in [self.L, self.V, self.N, self.R, self.E]:
                try:
                    func()
                    g = func
                except ValueError:
                    res.append(0)
                else:
                    res.append(1)
                    break
            if g != self.E:
                _ = self.stack.pop()
                self.result.append(Prn_Object(_)) if type(_) is not Prn_Object else self.result.append(_)
            if not any(res):
                raise ValueError(f"""line {self.line + 1}\nsure you didn't make a misstakes
most probable ones:
- variable names can only contain alphabetic characters
- fractional number entered incorrectly
- bool type can be only True or False
- expression must start with "("
- expression must end with ")""" + '"')

    def L(self):  # bool
        if self.lexema() not in ['True', 'False']:
            raise ValueError(f'line {self.line + 1}\nbool type can be only True or False')
        self.stack.append(self.lexema())
        self.next()

    def V(self):  # variable
        if not self.lexema().isalpha():
            raise ValueError(f'line {self.line + 1}\nvariable names can only contain alphabetic characters')
        if None in self.variables:
            self.variables[self.lexema()] = Prn_Object(self.lexema())
            del self.variables[None]
        try:
            self.stack.append(self.variables[self.lexema()])
        except KeyError:
            exit(f"ValueError: line {self.line + 1}\nusing an undeclared variable {self.lexema()}")
        self.next()

    def N(self):  # float
        if not self.check_float():
            raise ValueError(f'line {self.line + 1}\nfractional number entered incorrectly')
        self.stack.append(self.lexema())
        self.next()

    def R(self):  # int
        if not self.check_int():
            raise ValueError(f'line {self.line + 1}\nnumber entered incorrectly')
        self.stack.append(self.lexema())
        self.next()

    def check_int(self) -> bool:
        try:
            int(self.lexema())
        except ValueError:
            return False
        else:
            return True

    def check_float(self) -> bool:
        try:
            float(self.lexema())
        except ValueError:
            return False
        else:
            return True


if __name__ == '__main__':
    file = 'main.plg'
    code_lines = open(file, 'r').readlines()
    hexer = Hexer()
    parser = Parser()
    try:
        code = hexer.scan(code_lines)
        prn, len_lines = parser.prn(code)
        print(prn)
        print(len_lines)
    except ValueError as error:
        exit(f'ValueError: {error}')
