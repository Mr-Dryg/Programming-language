class Prn_Object:
    def __init__(self, value) -> None:
        if str(value).replace('-', '').isdigit() or type(value) is int:  # int
            self.type = int
            self.value = int(value)
        elif value in ['**', '*', '/', '%', '//', 'and', '+', '-', 'or', '>', '<', '=', '!=', ':=']:  # operation
            self.type = 'operation'
            self.value = value
        elif str(value) in ['True', 'False'] or type(value) is bool:  # bool
            self.type = bool
            self.value = 1 if str(value) == 'True' else 0
        elif value in ['print', 'input', 'goto', 'int', 'bool', 'float', 'not']:  # commands
            self.type = 'command'
            self.value = value
        elif value in ['while', 'if']:  # condition
            self.type = 'condition'
            self.value = value
        elif str(value).isalpha():  # variable
            self.type = str
            self.name = str(value)
            self.type_data = None
            self.value = None
        elif str(value).count('.') == 1 and str(value).replace('-', '').replace('.', '').isdigit() or type(value) is float:  # float
            self.type = float
            self.value = float(value)

    def __setattr__(self, key, value) -> None:
        if key == 'value' and self.type is str and not (value is None):
            if self.type_data == value.type:
                super().__setattr__(key, value.value)
            elif value.type is str:
                if self.type_data == value.type_data:
                    super().__setattr__(key, value.value)
                else:
                    raise ValueError('type of variable and data must be the same')
            else:
                raise ValueError('type of variable and data must be the same')
        else:
            super().__setattr__(key, value)

    def eval(self, *obj):
        if self.type == 'command':
            obj = obj[0]
            if self.value == 'input':
                obj.value = Prn_Object(input())
            elif self.value == 'print':
                print(obj.value)
            elif self.value == 'int':
                obj.type_data = int
            elif self.value == 'float':
                obj.type_data = float
            elif self.value == 'bool':
                obj.type_data = bool
            elif self.value == 'not':
                return Prn_Object(not obj.value)
        elif self.type == 'operation':  # ['*', '/', '%', '//', 'and', '+', '-', 'or', '>', '<', '=', '!=', ':=']
            a, b = obj[1], obj[0]
            at, bt = a.type, b.type
            atd, btd = None, None
            if at == str:
                atd = a.type_data
            if bt == str:
                btd = b.type_data
            a, b = a.value, b.value
            op = self.value
            if a is None:
                raise ValueError(f'variable {obj[1].name} is not assigned a value')
            if b is None and op != ':=':
                raise ValueError(f'variable {obj[0].name} is not assigned a value')
            if ((at == bt or at == btd) and at is bool) or ((atd == bt or atd == btd) and atd is bool):
                if op in ['and', '*']:
                    return Prn_Object(bool(a * b))
                elif op in ['or', '+']:
                    return Prn_Object(bool(a + b))
                elif op == '=':
                    return Prn_Object(a == b)
                elif op == ':=':
                    obj[0].value = obj[1]
                    return None
            elif (btd == atd or btd == at) and op == ':=':
                obj[0].value = obj[1]
                return None
            elif (at in [int, float] and bt in [int, float]) or (atd in [int, float] and btd in [int, float]) or (at in [int, float] and btd in [int, float]) or (atd in [int, float] and bt in [int, float]):
                if op == '*':
                    return Prn_Object(a * b)
                elif op == '**':
                    return Prn_Object(a ** b)
                elif op == '/':
                    return Prn_Object(a / b)
                elif op == '%':
                    return Prn_Object(a % b)
                elif op == '//':
                    return Prn_Object(a // b)
                elif op == '+':
                    return Prn_Object(a + b)
                elif op == '-':
                    return Prn_Object(a - b)
                elif op == '>':
                    return Prn_Object(a > b)
                elif op == '<':
                    return Prn_Object(a < b)
                elif op == '=':
                    return Prn_Object(a == b)
                elif op == '!=':
                    return Prn_Object(a != b)
                elif op == ':=':
                    obj[0].value = obj[1]
                    return None
            raise ValueError(f'invalid operation {op} for {atd if at is str else at} and {btd if bt is str else bt}')
