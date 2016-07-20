
USE_SAMPLE_GROUPS    = True # use sample group names to group samples if set to `True`, else use individual samples
USE_SR0b2_j25        = False # use modified signal region SR0b2 with jet pT cut of 25 GeV instead of 40 GeV
USE_RPV_SRS          = False # use RPV signal regions
USE_TRUTH_JETS       = False # use truth jets if set to `True`, else reco or pseudo-reco jets (note: this has nothing to do with whether truth jets were used in overlap removal)
LUMI_TO_SCALE_TO     = 10.0  # desired luminosity (fb^-1)
USE_RAW_N_EVENTS     = False
USE_RAW_LUMI         = False
SAMPLE_FILE          = "/data/uclhc/uci/user/asoffa/projects/ss3l/repos/scale_variations_n0224/scale-variations/scale_variations/samples.tab"
VERBOSE              = False

#YIELD_GROUP_DICT = {
#    "nom"      : ["nom"                          ],
#    "scale_up" : ["fac4",   "renorm4",   "qsf4"  ],
#    "scale_dn" : ["fac025", "renorm025", "qsf025"],
#}

SAMPLE_GROUPS = [
    "WZ",
    #"ZZ",
    #"ttV",
    #"ttW",
    #"ttZ",
]

SAMPLES = [
    #### ttW
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttW_Np0",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttW_Np1",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttW_Np2",
    #"Sherpa_NNPDF30NNLO_ttW",

    #### ttZ
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttee_Np0",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttee_Np1",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttmumu_Np0",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_ttmumu_Np1",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_tttautau_Np0",
    #"MadGraphPythia8EvtGen_A14NNPDF23LO_tttautau_Np1",
    #"Sherpa_NNPDF30NNLO_ttll_mll5",

    #### dibosons
    #"WplvWmqq",
    #"WpqqWmlv",
    #"WlvZqq",
    #"WqqZll",
    #"WqqZvv",
    #"ZqqZll",
    #"ZqqZvv",
    #"lllvSFMinus",
    #"lllvOFMinus",
    "lllvSFPlus",
    #"lllvOFPlus",
    #"llll",
    #"llvv",
    #"ggllll",
    #"ggllvv",
    #"lvvv",
    #"vvvv",
    #"lllvSFMinus_ckkw15",
    #"lllvSFMinux_ckkw30",
    #"lllvOFMinus_ckkw15",
    #"lllvOFMinus_ckkw30",
    #"lllvSFPlus_ckkw15",
    #"lllvSFPlus_ckkw30",
    #"lllvOFPlus_ckkw15",
    #"lllvOFPlus_ckkw30",
    #"llvv_ckkw15",
    #"llvv_ckkw30",
    #"llll_ckkw15",
    #"llll_ckkw30",
]

