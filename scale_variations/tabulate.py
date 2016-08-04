
# module for printing LaTeX or .csv tables

# primary functions to call
#   * print_header
#   * add_hline
#   * print_table_cell
#   * print_footer
#
#-------------------------------------------------------------------------------

from __future__ import print_function
import os
from textwrap import dedent
#from config import DEFAULT_COLUMN_WIDTH

class Tabulator:
    def __init__(self, output_name=None, use_csv=False):
        self.default_column_width = 30
        self.use_csv = use_csv
        if output_name:
            # ensure non-.tex/non-.csv files are never overwritten by mistake
            if use_csv and not output_name.endswith(".csv"):
                output_name = output_name+".csv"
            elif not output_name.endswith(".tex"):
                output_name = output_name+".tex"
            self.output_file = open(output_name, "w")
        else:
            self.output_file = None
        # reset default
        output_name=None
        use_csv=False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.output_file:
            print("\nOutput saved in {}".format(self.output_file.name))
            self.output_file.close()

    def println(self, line, end="\n"):
        print(line, end=end)
        if self.output_file:
            self.output_file.write(line + end)
        end="\n"

    def add_hline(self):
        if not self.use_csv:
            self.println("\\hline")
    
    def print_header(self, name, n_columns, label="", size="scriptsize"):
        if not self.use_csv:
            self.println(dedent("""
                \\begin{table}
                \\label{table:"""+name+"""}
                \\caption{"""+name+""".}
                \\"""+size+"""
                \\begin{tabular}{"""+(n_columns*"l")+"""}
                \\hline"""))
        label=""
        size="scriptsize"
    
    def print_footer(self):
        if not self.use_csv:
            self.println(dedent("""\
                \\hline
                \\end{tabular}
                \\end{table}
    
                """))
    
    def print_table_cell(self, content, is_last=False, width=None, fmt=""):
        if not width:
            width = self.default_column_width
        if self.use_csv:
            delimiter = "" if is_last else ","
            to_print = ("{:"+fmt+"}{}").format(content, delimiter)
        else:
            delimiter = "\\\\" if is_last else "&"
            to_print = (" {:<"+str(width)+fmt+"} {} ").format(content, delimiter)
        if is_last:
            self.println(to_print)
        else:
            self.println(to_print, end="")
        # reset default values
        width=None
        fmt=""
        is_last=False


