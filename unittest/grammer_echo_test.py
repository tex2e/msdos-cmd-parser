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
    def test_echo(self):
        inputfile_text = """
ECHO ---------- TEST TEXT ---------- >> %OUTPUT_LOG% 2>&1
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
      ---------- TEST TEXT ---------- 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_1_and_redirect(self):
        inputfile_text = """
ECHO  TEST  TEXT  1 >> %OUTPUT_LOG% 2>&1
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
       TEST  TEXT  1 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_paren(self):
        inputfile_text = """
ECHO  (TEST  TEXT)  1 >> %OUTPUT_LOG% 2>&1
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
       (TEST  TEXT)  1 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_only_open_paren(self):
        inputfile_text = """
ECHO  (TEST  TEXT  1 >> %OUTPUT_LOG% 2>&1
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
       (TEST  TEXT  1 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_only_close_paren(self):
        inputfile_text = """
ECHO  TEST  TEXT)  1 >> %OUTPUT_LOG% 2>&1
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
       TEST  TEXT)  1 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_nested_only_open_paren(self):
        inputfile_text = """
(
    ECHO  (TEST  TEXT  1 >> %OUTPUT_LOG% 2>&1
)
"""
        expected_parse_tree = """
program
  group
    (
    subprogram
      subcommand_oneline
        command_echo
          ECHO
           (TEST  TEXT  1 
        redirect_stdout
          >>
          %OUTPUT_LOG%
        redirect_stderr
          2>
          &1
    )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_escaped_redirect(self):
        inputfile_text = """
ECHO     ^<ClientId^>Your Name Here^</ClientId^> >>%MyFolder%\\Input.csv
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
          ^<ClientId^>Your Name Here^</ClientId^> 
    redirect_stdout
      >>
      %MyFolder%\\Input.csv
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_echo_dot(self):
        inputfile_text = """
ECHO. >> %OUTPUT_LOG%
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO.
    redirect_stdout
      >>
      %OUTPUT_LOG%
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_at_echo_off(self):
        inputfile_text = """
@ECHO OFF
"""
        expected_parse_tree = """
program
  command_echo
    ECHO
    OFF
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_single_echo(self):
        inputfile_text = """
ECHO
"""
        expected_parse_tree = """
program
  command_echo	ECHO
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)
