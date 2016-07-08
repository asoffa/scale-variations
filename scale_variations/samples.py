
import os
import fnmatch
from collections import OrderedDict, namedtuple
from math import sqrt
from ROOT import TChain, TH1D, Double, TFile
from config import SAMPLE_FILE, LUMI_TO_SCALE_TO, USE_SAMPLE_GROUPS, USE_RAW_LUMI, USE_RAW_N_EVENTS, VERBOSE


PB_TO_FB = 1000.0


Sample = namedtuple("Sample", "name  group  root_file_pattern  scale_factor  is_reco  lumi")

class Yield(namedtuple("Yield",  "n_entries  n_weighted  stat_err")):
    def __add__(self, other):
        n_entries  = self.n_entries
        n_weighted = self.n_weighted + other.n_weighted
        stat_err   = sqrt(self.stat_err**2 + other.stat_err**2)
        return Yield(n_entries, n_weighted, stat_err)
    def __sub__(self, other):
        n_entries  = self.n_entries
        n_weighted = self.n_weighted - other.n_weighted
        stat_err   = sqrt(self.stat_err**2 + other.stat_err**2)
        return Yield(n_entries, n_weighted, stat_err)
    def __mul__(self, factor):
        n_entries  = self.n_entries
        n_weighted = self.n_weighted * factor
        stat_err   = self.stat_err * factor
        return Yield(n_entries, n_weighted, stat_err)
    def __div__(self, factor):
        n_entries  = self.n_entries
        n_weighted = self.n_weighted / factor
        stat_err   = self.stat_err / factor
        return Yield(n_entries, n_weighted, stat_err)


def get_single_yield(sample, cut, _nhist=0):
    if sample.is_reco:
        chain     = TChain("superNt")
        weight    = "event_weight"
        dummy_var = "event_number"
    else:
        chain     = TChain("SuperTruth")
        weight    = "mcEventWeight"
        dummy_var = "eventNumber"

    chain.Add(sample.root_file_pattern)

    # ensure unique histogram names so ROOT doesn't complain
    _nhist += 1
    hname = 'h_{}'.format(_nhist)
    h = TH1D(hname, hname, 1, -1e30, 1e30)
    cmd = "{}>>+{}".format(dummy_var, h.GetName())
    chain.Draw(cmd, "({})*{}*{}".format(cut, weight, sample.scale_factor), "goff")

    h_raw = TH1D(hname+'_raw', hname+'_raw', 1, -1e30, 1e30)
    cmd_raw = "{}>>+{}".format(dummy_var, h_raw.GetName())
    chain.Draw(cmd_raw, "{}".format(cut), "goff")

    stat_err = Double(0.0)
    integral = h.IntegralAndError(0, -1, stat_err)

    n_entries = h_raw.Integral()
    n_weighted = integral
    stat_err = stat_err

    return Yield(n_entries, n_weighted, stat_err)


def get_group_yield(sample_group, cut):
    sum_of_yields = 0.
    sum_of_squared_stat_errors = 0.
    sum_of_n_entries = 0.
    for s in sample_group:
        y = get_single_yield(s, cut)
        sum_of_n_entries += y.n_entries
        sum_of_yields += y.n_weighted
        sum_of_squared_stat_errors += y.stat_err**2
    return Yield(sum_of_n_entries, sum_of_yields, sqrt(sum_of_squared_stat_errors))


def get_root_file_pattern(dsid, is_reco=False):
    if is_reco:
        return "/data/uclhc/uci/user/asoffa/projects/ss3l/productions/n0222/superNt/rootfiles/batch_mc/rootfiles/CENTRAL_{}.root".format(dsid)
    return "/data/uclhc/uci/user/asoffa/projects/ss3l/productions/scale_variations_n0224/SuperTruth/out_{}/data-myOutput/*.root*".format(dsid)


def get_sum_of_weights(root_file_pattern):
    files = []
    search_dir = "/".join(root_file_pattern.split("/")[:-1])
    if not os.path.isdir(search_dir):
        print "Warning: no such directory: {} (omitting!)".format(search_dir)
        return 0.
    for f in os.listdir(search_dir):
        if fnmatch.fnmatch(f, "*.root*"):
            files.append(search_dir+"/"+f)
    if len(files) == 0.:
        raise Exception("no ROOT files found matching pattern '{}'".format(root_file_pattern))
    sumw = 0.
    for f in files:
        rootfile = TFile(f, "READ")
        if not rootfile or not rootfile.Get("CutflowWeighted"):
            raise Exception("No 'CutflowWeighted' histogram found in {}".format(rootfile))
        sumw += rootfile.Get("CutflowWeighted").GetBinContent(1)
    return sumw


def get_base_name(short_name):
    return "_".join(short_name.split("_")[:-1])


def get_sample_groups(token, use_group=True):
    sample_dict = get_samples(token, use_group=use_group)
    sample_groups = OrderedDict()
    for s in sample_dict.values():
        if get_base_name(s.group) != token:
            continue
        if s.group not in sample_groups.keys():
            sample_groups[s.group] = []
            if VERBOSE:
                print "Added sample group: {}".format(s.group)
        sample_groups[s.group].append(s)
    return sample_groups
    # reset default
    use_group=True


def get_samples(token, use_group=False):
    samples = OrderedDict()
    nominal_eff_xsec = {}
    with open(SAMPLE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue
            values = line.split()
            short_name = values[1]
            group      = values[2]
            if token=="ttV" and (group.startswith("ttW") or group.startswith("ttZ")):
                group = "ttV" + group[3:]
            if USE_SAMPLE_GROUPS:
                is_match = get_base_name(group) == token
            else:
                is_match = get_base_name(short_name) == token
            if not is_match:
                continue
            dsid     = values[0]
            is_reco  = short_name.endswith("_reco")
            root_file_pattern = get_root_file_pattern(dsid, is_reco=is_reco)
            if is_reco:
                lumi = float(values[4])
                scale_factor = LUMI_TO_SCALE_TO / lumi
            else:
                if USE_RAW_LUMI:
                    lumi = float(values[4])
                    scale_factor = LUMI_TO_SCALE_TO / lumi
                else:
                    if USE_RAW_N_EVENTS:
                        n_events = float(values[3])
                    else:
                        n_events = get_sum_of_weights(root_file_pattern)
                    if n_events == 0:
                        continue
                    raw_xsec = float(values[5]) * PB_TO_FB
                    BR       = float(values[6])
                    filt_eff = float(values[7])
                    k_factor = float(values[8])
                    eff_xsec = raw_xsec * BR * filt_eff * k_factor
                    lumi = n_events / eff_xsec
                    scale_factor = LUMI_TO_SCALE_TO / lumi
            base_name = get_base_name(short_name)
            if short_name.endswith("_nom") and base_name not in nominal_eff_xsec.keys():
                nominal_eff_xsec[base_name] = eff_xsec
            elif not short_name.endswith("_reco"):
                if base_name not in nominal_eff_xsec.keys():
                    raise Exception("nominal sample must come before variation sample in sample table for variation samples to be scaled correctly")
                scale_factor *= nominal_eff_xsec[base_name] / eff_xsec
            samples[short_name] = Sample(short_name, group, root_file_pattern, scale_factor, is_reco, lumi)
            if VERBOSE:
                print "Added sample: {}".format(short_name)
    # reset default
    use_group=False
    return samples


def print_samples(samples):
    print 50*'-'
    print "Contents in samples:"
    for name, sdata in samples.iteritems():
        print "  {} : {}".format(name, sdata)
    print 50*'-'

