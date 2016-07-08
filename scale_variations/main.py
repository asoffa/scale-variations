#!/usr/bin/env python

import samples
import tabulate as tab
import ROOT
from regions import SRs, SRs_reco
from config import USE_SAMPLE_GROUPS, SAMPLE_GROUPS, SAMPLES
from argparse import ArgumentParser

ROOT.gErrorIgnoreLevel = ROOT.kError

#-------------------------------------------------------------------------------

def main(sample_set, raw_yields=False, uncertainties_only=False, csv=False, print_scale_factors=False):
    if USE_SAMPLE_GROUPS and print_scale_factors:
        print "Subsamples that make up a group each have their own scale factor"
        print "  --> Disable 'USE_SAMPLE_GROUPS' to print scale factors"
        return
    if csv:
        tab.USE_CSV = True
    if USE_SAMPLE_GROUPS:
        sample_dict = samples.get_sample_groups(sample_set)
    else:
        sample_dict = samples.get_samples(sample_set)
        #samples.print_samples(sample_dict)

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
            if print_scale_factors:
                #table_entry = "${}$".format(s.scale_factor)
                table_entry = "${}$".format(s.lumi)
            else:
                if USE_SAMPLE_GROUPS:
                    sr_yield = samples.get_group_yield(s, sr_cut)
                else:
                    sr_yield = samples.get_single_yield(s, sr_cut)
                syield = sr_yield.n_entries if raw_yields else sr_yield.n_weighted
                if csv:
                    if uncertainties_only:
                        if syield == 0.:
                            table_entry = "indeterminate"
                        else:
                            table_entry = sr_yield.stat_err / syield * 100.
                    else:
                        table_entry = syield
                else:
                    if uncertainties_only:
                        if syield == 0.:
                            table_entry = "indeterminate"
                        else:
                            table_entry = "$(\pm {:.2f} \%)$".format(sr_yield.stat_err / syield * 100.)
                    else:
                        table_entry = "${:.2f} \pm {:.2f}$".format(syield, sr_yield.stat_err)
            tab.print_table_cell(table_entry, is_last=is_last),

    tab.print_footer()


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-r", "--raw-yields", action="store_true", help="report raw yields instead of weighted")
    parser.add_argument("-u", "--uncertainties-only", action="store_true", help="report uncertainties only")
    parser.add_argument("-c", "--csv", action="store_true", help="use CSV format instead of LaTeX")
    parser.add_argument("-s", "--scale-factors", action="store_true", help="print scale factors instead of yields")
    args = parser.parse_args()

    if USE_SAMPLE_GROUPS:
        for s in SAMPLE_GROUPS:
            main(s, raw_yields=args.raw_yields, uncertainties_only=args.uncertainties_only, csv=args.csv, print_scale_factors=args.scale_factors)
    else:
        for s in SAMPLES:
            main(s, raw_yields=args.raw_yields, uncertainties_only=args.uncertainties_only, csv=args.csv, print_scale_factors=args.scale_factors)

