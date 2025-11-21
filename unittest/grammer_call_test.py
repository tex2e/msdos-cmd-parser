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
    def test_call_file(self):
        inputfile_text = """
call %BIN_PATH%\\MyProcess2.cmd
"""
        expected_parse_tree = """
program
  command_call_file
    call
    %BIN_PATH%\\MyProcess2.cmd
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_call_file_with_args(self):
        inputfile_text = """
call %BIN_PATH%\\MyProcess2.cmd %_MyVariable% 1234
"""
        expected_parse_tree = """
program
  command_call_file
    call
    %BIN_PATH%\\MyProcess2.cmd
    %_MyVariable% 1234
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_call_label(self):
        inputfile_text = """
CALL :SUBROUTINE
"""
        expected_parse_tree = """
program
  command_call_label
    CALL
    label
      :
      SUBROUTINE
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_call_label_with_args(self):
        inputfile_text = """
CALL :SUBROUTINE %%i %%j %%k %%l %%m %%n
"""
        expected_parse_tree = """
program
  command_call_label
    CALL
    label
      :
      SUBROUTINE
    %%i %%j %%k %%l %%m %%n
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)
