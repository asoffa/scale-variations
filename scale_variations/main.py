#!/usr/bin/env python

import samples
import tabulate as tab
import ROOT
from regions import SRs, SRs_reco
from ROOT import TChain
from config import USE_SAMPLE_GROUPS, SAMPLE_GROUPS, SAMPLES

ROOT.gErrorIgnoreLevel = ROOT.kError

#-------------------------------------------------------------------------------

def main(sample_set):
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
            if USE_SAMPLE_GROUPS:
                sr_yield = samples.get_group_yield(s, sr_cut)
            else:
                sr_yield = samples.get_single_yield(s, sr_cut)
            table_entry = "${:.2f} \pm {:.2f}$".format(sr_yield.n_weighted, sr_yield.stat_err)
            tab.print_table_cell(table_entry, is_last=is_last),

    tab.print_footer()


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    if USE_SAMPLE_GROUPS:
        for s in SAMPLE_GROUPS:
            main(s)
    else:
        for s in SAMPLES:
            main(s)

