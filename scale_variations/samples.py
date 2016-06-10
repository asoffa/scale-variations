
import os
import fnmatch
from collections import OrderedDict
from ROOT import TH1D, Double, TFile
from config import SAMPLE_FILE, LUMI_TO_SCALE_TO


PB_TO_FB = 1000.0


class Yield:
    def __init__(self, tree, cut, weight, scale_factor=1.0, dummy_var="event_number", _nhist = 0):
        # ensure unique histogram names so ROOT doesn't complain
        _nhist += 1
        hname = 'h_{}'.format(_nhist)

        h = TH1D(hname, hname, 1, -1e30, 1e30)
        cmd = "%s>>+%s"%(dummy_var, h.GetName())
        tree.Draw(cmd, "({})*{}*{}".format(cut, weight, scale_factor), "goff")
        stat_err = Double(0.0)
        integral = h.IntegralAndError(0, -1, stat_err)

        self.n_unweighted = tree.GetEntries()
        self.n_weighted = integral
        self.stat_err = stat_err


def get_root_file_pattern(dsid, is_reco=False):
    if is_reco:
        return "/data/uclhc/uci/user/asoffa/projects/ss3l/productions/n0222/superNt/rootfiles/batch_mc/rootfiles/CENTRAL_{}.root".format(dsid)
    return "/data/uclhc/uci/user/asoffa/projects/ss3l/repos/scale_variations_n0224/run_test/condor/out/out_{}/data-myOutput/*.root*".format(dsid)


def get_sum_of_weights(root_file_pattern):
    files = []
    search_dir = "/".join(root_file_pattern.split("/")[:-1])
    if not os.path.isdir(search_dir):
        return 0
    for f in os.listdir(search_dir):
        if fnmatch.fnmatch(f, "*.root*"):
            files.append(search_dir+"/"+f)
    if len(files) == 0:
        raise Exception("no ROOT files found matching pattern '{}'".format(root_file_pattern))
    elif len(files) > 1:  #TODO: generalize to allow for multiple files
        raise Exception("multiple ROOT files found matching patter '{}'".format(root_file_pattern))
    rootfile = TFile(files[0], "READ")
    if not rootfile or not rootfile.Get("CutflowWeighted"):
        return 0
    sumw = rootfile.Get("CutflowWeighted").GetBinContent(1)
    return sumw


def get_samples(short_name_prefix):
    samples = OrderedDict()
    with open(SAMPLE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or len(line) == 0:
                continue
            values = line.split()
            short_name = values[1]
            if "_".join(short_name.split("_")[:-1]) == short_name_prefix:
                dsid     = values[0]
                is_reco  = short_name.endswith("_reco")
                root_file_pattern = get_root_file_pattern(dsid, is_reco=is_reco)
                if is_reco:
                    lumi = float(values[3])
                    scale_factor = LUMI_TO_SCALE_TO / lumi
                else:
                    n_events = get_sum_of_weights(root_file_pattern)
                    if n_events == 0:
                        continue
                    raw_xsec = float(values[4]) * PB_TO_FB
                    BR       = float(values[5])
                    filt_eff = float(values[6])
                    k_factor = float(values[7])
                    lumi = n_events / (raw_xsec * BR * filt_eff * k_factor)
                    scale_factor = LUMI_TO_SCALE_TO / lumi
                samples[short_name] = (root_file_pattern, scale_factor, is_reco)
    return samples


def print_samples(samples):
    print 50*'-'
    print "Contents in samples:"
    for name, sdata in samples.iteritems():
        print "  {} : {}".format(name, sdata)
    print 50*'-'

