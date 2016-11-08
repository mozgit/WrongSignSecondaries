import ROOT
from ROOT import TFile
from ROOT import RooRealVar, RooDataSet, RooWorkspace, RooArgSet
ROOT.RooWorkspace.rfimport = getattr(ROOT.RooWorkspace, 'import')

"""
This script contains list of processed workspace files.
This list is used in Part-reco matching procedure.
Also, the files are merged in this script to the single workspace.
To keep size small, this workspace has only neccessary variables.

Note:

- Please do not modify list of files during the workflow (for example after matching procedure but before final fit) in the sake of consistency.

- Please add here adresses of files created with Create_WS.py script
  
"""

def WS_list(Save_DS = False):
    file_list = ["~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_0.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_1.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_2.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_3.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_4.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_5.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_6.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_7.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_8.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_9.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_10.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_11.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_12.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_13.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_14.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_15.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_16.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_17.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_18.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_19.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_20.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_21.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_22.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_23.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_24.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_25.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_26.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_27.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_28.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_29.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_30.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_31.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_32.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_33.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_34.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_36.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_37.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_38.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_39.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_40.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_41.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_42.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_43.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_44.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_45.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_46.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_47.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_48.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_49.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_50.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_51.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_52.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_53.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_55.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_56.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_57.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_58.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_59.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_35.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_54.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_60.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_61.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_62.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_63.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_64.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_65.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_66.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_67.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_68.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_69.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_70.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_71.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_72.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_73.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_74.root",
    #"~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/WorkSpaceD2hhNtuple_2015Turbo_MagUp_75.root"
    ]
    return file_list

def Merged_WS(Save_DS = False):
    file_list = WS_list()
    ws_file = TFile(file_list[0], "read")
    wsp = ws_file.Get("wspace")
    ws_file.Close()
    varset_comb = wsp.allVars()
    B_M = wsp.var("B_M")
    LOG_D0_IPCHI2_OWNPV = wsp.var("LOG_D0_IPCHI2_OWNPV")
    D0_TAU = wsp.var("D0_TAU")
    D0_M = wsp.var("D0_M")
    Dst_M = wsp.var("Dst_M")
    Dst_DTF_D0_CTAU = wsp.var("Dst_DTF_D0_CTAU")
    Dst_DTF_D0_M = wsp.var("Dst_DTF_D0_M")
    D0sPi_M = wsp.var("D0sPi_M")
    B_ENDVERTEX_CHI2 = wsp.var("B_ENDVERTEX_CHI2")
    DTF_D0sPi_M = wsp.var("DTF_D0sPi_M")
    Mu_PT = wsp.var("Mu_PT")
    runNumber = wsp.var("runNumber")
    
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


    datasets = {
    'RS':RooDataSet("dataset_RS", "dataset_RS",varset),
    'COMB_OS':RooDataSet("dataset_COMB_OS", "dataset_COMB_OS",varset_comb),
    'COMB_SS':RooDataSet("dataset_COMB_SS", "dataset_COMB_SS",varset_comb)
    }
    

    for f in file_list:
        print "Adding data from "+f
        ws_file = TFile(f, "read")
        wsp = ws_file.Get("wspace")
        ws_file.Close()
        datasets['RS'].append(wsp.data("dataset_RS"))
        datasets['COMB_OS'].append(wsp.data("dataset_COMB_OS"))
        datasets['COMB_SS'].append(wsp.data("dataset_COMB_SS"))
    
    if not Save_DS:
        #This is for test purpose only, normaly workspaces is saved.
        wspace = RooWorkspace("wspace")
        wspace.rfimport(varset_comb)
        wspace.rfimport(datasets['RS'])
        wspace.rfimport(datasets['WS'])
        wspace.rfimport(datasets['COMB_OS'])
        wspace.rfimport(datasets['COMB_SS'])
        print "All datasets are added but not written"
        #wspace.Write("wspace")
        return wspace
    else:
        wspace = RooWorkspace("wspace")
        wsfile = TFile("~/eos/lhcb/user/i/ikomarov/WrongSign/2015/WorkSpaces/Merged_Merged_WS.root", "recreate")
        wspace.rfimport(varset_comb)
        wspace.rfimport(varset)
        wspace.rfimport(datasets['RS'])
        wspace.rfimport(datasets['COMB_OS'])
        wspace.rfimport(datasets['COMB_SS'])
        print "All datasets are added"
        wspace.Write("wspace")
        return True

if __name__ == "__main__":
    Merged_WS(True)    
