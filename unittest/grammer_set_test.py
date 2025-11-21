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
SET MY_VARIABLE=%~dp0
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_VARIABLE
    =
    %~dp0
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_variable_expand_var(self):
        inputfile_text = """
SET %3=123
"""
        expected_parse_tree = """
program
  command_set
    SET
    %3
    =
    123
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_variable_value_expand_var(self):
        inputfile_text = """
SET MY_VARIABLE=%~dp0
echo TEST
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_VARIABLE
    =
    %~dp0
  command_echo
    echo
    TEST
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_variable_replace_doublequote(self):
        inputfile_text = """
IF DEFINED INPUT SET INPUT=%INPUT:"=%
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_defined
      DEFINED
      INPUT
    command_set
      SET
      INPUT
      =
      %INPUT:"=%
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_variable_single_doublequote(self):
        inputfile_text = """
SET arg1=%~1"
"""
        expected_parse_tree = """
program
  command_set
    SET
    arg1
    =
    %~1"
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_variable_surround_doublequote(self):
        inputfile_text = """
SET MY_QUERY="select S.*, '' from MYTABLE　as S where DELETE_FLG <> '1' and STARTYMD <= '%SYSTEMYMD%' and '%SYSTEMYMD%' <= ENDYMD order by COLUMN1, COLUMN2 desc;"
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_QUERY
    =
    "select S.*, '' from MYTABLE　as S where DELETE_FLG <> '1' and STARTYMD <= '%SYSTEMYMD%' and '%SYSTEMYMD%' <= ENDYMD order by COLUMN1, COLUMN2 desc;"
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_sql1(self):
        inputfile_text = """
SET MY_QUERY1="SELECT * FROM %MY_DB%..MYVIEW WHERE MYVIEW.COLUMN1='99999999' AND MYVIEW.COLUMN2='10' UNION ALL 
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_QUERY1
    =
    "SELECT * FROM %MY_DB%..MYVIEW WHERE MYVIEW.COLUMN1='99999999' AND MYVIEW.COLUMN2='10' UNION ALL 
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_sql2(self):
        inputfile_text = """
SET MY_QUERY2=SELECT * FROM %MY_DB%..MYVIEW WHERE MYVIEW.COLUMN1='99999999' AND (MYVIEW.COLUMN2='20' AND MYVIEW.COL3 IN ('0','1')) 
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_QUERY2
    =
    SELECT * FROM %MY_DB%..MYVIEW WHERE MYVIEW.COLUMN1='99999999' AND (MYVIEW.COLUMN2='20' AND MYVIEW.COL3 IN ('0','1')) 
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_sql3(self):
        inputfile_text = """
SET MY_QUERY3=ORDER BY CD1,CD2"
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_QUERY3
    =
    ORDER BY CD1,CD2"
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_open_paren_only(self):
        inputfile_text = """
SET MY_QUERY=%MY_QUERY% A.CD2 IN (
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_QUERY
    =
    %MY_QUERY% A.CD2 IN (
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_close_paren_only(self):
        inputfile_text = """
SET MY_QUERY=%MY_QUERY% )
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_QUERY
    =
    %MY_QUERY% )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_only_open_dquote(self):
        inputfile_text = """
set VARIABLE="select * from AAA where COL > 1 and COL < 10
"""
        expected_parse_tree = """
program
  command_set
    set
    VARIABLE
    =
    "select * from AAA where COL > 1 and COL < 10
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_with_redirect(self):
        inputfile_text = """
set VARIABLE="select * from AAA where COL > 1 and COL < 10" > %SQLFILE%
"""
        expected_parse_tree = """
program
  command_oneline
    command_set
      set
      VARIABLE
      =
      "select * from AAA where COL > 1 and COL < 10" 
    redirect_stdout
      >
      %SQLFILE%
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_1(self):
        inputfile_text = """
SET MY_FLG=1
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_FLG
    =
    1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_1_with_space(self):
        inputfile_text = """
SET MY_FLG = 1
"""
        expected_parse_tree = """
program
  command_set
    SET
    MY_FLG
    =
     1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_number(self):
        inputfile_text = """
set /a cno1=%2+1
"""
        expected_parse_tree = """
program
  command_set_expr
    set
    /a
    cno1
    =
    %2+1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_number_with_space(self):
        inputfile_text = """
SET /A RETRYCNT = RETRYCNT + 1
"""
        expected_parse_tree = """
program
  command_set_expr
    SET
    /A
    RETRYCNT
    =
     RETRYCNT + 1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_only_declared(self):
        inputfile_text = """
SET SQL >> ERR%CUSTOM_NO%.LOG
"""
        expected_parse_tree = """
program
  command_oneline
    command_set_disp
      SET
      SQL
    redirect_stdout
      >>
      ERR%CUSTOM_NO%.LOG
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_set_show_variables(self):
        inputfile_text = """
SET >> ERR%CUSTOM_NO%.LOG
"""
        expected_parse_tree = """
program
  command_oneline
    command_set_disp
      SET
    redirect_stdout
      >>
      ERR%CUSTOM_NO%.LOG
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)
