#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <vector>
#include "TMath.h"
#include "TMinuit.h"
#include "TTree.h"
#include "TFile.h"
#include "TString.h"
#include "TH1.h"
#include "TF1.h"

std::vector<double> mResult = {0., 0., 0., 0.};
std::vector<double> mError = {0., 0., 0., 0.};
TTree *tt;
Float_t mResidual, mLocalPoint[3], mGlobalPoint[3];
Long64_t mEvents;

double MuonResidualsFitter_logPureGaussian(double residual, double center, double sigma) {
  sigma = fabs(sigma);
  static const double cgaus = 0.5 * log(2.*M_PI);
  return (-pow(residual - center, 2) * 0.5 / sigma / sigma) - cgaus - log(sigma);
}

double getResidual(double delta_x, double delta_y, double delta_phiz, double track_x, double track_y, double R) {
  return delta_x - (track_x/R - 3.*pow(track_x/R, 3)) * delta_y - track_y * delta_phiz;
}

void MuonResiduals3DOFFitter_FCN(int &npar, double *gin, double &fval, double *par, int iflag) {
  const double dx = par[0];
  const double dy = par[1];
  const double dphiz = par[2];
  const double sig = par[3];
  fval = 0.;
  for (Long64_t i=0; i<mEvents; i++) {
    tt->GetEntry(i);
    double residual = mResidual; 
    double trackX = mLocalPoint[0]; 
    double trackY = mLocalPoint[1]; 
    double R = pow(pow(mGlobalPoint[0],2) + pow(mGlobalPoint[1],2), 0.5);
    double residpeak = getResidual(dx, dy, dphiz, trackX, trackY, R);
    fval += -1.*MuonResidualsFitter_logPureGaussian(residual, residpeak, sig);
  }
}

void doFit(bool doDx, bool doDy, bool doDphiz) {
  TMinuit mfit(4);
  mfit.SetFCN(MuonResiduals3DOFFitter_FCN);
  double par[4] = {0., 0., 0., 0.5};
  mfit.DefineParameter(0, "dx", par[0], 0.1, 0, 0);
  mfit.DefineParameter(1, "dy", par[1], 0.1, 0, 0);
  mfit.DefineParameter(2, "dphiz", par[2], 0.001, 0, 0);
  mfit.DefineParameter(3, "sig", par[3], 0.01, 0, 0);
  mfit.FixParameter(3);
  if (!doDx) mfit.FixParameter(0);
  if (!doDy) mfit.FixParameter(1);
  if (!doDphiz) mfit.FixParameter(2);
  
  double arglist[10];
  int ierflg;
  int smierflg;
  for (int i = 0; i < 10; i++) arglist[i] = 0.;
  arglist[0] = 0.5;
  ierflg = 0;
  smierflg = 0;
  mfit.mnexcm("SET ERR", arglist, 1, ierflg);
  
  for (int i = 0; i < 10; i++) arglist[i] = 0.;
  arglist[0] = 2;
  ierflg = 0;
  mfit.mnexcm("SET STR", arglist, 1, ierflg);
  
  bool try_again = false;
  for (int i = 0; i < 10; i++) arglist[i] = 0.;
  arglist[0] = 50000;
  ierflg = 0;
  mfit.mnexcm("MIGRAD", arglist, 1, ierflg);
  if (ierflg != 0) try_again = true;
  
  if (try_again){
    std::cout << "try again" << std::endl;
    for (int i = 0; i < 10; i++) arglist[i] = 0.;
    arglist[0] = 50000;
    mfit.mnexcm("MIGRAD", arglist, 1, smierflg);
  }
  
  Double_t fmin, fedm, errdef;
  Int_t npari, nparx, istat;
  mfit.mnstat(fmin, fedm, errdef, npari, nparx, istat);
  if (istat != 3) {
    for (int i = 0; i < 10; i++) arglist[i] = 0.;
    ierflg = 0;
    mfit.mnexcm("HESSE", arglist, 0, ierflg);
  }
  
  for (int i = 0; i < 3; i++){
    double v, e;
    mfit.GetParameter(i, v, e);
    mResult[i] = v;
    mError[i] = e;
  }
}

int main() {
  //////////////////////////////////////////////////////////////////////////////////////////
  //Input root file name
  //const char* input_name = "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_before_alignment/merged_all.root";
  const char* input_name = "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_iteration1_after_alignment_392278-393087/260311_203216/merged.root";
  //Tree name
  const char* tree_name = "analyzer/ME21Seg_Prop";
  //Output file prefix
  const char* outname_prefix = "Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop";
  //Cuts on full tree in first cloning step
  const char* cuts = "muon_pt > 5 && abs(RdPhi) < 100 && has_fidcut";
  //Option to turn on or off 3 dof alignments
  bool doDx = true;
  bool doDy = true;
  bool doDphiz = true;
  //Layer level vs chamber level
  bool byLayer = true;
  //Number of cuts to fit on
  int nCuts = 2;
  //////////////////////////////////////////////////////////////////////////////////////////
  
  int max_layer = 2;
  if(byLayer) max_layer = 3;
  
  TFile *tf = new TFile(input_name);
  TTree *tmpTr = (TTree*)tf->Get(tree_name);
  
  //Create tmp files to stop memory errors, basic cuts on full Tree
  TFile* tmpTF = new TFile("tmp1.root","recreate");
  std::cout << "Copying Tree with cuts: " << cuts << std::endl;
  TTree *cutEn = tmpTr->CopyTree(Form(cuts));
  std::cout << "Copied tree with " << cutEn->GetEntries() << " entries" << std::endl;
  std::cout << "Closing input" << std::endl;
  tf->Close();
  
  for (int nCut = 1; nCut < nCuts; nCut++) {
    std::cout << "\n========================================" << std::endl;
    std::cout << "Starting cut number " << nCut << std::endl;
    std::cout << "Current number of entries = " << cutEn->GetEntries() << std::endl;
    
    if(nCut == 1){
      std::cout << "nCut 1, using full file" << std::endl;
    }
    else{
      std::cout << "Slimming tmp file" << std::endl;
      int total_entries = cutEn->GetEntries();
      int nCut_entries = int(total_entries/2.0);
      std::cout << "nCut = " << nCut << std::endl;
      std::cout << "total_entries = " << total_entries << std::endl;
      std::cout << "nCut_entries = " << nCut_entries << std::endl;
      std::cout << "Taking first half" << std::endl;
      cutEn = cutEn->CloneTree(nCut_entries);
    }
    
    std::cout << "New number of entries = " << cutEn->GetEntries() << std::endl;
    
    // Get unique chamber DetIds from the tree
    std::cout << "\nExtracting unique chamber DetIds..." << std::endl;
    std::set<int> chamberIds;
    cutEn->Draw("rechit_detId", "", "goff");
    Int_t nEntries = cutEn->GetSelectedRows();
    Double_t *detIds = cutEn->GetV1();
    for(Int_t i = 0; i < nEntries; i++){
      chamberIds.insert((int)detIds[i]);
    }
    std::cout << "Found " << chamberIds.size() << " unique chambers" << std::endl;
    
    // Create output CSV files
    std::ofstream myfile;
    std::ofstream myerrorfile;
    std::cout << "Creating CSV file " << Form("%s.csv", outname_prefix) << std::endl;
    std::cout << "Creating error CSV file " << Form("%s_error.csv", outname_prefix) << std::endl;
    myfile.open(Form("%s.csv", outname_prefix));
    myerrorfile.open(Form("%s_error.csv", outname_prefix));
    
    double dx, dy, dz, dphix, dphiy, dphiz;
    double dx_error, dy_error, dz_error, dphix_error, dphiy_error, dphiz_error;
    dz = 0.0; dphix = 0.0; dphiy = 0.0;
    dz_error = 0.0; dphix_error = 0.0; dphiy_error = 0.0;
    
    // Loop over unique chamber DetIds
    std::cout << "\nStarting Chamber loop" << std::endl;
    int chamberCounter = 0;
    for(auto detId : chamberIds){
      chamberCounter++;
      std::cout << "\n--- Processing chamber " << chamberCounter << "/" << chamberIds.size() 
                << " (DetId=" << detId << ") ---" << std::endl;
      
      for (int k = 1; k < max_layer; k++){        // Layer loop
        std::cout << "  Layer " << k << std::endl;
        
        TFile* tmpTF2 = new TFile("tmp2.root","recreate");
        TTree* tt_tmp;
        
        if(byLayer){
          tt_tmp = cutEn->CopyTree(Form("rechit_detId==%d && rechit_location[3]==%d", detId, k));
        }
        else{
          tt_tmp = cutEn->CopyTree(Form("rechit_detId==%d", detId));
        }
        
        std::cout << "  Entries in this chamber/layer: " << tt_tmp->GetEntries() << std::endl;
        
        if (tt_tmp->GetEntries() < 10){
          std::cout << "  Skipping - too few entries" << std::endl;
          delete tt_tmp;
          delete tmpTF2;
          continue;
        }
        
        // New hist of RdPhi to get STD and MEAN
        TH1F *h1 = new TH1F("h1", "h1 title", 100, -20, 20);
        tt_tmp->Project("h1", "RdPhi", "");
        
        // Fit RdPhi to get STD and MEAN
        TF1 f1 = TF1("f1", "gaus", -2, 2);
        f1.SetParLimits(1, -2, 2);
        f1.SetParLimits(2, 0, 2);
        h1->Fit("f1", "RQ");
        float fitMean = f1.GetParameter(1);
        float fitStd = f1.GetParameter(2);
        
        std::cout << "  Fit Mean: " << fitMean << ", Std: " << fitStd << std::endl;
        
        // Copy only RdPhi within 1.6sigma of mean
        tt = tt_tmp->CopyTree(Form("RdPhi <= (%f + (1.6*%f)) && RdPhi >= (%f - (1.6*%f))", 
                                   fitMean, fitStd, fitMean, fitStd));
        
        std::cout << "  After sigma cut: " << tt->GetEntries() << " entries" << std::endl;
        
        // If there are no events on the chamber it is skipped
        if (tt->GetEntries() == 0){
          if(byLayer){
            myfile << detId << k << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                   << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
            myerrorfile << detId << k << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                        << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
          }
          else{
            myfile << detId << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                   << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
            myerrorfile << detId << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                        << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
          }
          delete h1;
          delete tt_tmp;
          delete tmpTF2;
          continue;
        }
        
        // Get variables for running Fit
        tt->SetBranchAddress("RdPhi", &mResidual);
        tt->SetBranchAddress("prop_LP", &mLocalPoint);
        tt->SetBranchAddress("prop_GP", &mGlobalPoint);
        mEvents = tt->GetEntries();
        
        std::cout << "  Running fit..." << std::endl;
        doFit(doDx, doDy, doDphiz);
        
        dx = mResult[0];
        dx_error = mError[0];
        dy = mResult[1];
        dy_error = mError[1];
        dphiz = mResult[2];
        dphiz_error = mError[2];
        
        std::cout << "  Results: dx=" << dx << " dy=" << dy << " dphiz=" << dphiz << std::endl;
        
        // Save alignment solutions to csv
        if(byLayer){
          myfile << detId << k << ", " << dx << ", " << dy << ", " << dz << ", " 
                 << dphix << ", " << dphiy << ", " << dphiz << ", " << mEvents << "\n";
          myerrorfile << detId << k << ", " << dx_error << ", " << dy_error << ", " << dz_error << ", " 
                      << dphix_error << ", " << dphiy_error << ", " << dphiz_error << ", " << mEvents << "\n";
        }
        else{
          myfile << detId << ", " << dx << ", " << dy << ", " << dz << ", " 
                 << dphix << ", " << dphiy << ", " << dphiz << ", " << mEvents << "\n";
          myerrorfile << detId << ", " << dx_error << ", " << dy_error << ", " << dz_error << ", " 
                      << dphix_error << ", " << dphiy_error << ", " << dphiz_error << ", " << mEvents << "\n";
        }
        
        delete h1;
        delete tt_tmp;
        delete tmpTF2;
      }
    }
    
    myfile.close();
    myerrorfile.close();
    std::cout << "\n========================================" << std::endl;
    std::cout << "Finished cut number " << nCut << std::endl;
    std::cout << "CSV files written successfully" << std::endl;
  }
  
  delete tmpTF;
  std::cout << "\nAll done!" << std::endl;
  return 0;
}