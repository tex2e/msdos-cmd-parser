# python -m unittest discover ./unittest "*_test.py"

import re
import unittest
from MsDosCommandParser import MsDosCommandParser

def format_lark_pretty_print(pretty_print):
    return '\n'.join(line for line in pretty_print.split("\n") if not re.match(r'^\s*$', line))

class MsDosCmdGrammerTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        transpiler = MsDosCommandParser()
        self.parser = transpiler.get_parser()

    # ------------------------------------------------------------------------
    def test_set_variable(self):
        inputfile_text = """
setlocal ENABLEDELAYEDEXPANSION
"""
        expected_parse_tree = """
program
  command_setlocal
    setlocal
    ENABLEDELAYEDEXPANSION
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)
