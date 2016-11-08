import ROOT
from ROOT import TFile, TCanvas
from ROOT import RooRealVar, RooDataSet, RooWorkspace
from ROOT import RooFit, RooDataHist, RooAddPdf, RooArgList, RooKeysPdf, RooHistPdf, RooArgSet
from ROOT import gPad
from configs.dtb import decaytime_binnning, tau, ctau
from Merge_DS import WS_list
from datetime import datetime
from ROOT import gStyle
import sys
import os
import array
from configs.cuts import combination_cut
from configs.cuts import preselection_cut
from configs.user import user, prefix
from Background_Subtraction import Subtract_Distribution
ROOT.RooWorkspace.rfimport = getattr(ROOT.RooWorkspace, 'import')

"""
This script provides matching of fully-reconstructed B decays (COMB_OS) with their parita-reconstructed entries to D* decays (RS).
This script uses data defined in Merge_DS.py script.
As an output, the script provide background-subtracted Log(IPCHI2) shapes of matched D* candidates in ctau bins (bins are defined in configs/dtb.py)
"""

#This fills temporary tree with information from matched candidates.
#combs - is a list of keys of B-candidates. Key is a string formed from exact numeric values of LOG_D0_IPCHI2_OWNPV and D0_M variables.
#signals - is a dictionary which stores info about LOG_D0_IPCHI2_OWNPV, D0_M, Dst_DTF_D0_CTAU, DTF_D0sPi_M with key formed in the same manner with combs and
def Fill_Shape(signals, combs, newtree):
    confirmed = []
    for i in combs:
        if i in signals:
            confirmed.append(signals[i])
    for c in confirmed:
        temp_LOG_D0_IPCHI2_OWNPV[0] = c[0]
        temp_Dst_DTF_D0_CTAU[0] = c[2]
        temp_DTF_D0sPi_M[0] = c[3]
        #temp_Dst_DTF_D0_M[0] = c[4]
        newtree.Fill()
    return newtree

#Usual RooFit stuff - extraction of neccessary variables
wlist = WS_list()
ws_file = TFile(wlist[0], "read")
t_wsp = ws_file.Get("wspace")
B_M = t_wsp.var("B_M")
LOG_D0_IPCHI2_OWNPV = t_wsp.var("LOG_D0_IPCHI2_OWNPV")
D0_TAU = t_wsp.var("D0_TAU")
D0_M = t_wsp.var("D0_M")
Dst_M = t_wsp.var("Dst_M")
Dst_DTF_D0_CTAU = t_wsp.var("Dst_DTF_D0_CTAU")
Dst_DTF_D0_M = t_wsp.var("Dst_DTF_D0_M")
D0sPi_M = t_wsp.var("D0sPi_M")
B_ENDVERTEX_CHI2 = t_wsp.var("B_ENDVERTEX_CHI2")
DTF_D0sPi_M = t_wsp.var("DTF_D0sPi_M")
Mu_PT = t_wsp.var("Mu_PT")
runNumber = t_wsp.var("runNumber")
    
varset_comb = RooArgSet("varset_comb")
varset_comb.add(B_M)
varset_comb.add(D0_TAU)
varset_comb.add(LOG_D0_IPCHI2_OWNPV)
varset_comb.add(D0sPi_M)
varset_comb.add(D0_M)
varset_comb.add(Mu_PT)
varset_comb.add(B_ENDVERTEX_CHI2)
varset_comb.add(runNumber)

varset = RooArgSet("varset")
varset.add(D0_M)
varset.add(D0_TAU)
varset.add(LOG_D0_IPCHI2_OWNPV)
varset.add(DTF_D0sPi_M)
varset.add(Dst_DTF_D0_CTAU)
varset.add(runNumber)
varset.add(Dst_DTF_D0_M)

varset_small = RooArgSet("varset_small")
varset_small.add(LOG_D0_IPCHI2_OWNPV)
varset_small.add(Dst_DTF_D0_CTAU)
varset_small.add(DTF_D0sPi_M)


newfile = ROOT.TFile("/tmp/"+user+"/Temp.root","recreate")
newtree = ROOT.TTree("newtree", "newtree")
temp_LOG_D0_IPCHI2_OWNPV = array.array("d", [0.0])
temp_Dst_DTF_D0_CTAU = array.array("d", [0.0])
temp_DTF_D0sPi_M = array.array("d", [0.0])
temp_Dst_DTF_D0_M = array.array("d", [0.0])
branch_LOG_D0_IPCHI2_OWNPV = newtree.Branch("LOG_D0_IPCHI2_OWNPV",temp_LOG_D0_IPCHI2_OWNPV,"LOG_D0_IPCHI2_OWNPV/D")
branch_Dst_DTF_D0_CTAU = newtree.Branch("Dst_DTF_D0_CTAU",temp_Dst_DTF_D0_CTAU,"Dst_DTF_D0_CTAU/D")
branch_DTF_D0sPi_M = newtree.Branch("DTF_D0sPi_M", temp_DTF_D0sPi_M, "DTF_D0sPi_M/D")

#Iteartion over the workspce files
for i, f_wsp in enumerate(wlist):
    print "Processing workspace "+str(i)+"/"+str(len(wlist))
    ws_file = TFile(f_wsp, "read")
    wsp = ws_file.Get("wspace")
    ws_file.Close()
    dataset_RS = wsp.data("dataset_RS")
    dataset_COMB_OS = wsp.data("dataset_COMB_OS")
    dataset_COMB_OS_dtb = RooDataSet("dataset_COMB_OS_dtb", "Combinatorial shape",dataset_COMB_OS, varset_comb,combination_cut)

    Runs = {}
    
    #Getting list of runs in the workspace
    start = datetime.now()
    for i in range(dataset_COMB_OS_dtb.numEntries()):
        i_runNumber = dataset_COMB_OS_dtb.get(i).getRealValue("runNumber")
        if i_runNumber not in Runs:
            Runs[i_runNumber]=[]
    run_indexing_time = datetime.now()-start
    
    start = datetime.now()
    #Iterating over runs
    for i, i_run in enumerate(Runs):
        #For each run we create a lists of B and D* candidates and match them later using the Fill_shape() function
        signals = {}
        combs = []
        i_dataset_COMB_OS_dtb = RooDataSet("i_dataset_COMB_OS_dtb", "Combinatorial shape",dataset_COMB_OS_dtb, varset_comb,"runNumber=="+str(i_run))
        i_dataset_RS_dtb = RooDataSet("i_dataset_RS_dtb", "Signal shape",dataset_RS, varset, preselection_cut+" && ( runNumber=="+str(i_run)+" )")
        for s_i in range(i_dataset_RS_dtb.numEntries()):        
            signals[str(i_dataset_RS_dtb.get(s_i).getRealValue("LOG_D0_IPCHI2_OWNPV"))+"__"+str(i_dataset_RS_dtb.get(s_i).getRealValue("D0_M"))] = [i_dataset_RS_dtb.get(s_i).getRealValue("LOG_D0_IPCHI2_OWNPV"),i_dataset_RS_dtb.get(s_i).getRealValue("D0_M"), i_dataset_RS_dtb.get(s_i).getRealValue("Dst_DTF_D0_CTAU"), i_dataset_RS_dtb.get(s_i).getRealValue("DTF_D0sPi_M")]
    
        for c_i in range(i_dataset_COMB_OS_dtb.numEntries()):
            combs.append(str(i_dataset_COMB_OS_dtb.get(c_i).getRealValue("LOG_D0_IPCHI2_OWNPV"))+"__"+str(i_dataset_COMB_OS_dtb.get(c_i).getRealValue("D0_M")))
        newtree = Fill_Shape(signals, combs, newtree)
        sys.stdout.flush()
        sys.stdout.write('Matching: Runs: '+str(i+1)+'/'+ str(len(Runs))+' ('+ str(int(100*float(i+1)/float(len(Runs))))+'%)\r')
    
    matching_time = datetime.now()-start
    
    print "\n"
    print "Run indexing:  "+str(run_indexing_time)
    print "Matching time: "+str(matching_time)
    print "\n"


#This is dataset create from matched D* candidates
dataset_COMB_CORR = RooDataSet("dataset_COMB_CORR","dataset_COMB_CORR",newtree,varset_small)


key_COMB = []
hist_COMB = []
for i, bin in enumerate(decaytime_binnning):
    if i == 0:
        continue
    start = datetime.now()
    dataset_COMB_CORR_dtb_init = RooDataSet("dataset_COMB_CORR_dtb_init","Decaytime bin"+str(i),dataset_COMB_CORR,varset_small,"Dst_DTF_D0_CTAU>"+str(bin[0]*ctau)+"&&Dst_DTF_D0_CTAU<"+str(bin[1]*ctau))
    dataset_COMB_CORR_dtb = Subtract_Distribution(dataset_COMB_CORR_dtb_init, DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV, str(i)+"_comb", True)
    dataset_COMB_CORR_dtb.SetName("dataset_COMB_CORR_dtb")
    print "Background substraction from combinatorial tool  "+str(datetime.now()-start)+" \n"

    hist_COMB.append(RooDataHist("hist_COMB"+str(i),"hist_COMB", RooArgSet(LOG_D0_IPCHI2_OWNPV), dataset_COMB_CORR_dtb))
    key_COMB.append(RooKeysPdf("key_COMB_"+str(i), "key_COMB", LOG_D0_IPCHI2_OWNPV, dataset_COMB_CORR_dtb))

#We store shapes of Log(IPCHI2) for mathced candidates in for each decay time bins here.
wspace_2 = RooWorkspace("wspace_key_shapes")
wspace_2.Print("t")
wsfile = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/Secondary_Key_Shapes.root", "recreate")
for k in key_COMB:
    wspace_2.rfimport(k) 
wspace_2.Write("wspace")

wspace_3 = RooWorkspace("wspace_hist_shapes")
wspace_3.Print("t")
wsfile = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/Secondary_Hist_Shapes.root", "recreate")
for s in hist_COMB:
    wspace_3.rfimport(s) 
wspace_3.Write("wspace")

