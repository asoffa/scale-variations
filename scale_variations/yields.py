
# module for computing yields from samples

# primary functions to call:
#   * get_single_yield
#   * get_single_percent_diff
#   * get_group_yield
#   * get_group_percent_diff
#-------------------------------------------------------------------------------

import tabulate as tab
from ROOT import TChain, TH1D, Double
from math import sqrt


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

    stat_err = Double(0.0)
    n_weighted = h.IntegralAndError(0, -1, stat_err)

    return Yield(n_weighted, stat_err)

def get_single_percent_diff(sample, nominal_sample, cut):
    sample_yield = get_single_yield(sample, cut)
    nominal_yield = get_single_yield(nominal_sample, cut)
    return sample_yield.percent_diff(nominal_yield)


def get_group_yield(sample_group, cut):
    sum_of_yields = Yield(0., 0.)
    for s in sample_group:
        sum_of_yields += get_single_yield(s, cut)
    return sum_of_yields

def get_group_percent_diff(sample_group, nominal_sample_group, cut):
    sample_yield  = get_group_yield(sample_group, cut)
    nominal_yield = get_group_yield(nominal_sample_group, cut)
    return sample_yield.percent_diff(nominal_yield)


#-------------------------------------------------------------------------------

class Yield:
    def __init__(self, n_weighted, stat_err, is_percent=False):
        self.n_weighted = n_weighted
        self.stat_err   = stat_err
        self.is_percent = is_percent
        is_percent=False

    def __add__(self, other):
        n_weighted = self.n_weighted + other.n_weighted
        stat_err   = sqrt(self.stat_err**2 + other.stat_err**2)
        return Yield(n_weighted, stat_err)

    def __sub__(self, other):
        n_weighted = self.n_weighted - other.n_weighted
        stat_err   = sqrt(self.stat_err**2 + other.stat_err**2)
        return Yield(n_weighted, stat_err)

    def __mul__(self, factor):
        n_weighted = self.n_weighted * factor
        stat_err   = self.stat_err * factor
        return Yield(n_weighted, stat_err)

    def __div__(self, factor):
        n_weighted = self.n_weighted / factor
        stat_err   = self.stat_err / factor
        return Yield(n_weighted, stat_err)

    def percent_diff(self, other):
        s  = self.n_weighted
        ds = self.stat_err
        n  = other.n_weighted
        dn = other.stat_err

        if abs(n) < 1e-15:
            return Yield(None, None)

        integral = (s - n) / n * 100.
        if abs(s) < 1e-15:
            return Yield(integral, None)

        stat_err = s/n * sqrt( (ds/s)**2 + (dn/n)**2 ) * 100.
        return Yield(integral, stat_err, is_percent=True)

    def latex_entry(self):
        if self.n_weighted == None:
            return "indeterminate"
        if self.is_percent:
            if abs(self.n_weighted) < 0.01:
                return "$< 0.01\%$"
            if self.stat_err == None:
                return "${:.2f}\, (\pm ??)\, \%$".format(self.n_weighted)
            if self.stat_err < 0.01:
                self.stat_err = 0.01
            return "${:+.2f}\, (\pm {:.2f})\, \%$".format(self.n_weighted, self.stat_err)
        else:
            if abs(self.n_weighted) < 0.01:
                return "$< 0.01$"
            if self.stat_err == None:
                return "${:.2f}\, (\pm ??)$".format(self.n_weighted)
            if self.stat_err < 0.01:
                self.stat_err = 0.01
            return "${:.2f}\, (\pm {:.2f})$".format(self.n_weighted, self.stat_err)

    def csv_entry(self):
        if self.is_percent:
            return "{}%".format(self.n_weighted)
        return "{}".format(self.n_weighted)


#class YieldAndSyst(namedtuple("YieldAndSyst", "syield  percent_diff")):
#    def print_latex(self):
#        pass
#    def print_csv(self):
#        pass

