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
    def test_exe(self):
        inputfile_text = """
%cmdline%	>%MYLOGFILE% 2>&1
"""
        expected_parse_tree = """
program
  command_oneline
    command_exe
      %cmdline%
    redirect_stdout
      >
      %MYLOGFILE%
    redirect_stderr
      2>
      &1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_exe_with_args_lt_gt(self):
        inputfile_text = """
@osql.exe -o %OUTPUTFILE% -s , -w 1024 -h-1 -d %MY_DB% -S %MY_DBSVR% -U %MY_DBUSER% -P %MY_DBPWD% -Q "SELECT TOP 1 * from MYTABLE where COL1 <> '' order by COL1"
"""
        expected_parse_tree = """
program
  command_exe
    osql.exe
    -o %OUTPUTFILE% -s , -w 1024 -h-1 -d %MY_DB% -S %MY_DBSVR% -U %MY_DBUSER% -P %MY_DBPWD% -Q "SELECT TOP 1 * from MYTABLE where COL1 <> '' order by COL1"
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_exe_with_args_paren(self):
        inputfile_text = """
%MYDIR%\\MYCALL %MYDIR%\\MYCOMMAND TESTMESSAGE(C1010.CMD) ERROR >> %OUTPUT_LOG%
"""
        expected_parse_tree = """
program
  command_oneline
    command_exe
      %MYDIR%\\MYCALL
      %MYDIR%\\MYCOMMAND TESTMESSAGE(C1010.CMD) ERROR 
    redirect_stdout
      >>
      %OUTPUT_LOG%
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_exe_with_args_paren_pair_in_subprogram(self):
        inputfile_text = """
IF 1 == 1 (
  %MYDIR%\\MYCALL %MYDIR%\\MYCOMMAND TESTMESSAGE(C1010.CMD) ERROR >> %OUTPUT_LOG%
)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      1
      ==
      1
    group
      (
      subprogram
        subcommand_oneline
          command_exe
            %MYDIR%\\MYCALL
            %MYDIR%\\MYCOMMAND TESTMESSAGE(C1010.CMD) ERROR 
          redirect_stdout
            >>
            %OUTPUT_LOG%
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_exe_with_args_paren_only_open_in_subprogram(self):
        inputfile_text = """
IF 1 == 1 (
  %MYDIR%\\MYCALL %MYDIR%\\MYCOMMAND TESTMESSAGE(C1010.CMD ERROR >> %OUTPUT_LOG%
)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      1
      ==
      1
    group
      (
      subprogram
        subcommand_oneline
          command_exe
            %MYDIR%\\MYCALL
            %MYDIR%\\MYCOMMAND TESTMESSAGE(C1010.CMD ERROR 
          redirect_stdout
            >>
            %OUTPUT_LOG%
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

