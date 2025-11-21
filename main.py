
# MSDOS command parser

import re
from lark import Lark  # pip install lark-parser regex

inputfilepath = "./sample/input.cmd"
grammarfilepath = "./grammar.lark"

# Load grammar
grammar_main = ""
with open(grammarfilepath, 'r', encoding='utf-8') as a_file:
    grammar_main = ''.join([line for line in a_file])

# Create parser
parser = Lark(grammar_main, parser='lalr', regex=True)


with open(inputfilepath, 'r', encoding='utf-8') as a_file:
    inputfile_text = a_file.read()

ast_tree = parser.parse(inputfile_text)
str_ast_tree = ast_tree.pretty()
str_ast_tree = '\n'.join(line for line in str_ast_tree.split("\n") if not re.match(r'^\s*$', line))

print(str_ast_tree)
