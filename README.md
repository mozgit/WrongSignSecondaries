# WrongSignSecondaries

Sequence of scripts:

1) Create_Workspaces.sh - This runs CreateWS.py which transform ntuples to RooDataSet
2) Matching.py - This match part reco B decays to D* candidates and provide datasets used for secondary shape.
3) Merge_DS.py - merge all datasets to single dataset
4) Split_DS.py - split single dataset in ctau bins
5) Estimate_Secondaries.py - Provide information on fraction of secondaries.
