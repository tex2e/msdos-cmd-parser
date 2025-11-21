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
    def test_label(self):
        inputfile_text = """
:L_TEST123
"""
        expected_parse_tree = """
program
  label
    :
    L_TEST123
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_label_with_space(self):
        inputfile_text = """
:L_TEST	
"""
        expected_parse_tree = """
program
  label
    :
    L_TEST
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_label_with_plus(self):
        inputfile_text = """
:LABEL+
"""
        expected_parse_tree = """
program
  label
    :
    LABEL+
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_label_with_minus(self):
        inputfile_text = """
:LABEL1-2-3
"""
        expected_parse_tree = """
program
  label
    :
    LABEL1-2-3
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)
