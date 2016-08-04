
# module for acquiring samples

# primary functions to call:
#   * get_sample_dict
#   * get_sample_group_dict
#   * get_base_name
#-------------------------------------------------------------------------------

import os
import fnmatch
from collections import OrderedDict, namedtuple
from ROOT import TFile
from sample_data import keys, sample_data
from config import LUMI_TO_SCALE_TO, USE_SAMPLE_GROUPS, USE_RAW_LUMI, USE_RAW_N_EVENTS


PB_TO_FB = 1000.0


Sample = namedtuple("Sample", "name  group  root_file_pattern  is_reco  lumi  scale_factor")

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


def get_sample_group_dict(token, verbose=False):
    sample_dict = get_sample_dict(token)
    sample_groups = OrderedDict()
    for s in sample_dict.values():
        if get_base_name(s.group) != token:
            continue
        if s.group not in sample_groups.keys():
            sample_groups[s.group] = []
            if verbose:
                print "Added sample group: {}".format(s.group)
        sample_groups[s.group].append(s)
    return sample_groups


def get_sample_dict(token, verbose=False):
    sample_dict = OrderedDict()
    nominal_eff_xsec = {}
    for short_name, data in sample_data.iteritems():
        group = data[keys["group"]]
        if token=="ttV" and (group.startswith("ttW") or group.startswith("ttZ")):
            group = "ttV" + group[3:]
        if USE_SAMPLE_GROUPS:
            is_match = get_base_name(group) == token
        else:
            is_match = get_base_name(short_name) == token
        if not is_match:
            continue
        dsid     = data[keys["DSID"]]
        is_reco  = short_name.endswith("_reco")
        root_file_pattern = get_root_file_pattern(dsid, is_reco=is_reco)
        if is_reco:
            lumi = data[keys["lumi"]]
            scale_factor = LUMI_TO_SCALE_TO / lumi
        else:
            if USE_RAW_LUMI:
                lumi = data[keys["lumi"]]
                scale_factor = LUMI_TO_SCALE_TO / lumi
            else:
                if USE_RAW_N_EVENTS:
                    n_events = data[keys["n_events"]]
                else:
                    n_events = get_sum_of_weights(root_file_pattern)
                if n_events == 0:
                    continue
                raw_xsec = data[keys["xsec"]] * PB_TO_FB
                BR       = data[keys["BR"]]
                filt_eff = data[keys["filt_eff"]]
                k_factor = data[keys["k_factor"]]
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
        sample_dict[short_name] = Sample(short_name, group, root_file_pattern, is_reco, lumi, scale_factor)
        if verbose:
            print "Added sample: {}".format(short_name)
    return sample_dict


def print_sample_dict(sample_dict):
    print 50*'-'
    print "Contents in sample_dict:"
    for name, sdata in sample_dict.iteritems():
        print "  {} : {}".format(name, sdata)
    print 50*'-'

