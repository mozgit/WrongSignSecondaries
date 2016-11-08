#Stripping_cuts = "(D0_PT>1800)&&((P1_PT>1100) || (P2_PT>1100)) && ((P1_MINIPCHI2>8)||(P2_MINIPCHI2>8)) && (D0_MINIPCHI2<15) && (sPi_PT>110) && (sPi_MINIPCHI2 < 10) && (Dst_ENDVERTEX_CHI2 < 10)"
Stripping_cuts = "(D0_PT>2000)&&(D0_P>5000)&&((P1_PT>1500) || (P2_PT>1500)) && (Dst_ENDVERTEX_CHI2 < 100) && (P1_MINIPCHI2 > 9) && (P2_MINIPCHI2 > 9) && (D0_FDCHI2_OWNPV > 40) && (P1_isMuon == 0) && (P2_isMuon == 0)"

#Stripping_cuts = "((D0_MINIPCHI2<15))"
PID_cuts = "( P1_PIDK < -5 ) && ( P2_PIDK > 8 ) && ( sPi_PIDK < 1 ) && (D0_L0HadronDecision_TOS || D0_L0Global_TIS) && (D0_Hlt1TrackMVADecision_TOS || D0_Hlt1TwoTrackMVADecision_TOS)" #Kinemmatic cuts used to create WS
combination_cut = "( Mu_PT > 2000 ) && ( B_ENDVERTEX_CHI2 < 8 ) && ( B_M < 5100 )" #Cuts to select B->D*muny events
preselection_cut = "( DTF_D0sPi_M < 2020 )  && ( Dst_DTF_D0_M < 1889) && ( Dst_DTF_D0_M > 1841)" #Kinematic cuts (a.k.a. offline_cuts)
#preselection_cut = "( D0sPi_M < 2015 )  && ( D0_M < 1889) && ( D0_M > 1841)" #Kinematic cuts (a.k.a. offline_cuts)
 
