import ROOT
from ROOT import TFile
from ROOT import RooRealVar, RooDataSet, RooWorkspace, RooArgSet
ROOT.RooWorkspace.rfimport = getattr(ROOT.RooWorkspace, 'import')
from configs.dtb import decaytime_binnning, tau, ctau
from datetime import datetime
from configs.cuts import preselection_cut as offline_cut
from Background_Subtraction import Subtract_Distribution
from configs.user import *
"""
This script takes huge workspace created with Merge_DS script and split it within decay time bins.
This improves speed of fit and helps to cope with root limitations
"""


def Split_DS(Save_DS = False):
    ws_file = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/WorkSpaces/Merged_Merged_WS.root", "read")
    wsp = ws_file.Get("wspace")
    ws_file.Close()
    LOG_D0_IPCHI2_OWNPV = wsp.var("LOG_D0_IPCHI2_OWNPV")
    Dst_DTF_D0_CTAU = wsp.var("Dst_DTF_D0_CTAU")
    Dst_DTF_D0_M = wsp.var("Dst_DTF_D0_M")
    DTF_D0sPi_M = wsp.var("DTF_D0sPi_M")
    DTF_D0sPi_M.setMax(2020)
    DTF_D0sPi_M.setMin(2000)
    dataset_RS_tot = wsp.data("dataset_RS")
    dataset_RS_tot.SetName("dataset_RS_tot")

    varset = RooArgSet("varset")
    varset.add(LOG_D0_IPCHI2_OWNPV)
    varset.add(DTF_D0sPi_M)
    varset.add(Dst_DTF_D0_CTAU)
    varset.add(Dst_DTF_D0_M)

    for i, bin in enumerate(decaytime_binnning):
        start = datetime.now()
        dataset_RS_dtb_init = RooDataSet("dataset_RS_dtb_init", "Decaytime bin"+str(i),dataset_RS_tot, varset,"Dst_DTF_D0_CTAU>"+str(bin[0]*ctau)+"&&Dst_DTF_D0_CTAU<"+str(bin[1]*ctau)+"&&"+offline_cut)
        dataset_RS = Subtract_Distribution(dataset_RS_dtb_init, DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV, str(i))
        dataset_RS.SetName("dataset_RS")
        wspace = RooWorkspace("wspace")
        wsfile2 = TFile("~/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/WorkSpaces/Merged_WS_Bin_"+str(i)+".root", "recreate")
        wspace.rfimport(varset)
        wspace.rfimport(dataset_RS)
        wspace.Write("wspace")
        wsfile2.Close()
        print "Dataset "+str(i)+" creation took  "+str(datetime.now()-start)+" \n"

    return True

if __name__ == "__main__":
    Split_DS(True)    
