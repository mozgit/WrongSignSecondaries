import ROOT
from ROOT import TFile, TCanvas
from ROOT import RooRealVar, RooDataSet, RooWorkspace
from ROOT import RooFit, RooDataHist, RooAddPdf, RooArgList, RooKeysPdf, RooHistPdf, RooArgSet, RooAbsReal
from ROOT import gPad
from ROOT import TH1F
from ROOT.TMath import Log
from configs.dtb import decaytime_binnning, tau, ctau, fractions_2012_TOS, fractions_2012_ATOS, decaytime_binnning_low_edge
from Merge_DS import Merged_WS
from datetime import datetime
from ROOT import gStyle
import sys
import array
from configs.cuts import preselection_cut as offline_cut
from configs.user import *
from ROOT import gROOT
from Background_Subtraction import Subtract_Distribution
gROOT.ProcessLineSync('.L functions/Johnson.cxx+')
gROOT.ProcessLineSync('.L functions/fage.cxx+')
gROOT.ProcessLineSync('.L functions/Background.cxx+')

ws_file = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/MatchedDS.root", "read")
wsp_0 = ws_file.Get("wspace")
ws_file.Close()
dataset_COMB_CORR = wsp_0.data("dataset_COMB_CORR")

ws_file0 = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/WorkSpaces/Merged_WS_Bin_0.root", "read")
wsp = ws_file0.Get("wspace")
ws_file0.Close()
start = datetime.now()

LOG_D0_IPCHI2_OWNPV = wsp.var("LOG_D0_IPCHI2_OWNPV")
Dst_DTF_D0_CTAU = wsp.var("Dst_DTF_D0_CTAU")
DTF_D0sPi_M = wsp.var("DTF_D0sPi_M")
DTF_D0sPi_M.setMax(2020)
DTF_D0sPi_M.setMin(2000)

varset_small = RooArgSet("varset_small")
varset_small.add(LOG_D0_IPCHI2_OWNPV)
varset_small.add(Dst_DTF_D0_CTAU)
varset_small.add(DTF_D0sPi_M)

#Create histogram for time bin 0
dataset_RS_0 = wsp.data("dataset_RS")
dataset_RS_0.SetName("dataset_RS_0")
print "dataset_RS_0 extraction took  "+str(datetime.now()-start)+" \n"
start = datetime.now()
hist_RS_0 = RooDataHist("hist_RS_0","hist_RS_0", RooArgSet(LOG_D0_IPCHI2_OWNPV), dataset_RS_0)
print "RooDataHist creation took  "+str(datetime.now()-start)+" \n"
start = datetime.now()
shape_RS_0 = RooHistPdf("shape_RS_0", "shape_RS_0", RooArgSet(LOG_D0_IPCHI2_OWNPV), hist_RS_0)
print "RooHistPdf creation took  "+str(datetime.now()-start)+" \n"
h_0 = hist_RS_0.createHistogram("LOG_D0_IPCHI2_OWNPV", 100)

#Fage function used to fit signal distribution
#Fix asymmetry paramters from 0 bin, leave mean and width float.
fage_mu = RooRealVar("fage_mu", "fage_mu", 0.5, 0., 1.)
fage_sigma = RooRealVar("fage_sigma", "fage_sigma", 2.0, 0.5, 5.)
fage_epsilon = RooRealVar("fage_epsilon", "fage_epsilon", 0., -1., 1.)
fage_rhol = RooRealVar("fage_rhol", "fage_rhol", 1., 0.1, 10)
fage_rhor = RooRealVar("fage_rhor", "fage_rhor", 1., 0.1, 10)
s_fage = ROOT.fage("s_fage", "s_fage", LOG_D0_IPCHI2_OWNPV, fage_mu, fage_sigma, fage_epsilon, fage_rhol, fage_rhor)
fit_hists_0 = s_fage.fitTo(hist_RS_0,RooFit.SumW2Error(True),RooFit.Save())
fage_epsilon.setConstant(True)
fage_rhol.setConstant(True)
fage_rhor.setConstant(True)

#Collection of fraction of secondaries for ctau bins
fraction_2015 = {0:[0, 0]}

for i, bin in enumerate(decaytime_binnning):

    if i == 0:
        continue
    #For test purposeses, one might use:
    #if i != 10:
    #    continue

    #Open data for given ctau bin
    ws_file0 = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/WorkSpaces/Merged_WS_Bin_"+str(i)+".root", "read")
    wsp = ws_file0.Get("wspace")
    ws_file0.Close()
    dataset_RS_dtb = wsp.data("dataset_RS")
    dataset_RS_dtb.SetName("dataset_RS_dtb")

    #Open secondary shape for given in
    start = datetime.now()
    dataset_COMB_CORR_dtb_init = RooDataSet("dataset_COMB_CORR_dtb_init","Decaytime bin"+str(i),dataset_COMB_CORR,varset_small,"Dst_DTF_D0_CTAU>"+str(bin[0]*ctau)+"&&Dst_DTF_D0_CTAU<"+str(bin[1]*ctau))
    dataset_COMB_CORR_dtb = Subtract_Distribution(dataset_COMB_CORR_dtb_init, DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV, str(i)+"_comb", True)
    dataset_COMB_CORR_dtb.SetName("dataset_COMB_CORR_dtb")
    print "Background substraction from combinatorial tool  "+str(datetime.now()-start)+" \n"

    hist_COMB = RooDataHist("hist_COMB","hist_COMB", RooArgSet(LOG_D0_IPCHI2_OWNPV), dataset_COMB_CORR_dtb)
    shape_COMB = RooHistPdf("shape_COMB", "shape_COMB", RooArgSet(LOG_D0_IPCHI2_OWNPV), hist_COMB)
    key_COMB = RooKeysPdf("key_COMB", "key_COMB", LOG_D0_IPCHI2_OWNPV, dataset_COMB_CORR_dtb)


    Prim_Yield = RooRealVar("Prim_Yield",  "Prim_Yield",   1000000,0,1e7);
    Sec_Yield = RooRealVar("Sec_Yield",  "Sec_Yield",   0,0,1e7);

    #Choise of fit model used to fit primary decays: fage (s_fage_ or histogram of 0 bin (shape_RS_0)
    #Two_hists = RooAddPdf("Two_hists", "Two_hists",  RooArgList(shape_RS_0,   key_COMB), RooArgList(Prim_Yield, Sec_Yield))
    Two_hists = RooAddPdf("Two_hists", "Two_hists",  RooArgList(s_fage,   key_COMB), RooArgList(Prim_Yield, Sec_Yield))
    
    
    LOG_D0_IPCHI2_OWNPV.setRange("All", -10, 10)
    LOG_D0_IPCHI2_OWNPV.setRange("Signal", -10, Log(9))
    LOG_D0_IPCHI2_OWNPV.setRange("Background", -10, 10)
    #N.B. Here, Signal region is one that we use for analysis, bagkround - is one with secondaries.
    #We can play with fit limits if we fail to describe signal shape properly
    #if i<8:        
    #    LOG_D0_IPCHI2_OWNPV.setRange("Background", -10, 10)
    #else:
    #    LOG_D0_IPCHI2_OWNPV.setRange("Background", Log(9), 10)

    fit_hists = Two_hists.fitTo(dataset_RS_dtb,RooFit.SumW2Error(True),RooFit.Save(), RooFit.Range("Background"))
    Bckg_int = key_COMB.createIntegral(RooArgSet(LOG_D0_IPCHI2_OWNPV), RooArgSet(LOG_D0_IPCHI2_OWNPV), "Background")
    Sig_int = key_COMB.createIntegral(RooArgSet(LOG_D0_IPCHI2_OWNPV), RooArgSet(LOG_D0_IPCHI2_OWNPV), "Signal")
    try:
        inSignal_Tot = dataset_RS_dtb.reduce(RooFit.Cut("LOG_D0_IPCHI2_OWNPV<TMath::Log(9)")).numEntries()
    except:
        inSignal_Tot = 0
    try:
        inSignal_Tot_Err = inSignal_Tot**0.5
    except:
        inSignal_Tot_Err = 0
    try:
        inSignal_Bck = Sec_Yield.getVal()/Bckg_int.getVal()*Sig_int.getVal()
    except:
        inSignal_Bck = 0
    try:
        inSignal_Bck_Err = Sec_Yield.getError()/Bckg_int.getVal()*Sig_int.getVal()
    except:
        inSignal_Bck_Err = 0
    try:
        inSignal_Frac = inSignal_Bck/inSignal_Tot
    except:
        inSignal_Frac = 0
    try:
        inSignal_Frac_Err = inSignal_Frac*((inSignal_Tot_Err/inSignal_Tot)**2+(inSignal_Bck_Err/inSignal_Bck)**2)**0.5
    except:
        inSignal_Frac_Err = 0
    #Here we write down fraction of secondaries within signal region for further use
    fraction_2015[i] = [inSignal_Frac*100, inSignal_Frac_Err*100]
    print "_-^-"*100+"_"
    print "Bin "+str(i)
    print "Background yiled in signal region:       "+str(inSignal_Bck)+"+/-"+str(inSignal_Bck_Err)
    print "Total Yield in signal region:            "+str(inSignal_Tot)+"+/-"+str(inSignal_Tot_Err)
    print "Fraction:                                "+str(inSignal_Frac)+"+/-"+str(inSignal_Frac_Err)
    print "_-^-"*100+"_"
    LOG_D0_IPCHI2_OWNPV.setRange("All", -10, 10)

    #Now, some plots:
    ipframe_1 = LOG_D0_IPCHI2_OWNPV.frame(RooFit.Title("Bin "+str(i)))
    ipframe_2 = LOG_D0_IPCHI2_OWNPV.frame(RooFit.Title("D^{*}#mu, bin "+str(i)))
    ipframe_3 = DTF_D0sPi_M.frame(RooFit.Title("Signal D* mass, bin "+str(i)))
    ipframe_4 = DTF_D0sPi_M.frame(RooFit.Title("D*_{from B} mass, bin"+str(i)))


    dataset_RS_dtb.plotOn(ipframe_1)
    Two_hists.plotOn(ipframe_1, RooFit.Components("key_COMB"), RooFit.LineColor(2),RooFit.LineWidth(4))
    Two_hists.plotOn(ipframe_1, RooFit.Components("shape_COMB"), RooFit.LineColor(2),RooFit.LineWidth(2))
    Two_hists.plotOn(ipframe_1, RooFit.Components("shape_RS_0"), RooFit.LineColor(3),RooFit.LineWidth(2))
    Two_hists.plotOn(ipframe_1, RooFit.Components("s_fage"), RooFit.LineColor(3),RooFit.LineWidth(2))
    Two_hists.plotOn(ipframe_1, RooFit.LineColor(4),RooFit.LineWidth(2)) 

    dataset_COMB_CORR_dtb.plotOn(ipframe_2)
    shape_COMB.plotOn(ipframe_2, RooFit.LineColor(2),RooFit.LineWidth(4))

    dataset_RS_dtb.plotOn(ipframe_3)

    dataset_COMB_CORR_dtb.plotOn(ipframe_4)    

    c_IP = TCanvas("c_IP","c_IP",900,900)
    c_IP.Divide(2,2)
    c_IP.cd(1)    
    ipframe_1.Draw()
    c_IP.cd(2)    
    ipframe_2.Draw()
    c_IP.cd(3)    
    ipframe_3.Draw()
    c_IP.cd(4)    
    ipframe_4.Draw()    
    c_IP.SaveAs("plots/Fit_Bin_"+str(i)+".pdf")

#This small appendix draws secondary comparision betewen 2012 and 2015 data:
h_12_TOS = TH1F("h_12_TOS", "Fraction of secondaries wihtin signal region", len(decaytime_binnning_low_edge)-1, array.array("d", decaytime_binnning_low_edge))
h_12_TOS.SetLineColor(2)
h_12_ATOS = TH1F("h_12_ATOS", "Fraction of secondaries wihtin signal region", len(decaytime_binnning_low_edge)-1, array.array("d", decaytime_binnning_low_edge))
h_12_ATOS.SetLineColor(3)
h_15 = TH1F("h_15", "Fraction of secondaries wihtin signal region", len(decaytime_binnning_low_edge)-1, array.array("d", decaytime_binnning_low_edge))
h_15.SetLineColor(1)
h_15.SetLineWidth(4)

for i, bin in enumerate(decaytime_binnning):
    h_12_TOS.SetBinContent(i+1, fractions_2012_TOS[i][0])
    h_12_ATOS.SetBinContent(i+1, fractions_2012_ATOS[i][0])
    try:
        h_15.SetBinContent(i+1, fraction_2015[i][0])
    except:
        pass
    h_12_TOS.SetBinError(i+1, fractions_2012_TOS[i][1])
    h_12_ATOS.SetBinError(i+1, fractions_2012_ATOS[i][1])
    try:
        h_15.SetBinError(i+1, fraction_2015[i][1])    
    except:
        pass

gStyle.SetOptStat(0)
c_Compare = TCanvas("c_Compare","c_Compare",900,900) 
h_12_TOS.Draw()
h_12_ATOS.Draw("SAME")
h_15.Draw("SAME")
leg = ROOT.TLegend(0.1,0.7,0.48,0.9)
leg.AddEntry(h_12_TOS,"2012 L0TOS","lp")
leg.AddEntry(h_12_ATOS,"2012 #bar{L0TOS}","lp")
leg.AddEntry(h_15,"2015","lp")
leg.Draw()
c_Compare.SaveAs("plots/Fraction_Comparison.pdf")
