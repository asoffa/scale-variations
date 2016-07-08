#!/usr/bin/env python

import samples
import debug
import ROOT
from regions import SRs, SRs_reco
from ROOT import TChain, TEventList
from config import SAMPLES

ROOT.gErrorIgnoreLevel = ROOT.kError

#-------------------------------------------------------------------------------
SAMPLE = "MadGraphPythia8EvtGen_A14NNPDF23LO_ttee_Np1_nom"

#-------------------------------------------------------------------------------

def get_chain(sample):
    sample_dict = samples.get_samples("_".join(SAMPLE.split("_")[:-1]))
    s = sample_dict[sample]
    if s.is_reco:
        chain = TChain("superNt")
        sr_dict = SRs_reco
    else:
        chain = TChain("SuperTruth")
        sr_dict = SRs
    chain.Add(s.root_file_pattern)
    return chain

def dump_event_info(tree, cut, is_reco=False):
    print 40*"-"
    print "cut =", cut
    print "event numbers:"
    elist = TEventList('elist', 'elist')
    tree.Draw('>>elist', cut)
    for i in xrange(0, elist.GetN()):
        tree.GetEntry(elist.GetEntry(i))
        if is_reco:
            event_number = tree.event_number
            weight = tree.event_weight
            lep_pt = tree.lep_pt
            lep_eta = tree.lep_eta
        else:
            event_number = tree.eventNumber
            weight = tree.mcEventWeight
            lep_pt = tree.lepton_pt
            lep_eta = tree.lepton_eta
        n_lep = tree.n_leptons
        print "    event_number={}, met={:.2f}, meff={:.2f}, lep:".format(event_number, tree.met, tree.meff),
        for i, lpt in enumerate(lep_pt):
            print "(pt={:.2f}, eta={:.2f}),".format(lpt, lep_eta[i]),
        print
    # reset default
    is_reco=False

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    chain = get_chain(SAMPLE)
    dump_event_info(chain, SRs["SR3b"])
        
