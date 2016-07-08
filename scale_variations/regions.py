
from collections import OrderedDict
from config import USE_TRUTH_JETS, USE_RPV_SRS


SRs      = OrderedDict()
SRs_reco = OrderedDict()


def n_lep_cut(n_leptons, is_reco=False):
    if is_reco:
        return "n_leptons >= {}".format(n_leptons)
    else:
        if n_leptons < 2:
            return "0"
        elif n_leptons == 2:
            return "((n_leptons > 2 || (n_leptons == 2 && isSS)) && lepton_pt[1] > 20)".format(n_leptons)
        else:
            return "(n_leptons >= {} && lepton_pt[1] > 20)".format(n_leptons)

if USE_TRUTH_JETS:
    n_bjets_20 = "n_truth_bjets_20"
    n_bjets_25 = "n_truth_bjets_25"
    n_bjets_40 = "n_truth_bjets_40"
    n_bjets_50 = "n_truth_bjets_50"

    n_jets_20  = "(n_truth_bjets_20 + n_truth_ljets_20)"
    n_jets_25  = "(n_truth_bjets_25 + n_truth_ljets_25)"
    n_jets_40  = "(n_truth_bjets_40 + n_truth_ljets_40)"
    n_jets_50  = "(n_truth_bjets_50 + n_truth_ljets_50)"

else:
    n_bjets_20 = "n_bjets_20"
    n_bjets_25 = "n_bjets_25"
    n_bjets_40 = "n_bjets_40"
    n_bjets_50 = "n_bjets_50"

    n_jets_20  = "n_jets_20"
    n_jets_25  = "n_jets_25"
    n_jets_40  = "n_jets_40"
    n_jets_50  = "n_jets_50"


if not USE_RPV_SRS:
    SRs[     "SS3L\_1j"] = n_lep_cut(2, is_reco=False) + " && {} >= 1".format(n_jets_25)
    SRs[        "SR3L1"] = n_lep_cut(3, is_reco=False) + " && {} == 0 && {} >= 4 && met > 150               ".format(n_bjets_20, n_jets_40)
    SRs[        "SR3L2"] = n_lep_cut(3, is_reco=False) + " && {} == 0 && {} >= 4 && met > 200 && meff > 1500".format(n_bjets_20, n_jets_40)
    SRs[        "SR0b1"] = n_lep_cut(2, is_reco=False) + " && {} == 0 && {} >= 6 && met > 150 && meff >  500".format(n_bjets_20, n_jets_25)
    SRs[        "SR0b2"] = n_lep_cut(2, is_reco=False) + " && {} == 0 && {} >= 6 && met > 150 && meff >  900".format(n_bjets_20, n_jets_40)
    SRs[        "SR1b" ] = n_lep_cut(2, is_reco=False) + " && {} >= 1 && {} >= 6 && met > 200 && meff >  650".format(n_bjets_20, n_jets_25)
    SRs[        "SR3b" ] = n_lep_cut(2, is_reco=False) + " && {} >= 3 && {} >= 6 && met > 150 && meff >  600".format(n_bjets_20, n_jets_25)

    SRs_reco["SS3L\_1j"] = n_lep_cut(2, is_reco=True ) + " && n_jets_25 >= 1"
    SRs_reco[   "SR3L1"] = n_lep_cut(3, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 150               "
    SRs_reco[   "SR3L2"] = n_lep_cut(3, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_40 >= 4 && met > 200 && meff > 1500"
    SRs_reco[   "SR0b1"] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_25 >= 6 && met > 150 && meff >  500"
    SRs_reco[   "SR0b2"] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 == 0 && n_jets_40 >= 6 && met > 150 && meff >  900"
    SRs_reco[   "SR1b" ] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 >= 1 && n_jets_25 >= 6 && met > 200 && meff >  650"
    SRs_reco[   "SR3b" ] = n_lep_cut(2, is_reco=True ) + " && n_bjets_20 >= 3 && n_jets_25 >= 6 && met > 150 && meff >  600"

else:
    SRs[     "SR1b-DD" ] = n_lep_cut(2, is_reco=False) + " && {} >= 1 && {} >= 4 && meff > 1200".format(n_bjets_20, n_jets_50)
    SRs[     "SR3b-DD" ] = n_lep_cut(2, is_reco=False) + " && {} >= 3 && {} >= 4 && meff > 1000".format(n_bjets_20, n_jets_50)
    SRs[     "SR1b-GG" ] = n_lep_cut(2, is_reco=False) + " && {} >= 1 && {} >= 6 && meff > 1800".format(n_bjets_20, n_jets_50)

    # just placeholders for now!
    SRs_reco[     "SR1b-DD" ] = "1"
    SRs_reco[     "SR3b-DD" ] = "1"
    SRs_reco[     "SR1b-GG" ] = "1"


