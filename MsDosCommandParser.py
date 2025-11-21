
from lark import Lark  # pip install lark-parser regex

class MsDosCommandParser:

    def get_parser(self):
        """Reads the grammar definition file and creates a parser."""

        # Load grammar
        grammar_main = ""
        with open('./grammar.lark', 'r', encoding='utf-8') as a_file:
            grammar_main = ''.join([line for line in a_file])

        # Create parser
        parser = Lark(grammar_main, parser='lalr', regex=True)
        return parser
