
from ROOT import TEventList

def dump_event_info(name, tree, cut, scale_factor, is_reco=False):
    print 40*"-"
    print "Dumping events for", name
    elist = TEventList('elist', 'elist')
    tree.Draw('>>elist', cut)
    sum_of_weights = 0
    for i in xrange(0, elist.GetN()):
        tree.GetEntry(elist.GetEntry(i))
        if is_reco:
            event_number = tree.event_number
            weight = tree.event_weight
        else:
            event_number = tree.eventNumber
            weight = tree.mcEventWeight
        #print "  {:>10}   {:.2f}".format(event_number, weight)
        sum_of_weights += weight
    print "  cut          =", cut
    print "  N_entries    =", elist.GetN()
    print "  scale factor =", scale_factor
    print "  N_events     =", sum_of_weights * scale_factor
    # reset default
    is_reco=False
        

