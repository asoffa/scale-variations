
from collections import OrderedDict


SRs      = OrderedDict()  # (scale factor, region cut)
SRs_reco = OrderedDict()


def n_lep_cut(n_leptons, is_reco=False):
    if is_reco:
        return "n_leptons >= {}".format(n_leptons)
    else:
        if n_leptons < 2:
            return "0"
        elif n_leptons == 2:
            return "((n_leptons > 2 || isSS) && lepton_pt[1] > 20)".format(n_leptons)
        else:
            return "(n_leptons >= {} && lepton_pt[1] > 20)".format(n_leptons)


#SRs["SR3L"   ] = n_lep_cut(3, is_reco) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 200               "
#SRs["SR0b1"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 == 0 && n_jets_25 >= 6 && met > 175 && meff >  600"
#SRs["SR0b2"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 == 0 && n_jets_50 >= 5 && met > 175 && meff > 1300"
#SRs["SR1b1"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 >= 1 && n_jets_25 >= 6 && met > 150 && meff >  600"
#SRs["SR1b2"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 >= 1 && n_jets_25 >= 6 && met > 200 && meff >  650"
#SRs["SR3b1"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 >= 3 && n_jets_25 >= 6 && met >  50               "
#SRs["SR3b2"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 >= 3 && n_jets_25 >= 5 && met > 100 && meff > 1100"
#
#SRs["SR0b5j" ] = n_lep_cut(2, is_reco) + " && n_bjets_20 == 0 && n_jets_50 >= 5 && met > 125 && meff >  650"
#SRs["SR2b1"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 >= 2 && n_jets_25 >= 6 && met > 100 && meff >  550"
#SRs["SR2b2"  ] = n_lep_cut(2, is_reco) + " && n_bjets_20 >= 2 && n_jets_25 >= 5 && met > 150 && meff >  600"
#SRs["SR3L3b" ] = n_lep_cut(3, is_reco) + " && n_bjets_20 >= 3                   && met >  50               "

SRs[     "SS/3L"] = n_lep_cut(2, is_reco=False) + " && lepton_pt[1] > 20"
SRs[     "SR3L1"] = n_lep_cut(3, is_reco=False) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 150               "
SRs[     "SR3L2"] = n_lep_cut(3, is_reco=False) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 200 && meff > 1500"
SRs[     "SR0b1"] = n_lep_cut(2, is_reco=False) + " && n_bjets_20 == 0 && n_jets_25 >= 6 && met > 150 && meff >  500"
SRs[     "SR0b2"] = n_lep_cut(2, is_reco=False) + " && n_bjets_20 == 0 && n_jets_40 >= 6 && met > 150 && meff >  900"
SRs[     "SR1b" ] = n_lep_cut(2, is_reco=False) + " && n_bjets_20 >= 1 && n_jets_25 >= 6 && met > 200 && meff >  650"
SRs[     "SR3b" ] = n_lep_cut(2, is_reco=False) + " && n_bjets_20 >= 3 && n_jets_25 >= 6 && met > 150 && meff >  600"

SRs_reco["SS/3L"] = n_lep_cut(2, is_reco=True ) + " && lep_pt[1] > 20"
SRs_reco["SR3L1"] = n_lep_cut(3, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 150               "
SRs_reco["SR3L2"] = n_lep_cut(3, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 200 && meff > 1500"
SRs_reco["SR0b1"] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_25 >= 6 && met > 150 && meff >  500"
SRs_reco["SR0b2"] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_40 >= 6 && met > 150 && meff >  900"
SRs_reco["SR1b" ] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 >= 1 && n_jets_25 >= 6 && met > 200 && meff >  650"
SRs_reco["SR3b" ] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 >= 3 && n_jets_25 >= 6 && met > 150 && meff >  600"


