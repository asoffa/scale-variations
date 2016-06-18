#!/usr/bin/env python

import samples
import debug
import ROOT
from regions import SRs, SRs_reco
from ROOT import TChain
from config import SAMPLES

ROOT.gErrorIgnoreLevel = ROOT.kError

#-------------------------------------------------------------------------------

def main(sample_group):
    sample_dict = samples.get_samples(sample_group)
    #samples.print_samples(sample_dict)

    for name, s in sample_dict.iteritems():
        if not name.endswith("_reco") and not name.endswith("_nom"):
            continue
        if s.is_reco:
            chain = TChain("superNt")
            sr_dict = SRs_reco
        else:
            chain = TChain("SuperTruth")
            sr_dict = SRs
        chain.Add(s.root_file_pattern)
        sr_cut = sr_dict["SS/3L"]
        debug.dump_event_info(name, chain, sr_cut, s.scale_factor, s.is_reco)

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    for s in SAMPLES:
        main(s)

