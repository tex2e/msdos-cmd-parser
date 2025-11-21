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
    def test_redirect_new_stdout(self):
        inputfile_text = """
ECHO MY_VARIABLE=test > %MY_DIR%\\MY_COMMAND.cmd
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
      MY_VARIABLE=test 
    redirect_stdout
      >
      %MY_DIR%\\MY_COMMAND.cmd
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_new_stderr(self):
        inputfile_text = """
ECHO MY_VARIABLE=test 2> %MY_DIR%\\MY_COMMAND.cmd
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
      MY_VARIABLE=test 
    redirect_stderr
      2>
      %MY_DIR%\\MY_COMMAND.cmd
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_escaped_1(self):
        inputfile_text = """
ECHO SET MY_VARIABLE=^1>>%MY_DIR%\\MY_COMMAND.cmd
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      ECHO
      SET MY_VARIABLE=^1
    redirect_stdout
      >>
      %MY_DIR%\\MY_COMMAND.cmd
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_new_prefix(self):
        inputfile_text = """
> SAMPLE.CONFIG  echo set key1 32767
"""
        expected_parse_tree = """
program
  command_oneline
    redirect_stdout
      >
      SAMPLE.CONFIG
    command_echo
      echo
      set key1 32767
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_add_prefix(self):
        inputfile_text = """
>> SAMPLE.CONFIG echo set key2 0
"""
        expected_parse_tree = """
program
  command_oneline
    redirect_stdout
      >>
      SAMPLE.CONFIG
    command_echo
      echo
      set key2 0
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_pipeline_chain_command(self):
        inputfile_text = """
echo 123 && echo 456 || echo 789
"""
        expected_parse_tree = """
program
  command_line
    command_echo
      echo
      123 
    &&
    command_echo
      echo
      456 
    ||
    command_echo
      echo
      789
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_pipe_command(self):
        inputfile_text = """
echo aaa | echo bbb
"""
        expected_parse_tree = """
program
  pipeline
    command_echo
      echo
      aaa 
    |
    command_echo
      echo
      bbb
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_escaped_pipe(self):
        inputfile_text = """
echo aaa ^| echo bbb
"""
        expected_parse_tree = """
program
  command_echo
    echo
    aaa ^| echo bbb
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_pipe_findstr(self):
        inputfile_text = """
set | findstr ^%_ENVNAME_%= >nul 2>nul
"""
        expected_parse_tree = """
program
  pipeline
    command_set_disp
      set
    |
    command_oneline
      command_exe
        findstr
        ^%_ENVNAME_%= 
      redirect_stdout
        >
        nul
      redirect_stderr
        2>
        nul
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_redirect_pipe_if(self):
        inputfile_text = """
IF NOT "%ERRORLEVEL%"=="0" %MYDIR%\\MYCOMMAND ERROR %OUTPUT_LOG% -n 0 >> %OUTPUT_LOG% & GOTO END
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_not_comp
      NOT
      "%ERRORLEVEL%"
      ==
      "0"
    command_line
      command_oneline
        command_exe
          %MYDIR%\\MYCOMMAND
          ERROR %OUTPUT_LOG% -n 0 
        redirect_stdout
          >>
          %OUTPUT_LOG%
      &
      command_goto
        GOTO
        END
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

