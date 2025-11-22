# MS-DOS Command Parser

A simple Python Program for parsing MS-DOS style command-line strings.

This library takes a command-line string as input and parses it into a command and a list of arguments, handling quotes and switches similar to how `cmd.exe` would.

## Features

*   Parses a command-line string into a command and arguments.
*   Correctly handles arguments enclosed in double quotes.

## Installation

```
pip install lark-parser regex
```

## Usage

```
python main.py
```

output example:

```
program
  command_set
    SET
    VARIABLE1
    =
    %~dp0
  statement_if
    IF
    test_comp
      "%VARIABLE1:~-1%"
      ==
      "\"
    command_set
      SET
      VARIABLE1
      =
      %VARIABLE1:~0,-1%
  emptyline
```
