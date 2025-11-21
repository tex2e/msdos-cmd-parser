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
    def test_if_eq_doublequote(self):
        inputfile_text = """
IF "A %MY_VARIABLE:~-1% A" == "A \\ A" SET MY_VARIABLE=%MY_VARIABLE:~0,-1%
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "A %MY_VARIABLE:~-1% A"
      ==
      "A \\ A"
    command_set
      SET
      MY_VARIABLE
      =
      %MY_VARIABLE:~0,-1%
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_not_eq_doublequote(self):
        inputfile_text = """
IF NOT "%ERRORLEVEL%" == "0" (
    goto END
)
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
    group
      (
      subprogram
        command_goto
          goto
          END
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_left_normal_right_quoted(self):
        inputfile_text = """
IF NOT %FLAG% == "1" GOTO LABEL_END
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_not_comp
      NOT
      %FLAG%
      ==
      "1"
    command_goto
      GOTO
      LABEL_END
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_left_quoted_right_normal(self):
        inputfile_text = """
IF NOT "1" == %FLAG% GOTO LABEL_END
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_not_comp
      NOT
      "1"
      ==
      %FLAG%
    command_goto
      GOTO
      LABEL_END
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_compare_value_has_colon(self):
        inputfile_text = """
IF %1:%2=="SYSTEMID":1 SET LOGIN_USER=user123
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %1:%2
      ==
      "SYSTEMID":1
    command_set
      SET
      LOGIN_USER
      =
      user123
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_compare_value_has_space(self):
        inputfile_text = """
IF %1:%2=="SYSTEMID SPACE":1 SET LOGIN_USER=user123
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %1:%2
      ==
      "SYSTEMID SPACE":1
    command_set
      SET
      LOGIN_USER
      =
      user123
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_equ(self):
        inputfile_text = """
IF %~5 EQU 1 echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %~5
      EQU
      1
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_lss(self):
        inputfile_text = """
IF %~5 lss 1 echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %~5
      lss
      1
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_gtr_with_variable_substring(self):
        inputfile_text = """
echo %TMP1_TARGETDATE:~0,8% GTR %TMP3_TARGETDATE:~0,8% >> %OUTPUT_LOG% 2>&1

IF %TMP1_TARGETDATE:~0,8% GTR %MY_YY%%MY_MM%%MY_DD% (
    SET MY_VARIABLE=%TMP3_TARGETDATE:~0,8%
    echo テスト（%MY_VARIABLE%） >> %OUTPUT_LOG% 2>&1
    goto :RUN_DELETE
)
"""
        expected_parse_tree = """
program
  command_oneline
    command_echo
      echo
      %TMP1_TARGETDATE:~0,8% GTR %TMP3_TARGETDATE:~0,8% 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
  emptyline	
  statement_if
    IF
    test_comp
      %TMP1_TARGETDATE:~0,8%
      GTR
      %MY_YY%%MY_MM%%MY_DD%
    group
      (
      subprogram
        command_set
          SET
          MY_VARIABLE
          =
          %TMP3_TARGETDATE:~0,8%
        subcommand_oneline
          command_echo
            echo
            テスト（%MY_VARIABLE%） 
          redirect_stdout
            >>
            %OUTPUT_LOG%
          redirect_stderr
            2>
            &1
        command_goto
          goto
          :
          RUN_DELETE
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_exist(self):
        inputfile_text = """
IF EXIST c:\\path\\to\\my.exe set flag=true
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_exist
      EXIST
      c:\\path\\to\\my.exe
    command_set
      set
      flag
      =
      true
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_exist_expand_var(self):
        inputfile_text = """
IF EXIST %~dp0..\\bin\\MYCOMMAND.exe (
    SET SAMPLE=%~dp0..\\bin\\MYCOMMAND.exe
    GOTO L_SAMPLE_END
)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_exist
      EXIST
      %~dp0..\\bin\\MYCOMMAND.exe
    group
      (
      subprogram
        command_set
          SET
          SAMPLE
          =
          %~dp0..\\bin\\MYCOMMAND.exe
        command_goto
          GOTO
          L_SAMPLE_END
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_not_exist(self):
        inputfile_text = """
if not exist "d:\\path\\to\\Program Files\\my.exe" set flag=true
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_not_exist
      not
      exist
      "d:\\path\\to\\Program Files\\my.exe"
    command_set
      set
      flag
      =
      true
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_group(self):
        inputfile_text = """
IF NOT "%ERRORLEVEL%" == "0" (
    GOTO L_ERR
)  
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
    group
      (
      subprogram
        command_goto
          GOTO
          L_ERR
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_multiple_commands(self):
        inputfile_text = """
IF "%MY_FLAG%" == "1" (
    REM * SAMPLE *
    SET DIR1=%MY_ROOT_DIR%\\SAMPLE
    SET DIR2=%MY_ROOT_DIR%\\Current
) else (
    REM noop
    SET FLAG=1
)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "1"
    group
      (
      subprogram
        command_rem
          REM
          * SAMPLE *
        command_set
          SET
          DIR1
          =
          %MY_ROOT_DIR%\\SAMPLE
        command_set
          SET
          DIR2
          =
          %MY_ROOT_DIR%\\Current
      )
    statement_else
      else
      group
        (
        subprogram
          command_rem
            REM
            noop
          command_set
            SET
            FLAG
            =
            1
        )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_not_else_command_with_redirect(self):
        inputfile_text = """
IF NOT ""%MY_FLAG%""=="\"\"" (%MYDIR%\\MYCALL %MYDIR%\\MYCOMMAND ARG100 >> %OUTPUT_LOG% 2>&1
)ELSE (%MYDIR%\\MYCALL %MYDIR%\\MYCOMMAND ARG200 >> %OUTPUT_LOG% 2>&1)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_not_comp
      NOT
      ""%MY_FLAG%""
      ==
      "\"\""
    group
      (
      subprogram
        subcommand_oneline
          command_exe
            %MYDIR%\\MYCALL
            %MYDIR%\\MYCOMMAND ARG100 
          redirect_stdout
            >>
            %OUTPUT_LOG%
          redirect_stderr
            2>
            &1
      )
    statement_else
      ELSE
      group
        (
        subprogram
          subcommand_oneline
            command_exe
              %MYDIR%\\MYCALL
              %MYDIR%\\MYCOMMAND ARG200 
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
    def test_if_else_if_else_normal(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" (
    GOTO LABEL_PROCESS1
) ELSE IF "%MY_FLAG%" == "1" (
    GOTO LABEL_PROCESS1
) ELSE (
    GOTO LABEL_PROCESS2
) 
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        command_goto
          GOTO
          LABEL_PROCESS1
      )
    statement_else
      ELSE
      statement_if
        IF
        test_comp
          "%MY_FLAG%"
          ==
          "1"
        group
          (
          subprogram
            command_goto
              GOTO
              LABEL_PROCESS1
          )
        statement_else
          ELSE
          group
            (
            subprogram
              command_goto
                GOTO
                LABEL_PROCESS2
            )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_if_else_slim_threelines_goto(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" (GOTO LABEL_PROCESS1
) ELSE IF "%MY_FLAG%" == "1" (GOTO LABEL_PROCESS1
) ELSE (GOTO LABEL_PROCESS2)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        command_goto
          GOTO
          LABEL_PROCESS1
      )
    statement_else
      ELSE
      statement_if
        IF
        test_comp
          "%MY_FLAG%"
          ==
          "1"
        group
          (
          subprogram
            command_goto
              GOTO
              LABEL_PROCESS1
          )
        statement_else
          ELSE
          group
            (
            subprogram
              command_goto
                GOTO
                LABEL_PROCESS2
            )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_if_else_slim_threelines_command_exe(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" (MYCALL LABEL_PROCESS1
) ELSE IF "%MY_FLAG%" == "1" (MYCALL LABEL_PROCESS1
) ELSE (MYCALL LABEL_PROCESS2)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        command_exe
          MYCALL
          LABEL_PROCESS1
      )
    statement_else
      ELSE
      statement_if
        IF
        test_comp
          "%MY_FLAG%"
          ==
          "1"
        group
          (
          subprogram
            command_exe
              MYCALL
              LABEL_PROCESS1
          )
        statement_else
          ELSE
          group
            (
            subprogram
              command_exe
                MYCALL
                LABEL_PROCESS2
            )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_if_else_slim_threelines_command_exe_redirect(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" (MYCALL LABEL_PROCESS1 >> %OUTPUT_LOG% 2>&1
) ELSE IF "%MY_FLAG%" == "1" (MYCALL LABEL_PROCESS1 >> %OUTPUT_LOG% 2>&1
) ELSE (MYCALL LABEL_PROCESS2 >> %OUTPUT_LOG% 2>&1)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        subcommand_oneline
          command_exe
            MYCALL
            LABEL_PROCESS1 
          redirect_stdout
            >>
            %OUTPUT_LOG%
          redirect_stderr
            2>
            &1
      )
    statement_else
      ELSE
      statement_if
        IF
        test_comp
          "%MY_FLAG%"
          ==
          "1"
        group
          (
          subprogram
            subcommand_oneline
              command_exe
                MYCALL
                LABEL_PROCESS1 
              redirect_stdout
                >>
                %OUTPUT_LOG%
              redirect_stderr
                2>
                &1
          )
        statement_else
          ELSE
          group
            (
            subprogram
              subcommand_oneline
                command_exe
                  MYCALL
                  LABEL_PROCESS2 
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
    def test_if_else_if_else_slim_oneline(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" (GOTO LABEL_PROCESS1) ELSE IF "%MY_FLAG%" == "1" (GOTO LABEL_PROCESS1) ELSE (GOTO LABEL_PROCESS2) 
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        command_goto
          GOTO
          LABEL_PROCESS1
      )
    statement_else
      ELSE
      statement_if
        IF
        test_comp
          "%MY_FLAG%"
          ==
          "1"
        group
          (
          subprogram
            command_goto
              GOTO
              LABEL_PROCESS1
          )
        statement_else
          ELSE
          group
            (
            subprogram
              command_goto
                GOTO
                LABEL_PROCESS2
            )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_if_else_slim_oneline_with_spaces(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" ( GOTO LABEL_PROCESS1 ) ELSE IF "%MY_FLAG%" == "1" ( GOTO LABEL_PROCESS1 ) ELSE ( GOTO LABEL_PROCESS2 )
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        command_goto
          GOTO
          LABEL_PROCESS1
      )
    statement_else
      ELSE
      statement_if
        IF
        test_comp
          "%MY_FLAG%"
          ==
          "1"
        group
          (
          subprogram
            command_goto
              GOTO
              LABEL_PROCESS1
          )
        statement_else
          ELSE
          group
            (
            subprogram
              command_goto
                GOTO
                LABEL_PROCESS2
            )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_nested_if(self):
        inputfile_text = """
IF "%I%" == "1" (
    IF "%J%" == "2" (
        echo OK
    )
)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%I%"
      ==
      "1"
    group
      (
      subprogram
        statement_if
          IF
          test_comp
            "%J%"
            ==
            "2"
          group
            (
            subprogram
              command_echo
                echo
                OK
            )
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_command_oneline(self):
        inputfile_text = """
IF NOT "%ERRORLEVEL%"=="0" %MYDIR%\\MYCALL %MYDIR%\\MYCOMMAND ERROR -n 0 >> %OUTPUT_LOG%
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
    command_oneline
      command_exe
        %MYDIR%\\MYCALL
        %MYDIR%\\MYCOMMAND ERROR -n 0 
      redirect_stdout
        >>
        %OUTPUT_LOG%
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_command_oneline_else(self):
        inputfile_text = """
IF /I "%INPUT%" == "N" (GOTO L_CANCEL) ELSE GOTO L_CHECK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      /I
      "%INPUT%"
      ==
      "N"
    group
      (
      subprogram
        command_goto
          GOTO
          L_CANCEL
      )
    statement_else
      ELSE
      command_goto
        GOTO
        L_CHECK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_else_set_in_paren(self):
        inputfile_text = """
IF "%MY_FLAG%" == "0" (SET CONFIG=01.2) ELSE (SET CONFIG=71.2)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MY_FLAG%"
      ==
      "0"
    group
      (
      subprogram
        command_set
          SET
          CONFIG
          =
          01.2
      )
    statement_else
      ELSE
      group
        (
        subprogram
          command_set
            SET
            CONFIG
            =
            71.2
        )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_doublequote4(self):
        inputfile_text = """
IF "%MYFLAG%" == "\"\"" echo ok
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      "%MYFLAG%"
      ==
      "\"\""
    command_echo
      echo
      ok
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_left_variable_replace(self):
        inputfile_text = """
IF %NUMBER:"='% == 123 echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %NUMBER:"='%
      ==
      123
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_right_variable_replace(self):
        inputfile_text = """
IF 123 == %NUMBER:"='% echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      123
      ==
      %NUMBER:"='%
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_left_variable_substr_start_only(self):
        inputfile_text = """
IF %NUMBER:~6% == 123 echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %NUMBER:~6%
      ==
      123
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_right_variable_substr_start_only(self):
        inputfile_text = """
IF 123 == %NUMBER:~6% echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      123
      ==
      %NUMBER:~6%
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_left_variable_substr_plus_range(self):
        inputfile_text = """
IF %NUMBER:~6,4% == 123 echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %NUMBER:~6,4%
      ==
      123
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_right_variable_substr_plus_range(self):
        inputfile_text = """
IF 123 == %NUMBER:~6,4% echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      123
      ==
      %NUMBER:~6,4%
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_left_variable_substr_minus(self):
        inputfile_text = """
IF %NUMBER~-8,-4% == 123 echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %NUMBER~-8,-4%
      ==
      123
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_right_variable_substr_minus(self):
        inputfile_text = """
IF 123 == %NUMBER~-8,-4% echo OK
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      123
      ==
      %NUMBER~-8,-4%
    command_echo
      echo
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_i_option(self):
        inputfile_text = """
if /I {%1}=={out} SET RETRY_FLAG=1
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_comp
      /I
      {%1}
      ==
      {out}
    command_set
      SET
      RETRY_FLAG
      =
      1
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_defined(self):
        inputfile_text = """
if defined VAL goto OK
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_defined
      defined
      VAL
    command_goto
      goto
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_defined_arg(self):
        inputfile_text = """
if defined %3 goto OK
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_defined
      defined
      %3
    command_goto
      goto
      OK
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_not_defined_arg(self):
        inputfile_text = """
IF NOT DEFINED %3 (
	echo ok
)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_not_defined
      NOT
      DEFINED
      %3
    group
      (
      subprogram
        command_echo
          echo
          ok
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_errorlevel(self):
        inputfile_text = """
if errorlevel 1 goto ONE
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_errorlevel
      errorlevel
      1
    command_goto
      goto
      ONE
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_errorlevel_0(self):
        inputfile_text = """
if errorlevel 0 goto ONE
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_errorlevel
      errorlevel
      0
    command_goto
      goto
      ONE
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_errorlevel_minus1(self):
        inputfile_text = """
if errorlevel -1 goto ONE
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_errorlevel
      errorlevel
      -1
    command_goto
      goto
      ONE
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_errorlevel_0(self):
        inputfile_text = """
if not errorlevel 0 goto ONE
"""
        expected_parse_tree = """
program
  statement_if
    if
    test_not_errorlevel
      not
      errorlevel
      0
    command_goto
      goto
      ONE
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_command_exe_in_paren(self):
        inputfile_text = """
IF NOT EXIST %TARGET_PATH% (mkdir %TARGET_PATH%)
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_not_exist
      NOT
      EXIST
      %TARGET_PATH%
    group
      (
      subprogram
        command_exe
          mkdir
          %TARGET_PATH%
      )
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)

    # ------------------------------------------------------------------------
    def test_if_variable_replacement_match(self):
        # IF文の条件に「%=」が含まれていることで文字列置換として判断されたときにエラーしたため追加
        inputfile_text = """
IF %ERRORLEVEL%==0 (
    for /f "delims=" %%i IN ('..\\Bin\\Custom.exe /E:%CONFIGPATH%') DO SET KEEPDAYS=%%i >> %OUTPUT_LOG% 2>&1
) else (
    SET KEEPDAYS=%KEEPDAYS_DEF%
    echo %KEEPDAYS_DEF% >> %OUTPUT_LOG% 2>&1
    echo DEBUG LOG >> %OUTPUT_LOG% 2>&1
)
echo −−−−−−−−−② >> %OUTPUT_LOG% 2>&1

REM TMP1_TARGETDATE
@SET TMP1_TARGETDATE=
@rem 2025/06/11 This is a comment
IF "%LASTDATE%"=="" goto :L_TMP2
"""
        expected_parse_tree = """
program
  statement_if
    IF
    test_comp
      %ERRORLEVEL%
      ==
      0
    group
      (
      subprogram
        statement_for_f
          for
          /f
          "delims="
          for_parameter
            %%
            i
          IN
          (
          for_range_command	'..\\Bin\\Custom.exe /E:%CONFIGPATH%'
          )
          DO
          command_oneline
            command_set
              SET
              KEEPDAYS
              =
              %%i 
            redirect_stdout
              >>
              %OUTPUT_LOG%
            redirect_stderr
              2>
              &1
      )
    statement_else
      else
      group
        (
        subprogram
          command_set
            SET
            KEEPDAYS
            =
            %KEEPDAYS_DEF%
          subcommand_oneline
            command_echo
              echo
              %KEEPDAYS_DEF% 
            redirect_stdout
              >>
              %OUTPUT_LOG%
            redirect_stderr
              2>
              &1
          subcommand_oneline
            command_echo
              echo
              DEBUG LOG 
            redirect_stdout
              >>
              %OUTPUT_LOG%
            redirect_stderr
              2>
              &1
        )
  command_oneline
    command_echo
      echo
      −−−−−−−−−② 
    redirect_stdout
      >>
      %OUTPUT_LOG%
    redirect_stderr
      2>
      &1
  emptyline	
  command_rem
    REM
    TMP1_TARGETDATE
  command_set
    SET
    TMP1_TARGETDATE
    =
  command_rem
    rem
    2025/06/11 This is a comment
  statement_if
    IF
    test_comp
      "%LASTDATE%"
      ==
      ""
    command_goto
      goto
      :
      L_TMP2
""".strip("\n")
        pretty_print = self.parser.parse(inputfile_text).pretty()
        pretty_print = format_lark_pretty_print(pretty_print)
        self.assertEqual(pretty_print, expected_parse_tree)



