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
        if s.is_reco:
            chain = TChain("superNt")
            sr_dict = SRs_reco
        else:
            chain = TChain("SuperTruth")
            sr_dict = SRs
        chain.Add(s.root_file_pattern)
        for sr_name, sr_cut in sr_dict.iteritems():
            is_last = (sr_name == next(reversed(sr_dict)))
            if s.is_reco:
                sr_yield = samples.Yield(chain, sr_cut, "event_weight", scale_factor=s.scale_factor, dummy_var="event_number")
            else:
                sr_yield = samples.Yield(chain, sr_cut, "mcEventWeight", scale_factor=s.scale_factor, dummy_var="eventNumber")
            table_entry = "${:.2f} \pm {:.2f}$".format(sr_yield.n_weighted, sr_yield.stat_err)
            #table_entry = "${:.2f}$".format(sr_yield.scale_factor)
            tab.print_table_cell(table_entry, is_last=is_last),

    tab.print_footer()


#-------------------------------------------------------------------------------

if __name__ == '__main__':
    for s in SAMPLES:
        main(s)

