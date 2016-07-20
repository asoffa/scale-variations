#!/usr/bin/env python

import samples
import yields
import ROOT
from tabulate import Tabulator
from regions import SRs, SRs_reco
from config import USE_SAMPLE_GROUPS, SAMPLE_GROUPS, SAMPLES, LUMI_TO_SCALE_TO
from argparse import ArgumentParser

ROOT.gErrorIgnoreLevel = ROOT.kError

#-------------------------------------------------------------------------------

def main(sample_set, csv=False, print_to_file=False, percent_diff=False):
    if USE_SAMPLE_GROUPS:
        sample_dict = samples.get_sample_group_dict(sample_set)
    else:
        sample_dict = samples.get_sample_dict(sample_set)
    #samples.print_sample_dict(sample_dict)

    output_name = sample_set if print_to_file else None # .txt added automatically
    with Tabulator(output_name) as tab:
        if csv:
            #tab.USE_CSV = True
            tab.use_csv = True
        #if print_to_file:
        #    #tab.PRINT_TO_FILE = True
        tab.print_header(sample_set, len(SRs) + 1)
        tab.print_table_cell(""),

        for sr_name in SRs.keys():
            is_last = (sr_name == next(reversed(SRs)))
            tab.print_table_cell(sr_name, is_last=is_last),
        tab.add_hline()

        for name, s in sample_dict.iteritems():
            tab.print_table_cell(name.replace("_", "\\_")),

            is_reco = s[0].is_reco if USE_SAMPLE_GROUPS else s.is_reco
            sr_dict = SRs_reco if is_reco else SRs

            for sr_name, sr_cut in sr_dict.iteritems():
                is_last = (sr_name == next(reversed(sr_dict)))
                if not percent_diff:
                    if USE_SAMPLE_GROUPS:
                        sr_yield = yields.get_group_yield(s, sr_cut)
                    else:
                        sr_yield = yields.get_single_yield(s, sr_cut)
                else:
                    nominal_dict = samples.get_nominal_dict(sample_set)
                    if USE_SAMPLE_GROUPS:
                        sr_yield = yields.get_group_percent_diff(s, sr_cut, nominal_dict)
                    else:
                        sr_yield = yields.get_single_percent_diff(s, sr_cut, nominal_dict)
                if csv:
                    table_entry = sr_yield.csv_entry()
                else:
                    table_entry = sr_yield.latex_entry()
                tab.print_table_cell(table_entry, is_last=is_last),

        tab.print_footer()


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = ArgumentParser()
    #parser.add_argument("-r", "--raw-yields", action="store_true", help="report raw yields instead of weighted")
    #parser.add_argument("-u", "--uncertainties-only", action="store_true", help="report uncertainties only")
    #parser.add_argument("-s", "--scale-factors", action="store_true", help="print scale factors instead of yields")
    parser.add_argument("-c", "--csv", action="store_true", help="use CSV format instead of LaTeX")
    parser.add_argument("-f", "--file-output", action="store_true", help="print output to .tex files (or .csv files if --csv is used) instead of to STDOUT")
    parser.add_argument("-p", "--percent-diff", action="store_true", help="report percent difference from nominal sample instead of yields")
    args = parser.parse_args()

    if USE_SAMPLE_GROUPS:
        for s in SAMPLE_GROUPS:
            main(s, csv=args.csv, print_to_file=args.file_output, percent_diff=args.percent_diff)
    else:
        for s in SAMPLES:
            main(s, csv=args.csv, print_to_file=args.file_output, percent_diff=args.percent_diff)

