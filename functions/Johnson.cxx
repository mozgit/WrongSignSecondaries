/***************************************************************************** 
 * Project: RooFit                                                           * 
 *                                                                           * 
 * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/ 

// Your description goes here... 

#include "Riostream.h" 

#include "Johnson.h" 
#include "RooAbsReal.h" 
#include "RooAbsCategory.h" 
#include <math.h> 
#include "TMath.h" 

ClassImp(Johnson) 

 Johnson::Johnson(const char *name, const char *title, 
                        RooAbsReal& _m,
                        RooAbsReal& _mu,
                        RooAbsReal& _sigma,
                        RooAbsReal& _delta,
                        RooAbsReal& _gamma):
   RooAbsPdf(name,title), 
   m("m","m",this,_m),
   mu("mu","mu",this,_mu),
   sigma("sigma","sigma",this,_sigma),
   delta("delta","delta",this,_delta),
   gamma("gamma","gamma",this,_gamma)
 { 
 } 


 Johnson::Johnson(const Johnson& other, const char* name) :  
   RooAbsPdf(other,name), 
   m("m",this,other.m),
   mu("mu",this,other.mu),
   sigma("sigma",this,other.sigma),
   delta("delta",this,other.delta),
   gamma("gamma",this,other.gamma)
 { 
 } 



 Double_t Johnson::evaluate() const 
 { 
   // ENTER EXPRESSION IN TERMS OF VARIABLE ARGUMENTS HERE 
  Double_t z = (m - mu)/sigma;
  Double_t f = TMath::Power(z*z+1, 0.5);
  Double_t arcsh = log(z + f);
  Double_t t = - (gamma + delta * arcsh)/2.;
  return exp(t) / f;

 } 


