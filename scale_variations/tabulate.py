
from __future__ import print_function
from textwrap import dedent
from config import DEFAULT_COLUMN_WIDTH

USE_CSV = False

def add_hline():
    if not USE_CSV:
        print("\\hline")

def print_header(name, n_columns):
    if not USE_CSV:
        print(dedent("""
        """+name+"""
        ----------

        \\begin{table}
        \\tiny
        \\begin{tabular}{"""+(n_columns*"l")+"""}
        \\hline"""))

def print_footer():
    if not USE_CSV:
        print(dedent("""\
        \\hline
        \\end{tabular}
        \\end{table}

        """))

def print_table_cell(content, is_last=False, width=DEFAULT_COLUMN_WIDTH, fmt=""):
    if USE_CSV:
        delimiter = "" if is_last else ","
        to_print = ("{:"+fmt+"}{}").format(content, delimiter)
    else:
        delimiter = "\\\\" if is_last else "&"
        to_print = (" {:<"+str(width)+fmt+"} {} ").format(content, delimiter)
    if is_last:
        print(to_print)
    else:
        print(to_print, end="")
    # reset default values
    width=DEFAULT_COLUMN_WIDTH
    fmt=""
    is_last=False


