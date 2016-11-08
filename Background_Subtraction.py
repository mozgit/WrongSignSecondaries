from Merge_DS import Merged_WS
import ROOT
from ROOT import TFile, TCanvas
from ROOT import RooRealVar, RooDataSet, RooWorkspace
from ROOT import RooFit, RooDataHist, RooAddPdf, RooArgList, RooKeysPdf, RooHistPdf, RooArgSet, RooAbsData
from ROOT import gROOT
from datetime import datetime
gROOT.ProcessLineSync('.L functions/Johnson.cxx+')
gROOT.ProcessLineSync('.L functions/Background.cxx+')
from configs.cuts import preselection_cut as offline_cut
"""
This is simple script to perform combinatorial subtraction from log IPCHI2 distribution.
Idea is sraight-forward:
- Fit mass distribution (here, we use three gaussians for signal and generic shape for the Background)
- Estimate number of combinatorials in signal region
- Reweight candidates from background region with negative weights to correct this
"""

def Subtract_Distribution(dataset, DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV, bin = "undefined", silent = False):

    dataset_sig = RooDataSet("dataset_sig", "Signal region",dataset, RooArgSet(DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV) ," ( DTF_D0sPi_M < 2015 ) ")
    dataset_bckg = RooDataSet("dataset_bckg", "Background region",dataset, RooArgSet(DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV) ," ( DTF_D0sPi_M > 2015 ) && ( DTF_D0sPi_M < 2020 ) ")

    #Introduce fit variables
    ## Johnson parameters
    J_mu = RooRealVar("J_mu","J_mu",  2011, 2000, 2020)
    J_sigma = RooRealVar("J_sigma","J_sigma", 0.045, 0.01, 0.1)
    J_delta = RooRealVar("J_delta","J_delta", 0., -1, 1)
    J_gamma = RooRealVar("J_gamma","J_gamma", 0., -1, 1)

    ## Gaussian parameters

    G1_mu = RooRealVar("G1_mu","G1_mu", 2010, 2008, 2012)
    G1_sigma = RooRealVar("G1_sigma","G1_sigma", 1.0, 0.01, 5)
    G2_mu = RooRealVar("G2_mu","G2_mu", 2010, 2008, 2012)
    G2_sigma = RooRealVar("G2_sigma","G2_sigma", 0.4, 0.01, 5)
    G3_mu = RooRealVar("G3_mu","G3_mu", 2010, 2008, 2012)
    G3_sigma = RooRealVar("G3_sigma","G3_sigma", 0.2, 0.01, 5)

    ## Signal yields ratios
    fJ = RooRealVar("fJ","fJ", 0.5, 0., 1)
    fG1 = RooRealVar("fG1","fG1", 0.5, 0., 1)
    fG2 = RooRealVar("fG2","fG2", 0.5, 0., 1)

    ##Background parameters
    B_b = RooRealVar("B_b","B_b", 1.09, 0.9, 1.5)
    B_c = RooRealVar("B_c","B_c", 0.0837, 0.01, 0.2)

    ##Total yield
    N_S = RooRealVar("N_S","N_S", 0.6*dataset.numEntries(), 0, 1.1*dataset.numEntries())
    N_B = RooRealVar("N_B","N_B", 0.3*dataset.numEntries(), 0, 1.1*dataset.numEntries())



    #Define shapes
    s_Johnson = ROOT.Johnson("s_Johnson", "s_Johnson", DTF_D0sPi_M, J_mu, J_sigma, J_delta, J_gamma)
    s_Gauss1  = ROOT.RooGaussian("s_Gauss1","s_Gauss1", DTF_D0sPi_M, G1_mu, G1_sigma)
    s_Gauss2  = ROOT.RooGaussian("s_Gauss2","s_Gauss2", DTF_D0sPi_M, G2_mu, G2_sigma)
    s_Gauss3  = ROOT.RooGaussian("s_Gauss3","s_Gauss3", DTF_D0sPi_M, G3_mu, G3_sigma)
    s_Background = ROOT.Background("s_Background", "s_Background", DTF_D0sPi_M, B_b, B_c)
    s_Signal  = RooAddPdf("s_Signal", "s_Signal", RooArgList(s_Gauss1, s_Gauss2, s_Gauss3), RooArgList(fG1, fG2), True)
    s_Total = RooAddPdf("s_Total", "s_Total", RooArgList(s_Signal, s_Background), RooArgList(N_S, N_B))

    dataset_binned = RooDataHist("dataset_binned","Binned data", RooArgSet(DTF_D0sPi_M), dataset)

    #Fit shapes
    fit_hists = s_Total.fitTo(dataset_binned,RooFit.SumW2Error(True),RooFit.Save())
    if not silent:
        ipframe_1 = DTF_D0sPi_M.frame(RooFit.Title("Fit example"))
        dataset_binned.plotOn(ipframe_1)
        s_Total.plotOn(ipframe_1, RooFit.Components("s_Signal"), RooFit.LineColor(2),RooFit.LineWidth(4))
        s_Total.plotOn(ipframe_1, RooFit.Components("s_Johnson"), RooFit.LineColor(5),RooFit.LineWidth(2), RooFit.LineStyle(3))
        s_Total.plotOn(ipframe_1, RooFit.Components("s_Gauss1"), RooFit.LineColor(6),RooFit.LineWidth(2), RooFit.LineStyle(3))
        s_Total.plotOn(ipframe_1, RooFit.Components("s_Gauss2"), RooFit.LineColor(7),RooFit.LineWidth(2), RooFit.LineStyle(3))
        s_Total.plotOn(ipframe_1, RooFit.Components("s_Gauss3"), RooFit.LineColor(8),RooFit.LineWidth(2), RooFit.LineStyle(3))
        s_Total.plotOn(ipframe_1, RooFit.Components("s_Background"), RooFit.LineColor(4),RooFit.LineWidth(4))
        s_Total.plotOn(ipframe_1, RooFit.LineColor(1), RooFit.LineWidth(4))


    DTF_D0sPi_M.setRange("Background_region", 2015, 2020)
    DTF_D0sPi_M.setRange("Signal_region", 2002, 2015)

    Bckg_int = s_Background.createIntegral(RooArgSet(DTF_D0sPi_M), RooArgSet(DTF_D0sPi_M), "Background_region")
    Sig_int = s_Background.createIntegral(RooArgSet(DTF_D0sPi_M), RooArgSet(DTF_D0sPi_M), "Signal_region")

    w = RooRealVar("w","w",-1,1)
    w.setVal(1)
    dataset_sig.addColumn(w, False)
    w.setVal(-float(Sig_int.getVal())/float(Bckg_int.getVal()))
    dataset_bckg.addColumn(w, False)

    dataset_all = RooDataSet("dataset_all", "dataset_all",dataset_bckg, RooArgSet(DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV, w), "1>0", "w")
    dataset_all.append(dataset_sig)
    if not silent:
        ipframe_2 = LOG_D0_IPCHI2_OWNPV.frame(RooFit.Title("IPChi2 distribution"))
        dataset_bckg.plotOn(ipframe_2, RooFit.LineColor(4), RooFit.MarkerColor(4))
        dataset_all.plotOn(ipframe_2, RooFit.LineColor(3), RooFit.MarkerColor(3))
        dataset_sig.plotOn(ipframe_2, RooFit.LineColor(2), RooFit.MarkerColor(2))
    
        c1 = TCanvas("c1","c1",900,900)
        ipframe_1.Draw()
        c1.SaveAs("plots/Subtraction_Control/Bin_"+str(bin)+"_frame1.pdf")
        c1.SaveAs("plots/Subtraction_Control/Bin_"+str(bin)+"_frame1_C.C")
        c2 = TCanvas("c2","c2",900,900)
        ipframe_2.Draw()
        c2.SaveAs("plots/Subtraction_Control/Bin_"+str(bin)+"_frame2.pdf")    
        c2.SaveAs("plots/Subtraction_Control/Bin_"+str(bin)+"_frame2_C.C")  
        ipframe_1.SaveAs("plots/Subtraction_Control/Bin_"+str(bin)+"_ipframe1.C")
        ipframe_2.SaveAs("plots/Subtraction_Control/Bin_"+str(bin)+"_ipframe2.C")

    return dataset_all    


if __name__ == "__main__":
    start = datetime.now()
    wsp = Merged_WS()
    print "Merging took  "+str(datetime.now()-start)+" \n"
    DTF_D0sPi_M = wsp.var("DTF_D0sPi_M")
    Dst_DTF_D0_M = wsp.var("Dst_DTF_D0_M")
    LOG_D0_IPCHI2_OWNPV = wsp.var("LOG_D0_IPCHI2_OWNPV")
    DTF_D0sPi_M.setMax(2020)
    DTF_D0sPi_M.setMin(2000)
    dataset_RS = wsp.data("dataset_RS")
    dataset_RS_0 = RooDataSet("dataset_RS_0", "Decaytime bin 0",dataset_RS, RooArgSet(DTF_D0sPi_M, Dst_DTF_D0_M, LOG_D0_IPCHI2_OWNPV) ," ( Dst_DTF_D0_M < 1889) && ( Dst_DTF_D0_M > 1841)")
    frame = Subtract_Distribution(dataset_RS_0, DTF_D0sPi_M, LOG_D0_IPCHI2_OWNPV)
    frame.Draw()
