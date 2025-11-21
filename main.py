
# MSDOS command parser

import re
from MsDosCommandParser import MsDosCommandParser

inputfilepath = "./sample/input.cmd"

with open(inputfilepath, 'r', encoding='utf-8') as a_file:
    inputfile_text = a_file.read()

# Create parser
parser = MsDosCommandParser().get_parser()
ast_tree = parser.parse(inputfile_text)
str_ast_tree = ast_tree.pretty()
str_ast_tree = '\n'.join(line for line in str_ast_tree.split("\n") if not re.match(r'^\s*$', line))

print(str_ast_tree)
