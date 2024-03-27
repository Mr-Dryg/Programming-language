import sys
from hexer import Hexer
from syntax import Parser
from prn_do import Prn

file = sys.argv[1]
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
