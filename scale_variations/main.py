#!/usr/bin/env python

import samples
import yields
import ROOT
from argparse import ArgumentParser
from tabulate import Tabulator
from regions import get_SRs, get_reco_SRs
from samples import get_base_name
from config import USE_SAMPLE_GROUPS, SAMPLE_GROUPS, SAMPLES, LUMI_TO_SCALE_TO

ROOT.gErrorIgnoreLevel = ROOT.kError

#-------------------------------------------------------------------------------

def main(sample_set, csv=False, print_to_file=False, percent_diff=False, verbose=False, rpv=False, sr0b2_j25=False):
    if USE_SAMPLE_GROUPS:
        sample_dict = samples.get_sample_group_dict(sample_set, verbose=verbose)
    else:
        sample_dict = samples.get_sample_dict(sample_set, verbose=verbose)
    #samples.print_sample_dict(sample_dict)

    output_name = sample_set if print_to_file else None # .txt added automatically
    with Tabulator(output_name) as tab:
        if csv:
            tab.use_csv = True

        SRs = get_SRs(rpv=rpv, sr0b2_j25=sr0b2_25)
        SRs_reco = get_reco_SRs(rpv=rpv, sr0b2_j25=sr0b2_25)
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
                    basename = get_base_name(name)
                    nominal_sample = sample_dict[basename+"_nom"]
                    if USE_SAMPLE_GROUPS:
                        sr_yield = yields.get_group_percent_diff(s, nominal_sample, sr_cut)
                    else:
                        sr_yield = yields.get_single_percent_diff(s, nominal_sample, sr_cut)
                if csv:
                    table_entry = sr_yield.csv_entry()
                else:
                    table_entry = sr_yield.latex_entry()
                tab.print_table_cell(table_entry, is_last=is_last),

        tab.print_footer()


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = ArgumentParser()

    # output options
    parser.add_argument("-c", "--csv", action="store_true", help="use CSV format instead of LaTeX")
    parser.add_argument("-f", "--file-output", action="store_true", help="print output to .tex files (or .csv files if --csv is used) instead of to STDOUT")
    parser.add_argument("-p", "--percent-diff", action="store_true", help="report percent difference from nominal sample instead of yields")
    parser.add_argument("-v", "--verbose", action="store_true", help="print additional diagnostic information")

    # selection options
    parser.add_argument("-r", "--rpv", action="store_true", help="use RPV signal regions")
    parser.add_argument("-s", "--sr0b2-j25", action="store_true", help="use SR0b2_j25 signal region")
    args = parser.parse_args()

    if USE_SAMPLE_GROUPS:
        for s in SAMPLE_GROUPS:
            main(s, csv=args.csv, print_to_file=args.file_output, percent_diff=args.percent_diff, verbose=args.verbose, rpv=args.rpv, sr0b2_j25=args.sr0b2_j25)
    else:
        for s in SAMPLES:
            main(s, csv=args.csv, print_to_file=args.file_output, percent_diff=args.percent_diff, verbose=args.verbose, rpv=args.rpv, sr0b2_j25=args.sr0b2_j25)

