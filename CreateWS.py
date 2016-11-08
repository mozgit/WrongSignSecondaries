import os
import sys
import ROOT as R
from ROOT import TFile, TCanvas
from ROOT import RooRealVar, RooArgSet, RooDataSet, RooWorkspace, RooArgList, RooFormulaVar
R.RooWorkspace.rfimport = getattr(R.RooWorkspace, 'import')
import configs
from configs.dtb import tau, ctau
from configs.cuts import PID_cuts, preselection_cut, Stripping_cuts
from configs.user import user, prefix
from datetime import datetime
"""
This script transforms ntuples to RooDataSets.
Production mode suntax:
python CreateWS.py <ntuple.root> 

If you want to run it in test mode, use:
python CreateWS.py <ntuple.root> test

In production mode it will create .root file
with RooDataSet at your eos directory:
/eos/lhcb/user/<prefix>/<user>/WrongSign/2015/WorkSpaces/
In test mode, .root file will be created 
in the same directory with script.

Notes:

- Script is created accounting that eos will be mounted at your home
  lxplus directory to eos folder:
  > cd
  > eosmount eos

- Please create "/WrongSign/2015/WorkSpaces/" directory at your eos
  (Or fix address in the script below)

- Please make sure your user name is correctly indicated at configs/user.py

- During cration of RooDataSets some cuts will be applied. (see the code)
  You may find cuts at configs/cuts.py

- To use created workspaces, add file addresses to Merge_DS.py script

"""


data_file = sys.argv[1]
#id_seed is a name of input file, without .root extension
id_seed = data_file.split("/")[-1].split(".")[0]

f = TFile(data_file)
Tree_RS = f.Get("DStarKP_RS_Tuple/DStarKP_RS")
Tree_WS = f.Get("DStarKP_WS_Tuple/DStarKP_WS")
Tree_COMB_OS = f.Get("DStarMu_COMB_Tuple/DstarMu_COMB")
Tree_COMB_SS = f.Get("DStarMu_COMB_Tuple/DstarMu_COMB")

#Translation of ntuple variables to RooRealVars. 
fRun                 =       RooRealVar("fRun", "fRun", 0, 10e6)           
fEvent               =       RooRealVar("fEvent", "fEvent", 0, 10e10)     
runNumber            =       RooRealVar("runNumber", "runNumber", 0, 10e6)           
D0_M                 =       RooRealVar("D0_M", "D0_M", 1700, 2100, "MeV/c^{2}")
D0_IPCHI2_OWNPV      =       RooRealVar("D0_IPCHI2_OWNPV", "D0_IPCHI2_OWNPV", 0, 60000, "")
LOG_D0_IPCHI2_OWNPV  =       RooFormulaVar("LOG_D0_IPCHI2_OWNPV","LOG_D0_IPCHI2_OWNPV","TMath::Log(D0_IPCHI2_OWNPV)",RooArgList(D0_IPCHI2_OWNPV))
Dst_DTF_CHI2NDOF     =       RooRealVar("Dst_DTF_CHI2NDOF", "Dst_DTF_CHI2NDOF", 0, 1000)
Dst_DTF_D0_CTAU      =       RooRealVar("Dst_DTF_D0_CTAU", "Dst_DTF_D0_CTAU", 0, 20*ctau)
Dst_DTF_D0_M         =       RooRealVar("Dst_DTF_D0_M", "Dst_DTF_D0_M", 1700, 2100, "MeV/c^{2}")
Dst_DTF_Dst_M        =       RooRealVar("Dst_DTF_Dst_M", "Dst_DTF_Dst_M", 1700, 2100, "MeV/c^{2}")
Dst_DTF_P1_PX        =       RooRealVar("Dst_DTF_P1_PX", "Dst_DTF_P1_PX", -40000, 40000, "MeV/c")
Dst_DTF_P1_PY        =       RooRealVar("Dst_DTF_P1_PY", "Dst_DTF_P1_PY", -40000, 40000, "MeV/c^{2}")
Dst_DTF_P1_PZ        =       RooRealVar("Dst_DTF_P1_PZ", "Dst_DTF_P1_PZ", 0, 1800000, "MeV/c^{2}")
Dst_DTF_P2_PX        =       RooRealVar("Dst_DTF_P2_PX", "Dst_DTF_P2_PX", -40000, 40000, "MeV/c^{2}")
Dst_DTF_P2_PY        =       RooRealVar("Dst_DTF_P2_PY", "Dst_DTF_P2_PY", -40000, 40000, "MeV/c^{2}")
Dst_DTF_P2_PZ        =       RooRealVar("Dst_DTF_P2_PZ", "Dst_DTF_P2_PZ", 0, 1800000, "MeV/c^{2}")
Dst_DTF_sPi_PX       =       RooRealVar("Dst_DTF_sPi_PX", "Dst_DTF_sPi_PX", -40000, 40000, "MeV/c^{2}")
Dst_DTF_sPi_PY       =       RooRealVar("Dst_DTF_sPi_PY", "Dst_DTF_sPi_PY", -40000, 40000, "MeV/c^{2}")
Dst_DTF_sPi_PZ       =       RooRealVar("Dst_DTF_sPi_PZ", "Dst_DTF_sPi_PZ", 0, 1800000, "MeV/c^{2}")
sPi_M                =       RooRealVar("sPi_M", "sPi_M", 100, 200, "MeV/c^{2}")
D0_PE                =       RooRealVar("D0_PE", "D0_PE", 0, 500000, "MeV/c^{2}")
sPi_PE               =       RooRealVar("sPi_PE", "sPi_PE", 0, 1800000, "MeV/c^{2}")
D0_PX                =       RooRealVar("D0_PX", "D0_PX", -40000, 40000, "MeV/c^{2}")
sPi_PX               =       RooRealVar("sPi_PX", "sPi_PX", -40000, 40000, "MeV/c^{2}")
D0_PY                =       RooRealVar("D0_PY", "D0_PY", -40000, 40000, "MeV/c^{2}")
sPi_PY               =       RooRealVar("sPi_PY", "sPi_PY", -40000, 40000, "MeV/c^{2}")
D0_PZ                =       RooRealVar("D0_PZ", "D0_PZ", 0, 1800000, "MeV/c^{2}")
sPi_PZ               =       RooRealVar("sPi_PZ", "sPi_PZ", 0, 1800000, "MeV/c^{2}")
D0sPi_M              =       RooFormulaVar("D0sPi_M","D0sPi_M","TMath::Sqrt(1865**2+sPi_M**2 + 2*(D0_PE*sPi_PE - (D0_PX*sPi_PX+D0_PY*sPi_PY+D0_PZ*sPi_PZ)))",RooArgList(sPi_M, D0_PE, sPi_PE, D0_PX, sPi_PX, D0_PY, sPi_PY, D0_PZ, sPi_PZ)) 
diff_D0_PE           =       RooFormulaVar("diff_D0_PE", "diff_D0_PE", "D0_PE - TMath::Sqrt(1865**2 + (Dst_DTF_P1_PX+Dst_DTF_P2_PX)**2 + (Dst_DTF_P1_PY+Dst_DTF_P2_PY)**2 + (Dst_DTF_P1_PZ+Dst_DTF_P2_PZ)**2)", RooArgList(D0_PE, Dst_DTF_P1_PX, Dst_DTF_P2_PX, Dst_DTF_P1_PY, Dst_DTF_P2_PY, Dst_DTF_P1_PZ, Dst_DTF_P2_PZ) )
diff_sPi_PE          =       RooFormulaVar("diff_sPi_PE", "diff_sPi_PE", "sPi_PE - TMath::Sqrt(sPi_M**2 + Dst_DTF_sPi_PX**2 + Dst_DTF_sPi_PY**2 + Dst_DTF_sPi_PZ**2)",RooArgList(sPi_PE ,sPi_M ,Dst_DTF_sPi_PX ,Dst_DTF_sPi_PY ,Dst_DTF_sPi_PZ))
diff_D0_PX           =       RooFormulaVar("diff_D0_PX", "diff_D0_PX", "D0_PX - (Dst_DTF_P1_PX+Dst_DTF_P2_PX)", RooArgList(D0_PX, Dst_DTF_P1_PX, Dst_DTF_P2_PX)  )
diff_D0_PY           =       RooFormulaVar("diff_D0_PY", "diff_D0_PY", "D0_PY - (Dst_DTF_P1_PY+Dst_DTF_P2_PY)", RooArgList(D0_PY, Dst_DTF_P1_PY, Dst_DTF_P2_PY)  )
diff_D0_PZ           =       RooFormulaVar("diff_D0_PZ", "diff_D0_PZ", "D0_PZ - (Dst_DTF_P1_PZ+Dst_DTF_P2_PZ)", RooArgList(D0_PZ, Dst_DTF_P1_PZ, Dst_DTF_P2_PZ)  )
diff_sPi_PX          =       RooFormulaVar("diff_sPi_PX", "diff_sPi_PX", "sPi_PX - Dst_DTF_sPi_PX", RooArgList(sPi_PX, Dst_DTF_sPi_PX)  )
diff_sPi_PY          =       RooFormulaVar("diff_sPi_PY", "diff_sPi_PY", "sPi_PY - Dst_DTF_sPi_PY", RooArgList(sPi_PY, Dst_DTF_sPi_PY)  )
diff_sPi_PZ          =       RooFormulaVar("diff_sPi_PZ", "diff_sPi_PZ", "sPi_PZ - Dst_DTF_sPi_PZ", RooArgList(sPi_PZ, Dst_DTF_sPi_PZ)  )
Dst_DTF_D0_PE        =       RooFormulaVar("Dst_DTF_D0_PE", "Dst_DTF_D0_PE", "TMath::Sqrt(1865**2 + (Dst_DTF_P1_PX+Dst_DTF_P2_PX)**2 + (Dst_DTF_P1_PY+Dst_DTF_P2_PY)**2 + (Dst_DTF_P1_PZ+Dst_DTF_P2_PZ)**2)", RooArgList( Dst_DTF_P1_PX, Dst_DTF_P2_PX, Dst_DTF_P1_PY, Dst_DTF_P2_PY, Dst_DTF_P1_PZ, Dst_DTF_P2_PZ) )
Dst_DTF_sPi_PE       =       RooFormulaVar("Dst_DTF_sPi_PE", "Dst_DTF_sPi_PE", "TMath::Sqrt(sPi_M**2 + Dst_DTF_sPi_PX**2 + Dst_DTF_sPi_PY**2 + Dst_DTF_sPi_PZ**2)",RooArgList(sPi_M ,Dst_DTF_sPi_PX ,Dst_DTF_sPi_PY ,Dst_DTF_sPi_PZ))
Dst_DTF_D0_PX        =       RooFormulaVar("Dst_DTF_D0_PX", "Dst_DTF_D0_PX", "(Dst_DTF_P1_PX+Dst_DTF_P2_PX)", RooArgList( Dst_DTF_P1_PX, Dst_DTF_P2_PX)  )
Dst_DTF_D0_PY        =       RooFormulaVar("Dst_DTF_D0_PY", "Dst_DTF_D0_PY", "(Dst_DTF_P1_PY+Dst_DTF_P2_PY)", RooArgList( Dst_DTF_P1_PY, Dst_DTF_P2_PY)  )
Dst_DTF_D0_PZ        =       RooFormulaVar("Dst_DTF_D0_PZ", "Dst_DTF_D0_PZ", "(Dst_DTF_P1_PZ+Dst_DTF_P2_PZ)", RooArgList( Dst_DTF_P1_PZ, Dst_DTF_P2_PZ)  )
Dst_M                =       RooRealVar("Dst_M", "Dst_M", 1700, 2100, "MeV/c^{2}")
D0_TAU               =       RooRealVar("D0_TAU", "D0_TAU", 0, 20*tau, "ns")
B_M                  =       RooRealVar("B_M", "B_M", 2900, 8000, "MeV/c^{2}")
B_ENDVERTEX_CHI2     =       RooRealVar("B_ENDVERTEX_CHI2", "B_ENDVERTEX_CHI2", -1, 80)
B_ENDVERTEX_NDOF     =       RooRealVar("B_ENDVERTEX_NDOF", "B_ENDVERTEX_NDOF", 1, 10)
Mu_IPCHI2_OWNPV      =       RooRealVar("Mu_IPCHI2_OWNPV", "Mu_IPCHI2_OWNPV", 0, 8000)
Mu_IP_OWNPV          =       RooRealVar("Mu_IP_OWNPV", "Mu_IP_OWNPV", 0, 5)
Mu_PT                =       RooRealVar("Mu_PT", "Mu_PT", 0, 15000, "MeV/c")



varset = RooArgSet(D0_M)
varset.add(D0_TAU)
varset.add(runNumber)
varset.add(Dst_M)
varset.add(D0_IPCHI2_OWNPV)
varset.add(sPi_M)
varset.add(D0_PE)
varset.add(sPi_PE)
varset.add(D0_PX)
varset.add(sPi_PX)
varset.add(D0_PY)
varset.add(sPi_PY)
varset.add(D0_PZ)
varset.add(sPi_PZ)
varset.add(Dst_DTF_CHI2NDOF)
varset.add(Dst_DTF_D0_CTAU)
varset.add(Dst_DTF_D0_M)
varset.add(Dst_DTF_Dst_M)
varset.add(Dst_DTF_P1_PX)
varset.add(Dst_DTF_P1_PY)
varset.add(Dst_DTF_P1_PZ)
varset.add(Dst_DTF_P2_PX)
varset.add(Dst_DTF_P2_PY)
varset.add(Dst_DTF_P2_PZ)
varset.add(Dst_DTF_sPi_PX)
varset.add(Dst_DTF_sPi_PY)
varset.add(Dst_DTF_sPi_PZ)

varset_comb = RooArgSet(B_ENDVERTEX_CHI2)
varset_comb.add(D0_TAU)
varset_comb.add(runNumber)
varset_comb.add(D0_IPCHI2_OWNPV)
varset_comb.add(B_M)
varset_comb.add(D0_M)
varset_comb.add(sPi_M)
varset_comb.add(D0_PE)
varset_comb.add(sPi_PE)
varset_comb.add(D0_PX)
varset_comb.add(sPi_PX)
varset_comb.add(D0_PY)
varset_comb.add(sPi_PY)
varset_comb.add(D0_PZ)
varset_comb.add(sPi_PZ)
varset_comb.add(Mu_IPCHI2_OWNPV)
varset_comb.add(Mu_IP_OWNPV)
varset_comb.add(Mu_PT)


#We apply some cuts here
outfile = TFile("/tmp/"+user+"/temp"+id_seed+".root", "RECREATE")
Tree_temp = Tree_RS.CopyTree("(Dst_DTF_P1_PX > -40000) "+" && "+PID_cuts+"&"+Stripping_cuts)
dataset_RS = RooDataSet("dataset_RS","dataset_RS",Tree_temp,varset)
Tree_temp = Tree_WS.CopyTree("(Dst_DTF_P1_PX > -40000) "+" && "+PID_cuts+"&"+Stripping_cuts)
dataset_WS = RooDataSet("dataset_WS","dataset_WS",Tree_temp,varset)
Tree_temp = Tree_COMB_OS.CopyTree("(Dst_ID*Mu_ID>0)"+" && "+PID_cuts+"&"+Stripping_cuts)
dataset_COMB_OS = RooDataSet("dataset_COMB_OS","dataset_COMB_OS",Tree_temp,varset_comb)
Tree_temp = Tree_COMB_SS.CopyTree("(Dst_ID*Mu_ID<0)"+" && "+PID_cuts+"&"+Stripping_cuts)
dataset_COMB_SS = RooDataSet("dataset_COMB_SS","dataset_COMB_SS",Tree_temp,varset_comb)

#Also, we need to add some generic variables:
dataset_WS.addColumn(LOG_D0_IPCHI2_OWNPV).setRange(-10, 10)
dataset_RS.addColumn(LOG_D0_IPCHI2_OWNPV).setRange(-10, 10)
dataset_COMB_SS.addColumn(LOG_D0_IPCHI2_OWNPV).setRange(-10, 10)
dataset_COMB_OS.addColumn(LOG_D0_IPCHI2_OWNPV).setRange(-10, 10)
#
dataset_WS.addColumn(D0sPi_M).setRange(1700, 2020)
dataset_RS.addColumn(D0sPi_M).setRange(1700, 2020)
dataset_COMB_SS.addColumn(D0sPi_M).setRange(1850, 2200)
dataset_COMB_OS.addColumn(D0sPi_M).setRange(1850, 2200)
dataset_WS.addColumn(Dst_DTF_D0_PE).setRange(0, 180000)
dataset_WS.addColumn(Dst_DTF_sPi_PE).setRange(0, 180000)
dataset_WS.addColumn(Dst_DTF_D0_PX).setRange(-40000,40000)
dataset_WS.addColumn(Dst_DTF_D0_PY).setRange(-40000,40000)
dataset_WS.addColumn(Dst_DTF_D0_PZ).setRange(-40000,40000)
dataset_RS.addColumn(Dst_DTF_D0_PE).setRange(0, 180000)
dataset_RS.addColumn(Dst_DTF_sPi_PE).setRange(0, 180000)
dataset_RS.addColumn(Dst_DTF_D0_PX).setRange(-40000,40000)
dataset_RS.addColumn(Dst_DTF_D0_PY).setRange(-40000,40000)
dataset_RS.addColumn(Dst_DTF_D0_PZ).setRange(-40000,40000)
dataset_COMB_SS.addColumn(Dst_DTF_D0_PE).setRange(0, 180000)
dataset_COMB_SS.addColumn(Dst_DTF_sPi_PE).setRange(0, 180000)
dataset_COMB_SS.addColumn(Dst_DTF_D0_PX).setRange(-40000,40000)
dataset_COMB_SS.addColumn(Dst_DTF_D0_PY).setRange(-40000,40000)
dataset_COMB_SS.addColumn(Dst_DTF_D0_PZ).setRange(-40000,40000)
dataset_COMB_OS.addColumn(Dst_DTF_D0_PE).setRange(0, 180000)
dataset_COMB_OS.addColumn(Dst_DTF_sPi_PE).setRange(0, 180000)
dataset_COMB_OS.addColumn(Dst_DTF_D0_PX).setRange(-40000,40000)
dataset_COMB_OS.addColumn(Dst_DTF_D0_PY).setRange(-40000,40000)
dataset_COMB_OS.addColumn(Dst_DTF_D0_PZ).setRange(-40000,40000)
#
DTF_D0sPi_M          =       RooFormulaVar("DTF_D0sPi_M","DTF_D0sPi_M","TMath::Sqrt(1865**2+sPi_M**2 + 2*(Dst_DTF_D0_PE*Dst_DTF_sPi_PE - (Dst_DTF_D0_PX*Dst_DTF_sPi_PX+Dst_DTF_D0_PY*Dst_DTF_sPi_PY+Dst_DTF_D0_PZ*Dst_DTF_sPi_PZ)))",RooArgList(sPi_M, Dst_DTF_D0_PE, Dst_DTF_sPi_PE, Dst_DTF_D0_PX, Dst_DTF_sPi_PX, Dst_DTF_D0_PY, Dst_DTF_sPi_PY, Dst_DTF_D0_PZ, Dst_DTF_sPi_PZ)) 
dataset_WS.addColumn(DTF_D0sPi_M).setRange(1700, 2100)
dataset_RS.addColumn(DTF_D0sPi_M).setRange(1700, 2100)


try:
    test_mode = sys.argv[2]
except:
    test_mode = False

wspace = RooWorkspace("wspace")
wspace.Print("t")
if not test_mode:
    #Here is address of output file
    wsfile = TFile("/afs/cern.ch/user/"+prefix+"/"+user+"/eos/lhcb/user/"+prefix+"/"+user+"/WrongSign/2015/WorkSpaces/WorkSpace"+id_seed+".root", "recreate")
else:
    wsfile = TFile("WorkSpace"+id_seed+".root", "recreate")
wspace.rfimport(varset)
wspace.rfimport(varset_comb)
wspace.rfimport(dataset_COMB_OS)
wspace.rfimport(dataset_COMB_SS)
wspace.rfimport(dataset_WS)
wspace.rfimport(dataset_RS)
wspace.Write("wspace")
os.remove("/tmp/"+user+"/temp"+id_seed+".root")

