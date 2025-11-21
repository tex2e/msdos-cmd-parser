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
    def test_for_f_file(self):
        inputfile_text = """
for /f %%p in (%FILEPATH%) do CALL :SUBROUTINE %%p
"""
        expected_parse_tree = """
program
  statement_for_f
    for
    /f
    for_parameter
      %%
      p
    in
    (
    for_range_filename	%FILEPATH%
    )
    do
    command_call_label
      CALL
      label
        :
        SUBROUTINE
      %%p
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_for_f_command(self):
        inputfile_text = """
FOR /F "delims= " %%i IN ('DATE /T') DO SET YMD=%%i
"""
        expected_parse_tree = """
program
  statement_for_f
    FOR
    /F
    "delims= "
    for_parameter
      %%
      i
    IN
    (
    for_range_command	'DATE /T'
    )
    DO
    command_set
      SET
      YMD
      =
      %%i
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_for_f_empty_option(self):
        inputfile_text = """
FOR /F "" %%i IN (%O1%) DO SET NY_DATETIME=%%i
"""
        expected_parse_tree = """
program
  statement_for_f
    FOR
    /F
    ""
    for_parameter
      %%
      i
    IN
    (
    for_range_filename	%O1%
    )
    DO
    command_set
      SET
      NY_DATETIME
      =
      %%i
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_for_f_for_f_command(self):
        inputfile_text = """
FOR /F "delims= " %%i IN ("1 2 3") DO (
    FOR /F "delims= " %%i IN ("4 5 6") DO (
        echo %%i %%j
    )
)
"""
        expected_parse_tree = """
program
  statement_for_f
    FOR
    /F
    "delims= "
    for_parameter
      %%
      i
    IN
    (
    for_range_text	"1 2 3"
    )
    DO
    group
      (
      subprogram
        statement_for_f
          FOR
          /F
          "delims= "
          for_parameter
            %%
            i
          IN
          (
          for_range_text	"4 5 6"
          )
          DO
          group
            (
            subprogram
              command_echo
                echo
                %%i %%j
            )
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_for_f_for_f_oneline_command(self):
        inputfile_text = """
FOR /F "delims= " %%i IN ("1 2 3") DO FOR /F "delims= " %%i IN ("4 5 6") DO echo %%i %%j
"""
        expected_parse_tree = """
program
  statement_for_f
    FOR
    /F
    "delims= "
    for_parameter
      %%
      i
    IN
    (
    for_range_text	"1 2 3"
    )
    DO
    statement_for_f
      FOR
      /F
      "delims= "
      for_parameter
        %%
        i
      IN
      (
      for_range_text	"4 5 6"
      )
      DO
      command_echo
        echo
        %%i %%j
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_for_f_number_parameter(self):
        inputfile_text = """
FOR /f "delims=" %%1 IN ('CALL %MYDIR%\\MYCOMMAND Input.xml /param -t E') DO SET FILENAME=%%1
"""
        expected_parse_tree = """
program
  statement_for_f
    FOR
    /f
    "delims="
    for_parameter
      %%
      1
    IN
    (
    for_range_command	'CALL %MYDIR%\\MYCOMMAND Input.xml /param -t E'
    )
    DO
    command_set
      SET
      FILENAME
      =
      %%1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)


