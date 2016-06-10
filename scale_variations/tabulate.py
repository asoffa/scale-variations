
from textwrap import dedent
from config import DEFAULT_COLUMN_WIDTH


def print_header(name, n_columns):
    print dedent("""
    """+name+"""
    ----------

    \\begin{table}
    \\tiny
    \\begin{tabular}{"""+(n_columns*"l")+"""}
    \\hline""")

def print_footer():
    print dedent("""\
    \\hline
    \\end{tabular}
    \\end{table}

    """)

def print_table_cell(content, is_last=False, width=DEFAULT_COLUMN_WIDTH, fmt=""):
    delimiter = "\\\\" if is_last else "&"
    to_print = (" {:<"+str(width)+fmt+"} {} ").format(content, delimiter)
    if is_last:
        print to_print
    else:
        print to_print,
    # reset default values
    width=DEFAULT_COLUMN_WIDTH
    fmt=""
    is_last=False


