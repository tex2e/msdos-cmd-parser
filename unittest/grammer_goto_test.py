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
    def test_goto_label(self):
        inputfile_text = """
GOTO L_TEST123
"""
        expected_parse_tree = """
program
  command_goto
    GOTO
    L_TEST123
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_goto_label_with_space(self):
        inputfile_text = """
goto :L_GET_STATUS
"""
        expected_parse_tree = """
program
  command_goto
    goto
    :
    L_GET_STATUS
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_goto_label_with_plus(self):
        inputfile_text = """
GOTO LABLE+
"""
        expected_parse_tree = """
program
  command_goto
    GOTO
    LABLE+
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_goto_label_with_minus(self):
        inputfile_text = """
GOTO LABLE2-1AAA
"""
        expected_parse_tree = """
program
  command_goto
    GOTO
    LABLE2-1AAA
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)
