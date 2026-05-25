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
  for (int i = 0; i < 10; i++) arglist[i] = 0.;
  arglist[0] = 0.5;
  mfit.mnexcm("SET ERR", arglist, 1, ierflg);
  
  for (int i = 0; i < 10; i++) arglist[i] = 0.;
  arglist[0] = 2;
  mfit.mnexcm("SET STR", arglist, 1, ierflg);
  
  bool try_again = false;
  for (int i = 0; i < 10; i++) arglist[i] = 0.;
  arglist[0] = 50000;
  mfit.mnexcm("MIGRAD", arglist, 1, ierflg);
  if (ierflg != 0) try_again = true;
  
  if (try_again){
    std::cout << "try again" << std::endl;
    for (int i = 0; i < 10; i++) arglist[i] = 0.;
    arglist[0] = 50000;
    mfit.mnexcm("MIGRAD", arglist, 1, ierflg);
  }
  
  Double_t fmin, fedm, errdef;
  Int_t npari, nparx, istat;
  mfit.mnstat(fmin, fedm, errdef, npari, nparx, istat);
  if (istat != 3) {
    for (int i = 0; i < 10; i++) arglist[i] = 0.;
    mfit.mnexcm("HESSE", arglist, 0, ierflg);
  }
  
  for (int i = 0; i < 3; i++){
    double v, e;
    mfit.GetParameter(i, v, e);
    mResult[i] = v;
    mError[i] = e;
  }
}

// Helper function to create simple CSC DetId
int createSimpleCSCDetId(int endcap, int station, int ring, int chamber, int layer) {
    int sign = (endcap == 2) ? -1 : +1;  // 1=ME+, 2=ME-
    int stationRing = station * 10 + ring;  // 21 for ME2/1
    int detId = stationRing * 1000 + chamber * 10 + layer;
    return sign * detId;
}

int main() {
  //////////////////////////////////////////////////////////////////////////////////////////
  // Input root file name
  const char* input_name = "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_before_alignment/merged_all.roott";
  
  // Tree name - ME21 CSC segments
  const char* tree_name = "analyzer/ME21Seg";  // Adjust to your tree name
  
  // Output file prefix
  const char* outname_prefix = "ME21_CSC_alignment";
  
  // Cuts on full tree
  const char* cuts = "muon_pt > 5 && abs(seg_RdPhi) < 100";  // Adjust branch names
  
  // Alignment options
  bool doDx = true;
  bool doDy = true;
  bool doDphiz = true;
  
  // CSC has 6 layers per chamber
  bool byLayer = true;
  int max_layer = 7;  // Layers 1-6
  
  int nCuts = 2;
  //////////////////////////////////////////////////////////////////////////////////////////
  
  TFile *tf = new TFile(input_name);
  TTree *tmpTr = (TTree*)tf->Get(tree_name);
  
  // Create tmp files with cuts
  TFile* tmpTF = new TFile("tmp1.root","recreate");
  std::cout << "Copying Tree with cuts: " << cuts << std::endl;
  TTree *cutEn = tmpTr->CopyTree(Form(cuts));
  std::cout << "Copied tree with " << cutEn->GetEntries() << " entries" << std::endl;
  tf->Close();
  
  for (int nCut = 1; nCut < nCuts; nCut++) {
    std::cout << "\n======================================== " << std::endl;
    std::cout << "Starting cut number " << nCut << std::endl;
    std::cout << "Current number of entries = " << cutEn->GetEntries() << std::endl;
    
    if(nCut == 1){
      std::cout << "nCut 1, using full file" << std::endl;
    }
    else{
      std::cout << "Slimming tmp file" << std::endl;
      int total_entries = cutEn->GetEntries();
      int nCut_entries = int(total_entries/2.0);
      cutEn = cutEn->CloneTree(nCut_entries);
    }
    
    std::cout << "New number of entries = " << cutEn->GetEntries() << std::endl;
    
    // Create output CSV files
    std::ofstream myfile;
    std::ofstream myerrorfile;
    std::cout << "Creating CSV file " << Form("%s.csv", outname_prefix) << std::endl;
    myfile.open(Form("%s.csv", outname_prefix));
    myerrorfile.open(Form("%s_error.csv", outname_prefix));
    
    double dx, dy, dz, dphix, dphiy, dphiz;
    double dx_error, dy_error, dz_error, dphix_error, dphiy_error, dphiz_error;
    dz = 0.0; dphix = 0.0; dphiy = 0.0;
    dz_error = 0.0; dphix_error = 0.0; dphiy_error = 0.0;
    
    // Loop over ME2/1 chambers
    std::cout << "\nStarting Chamber loop" << std::endl;
    
    for (int j = -1; j < 2; j = j + 2){        // Endcap: -1 (ME-), +1 (ME+)
      int endcap = (j == -1) ? 2 : 1;          // Convert to CMSSW convention
      
      for (int i = 1; i <= 18; i++){           // ME2/1 has 18 chambers per endcap
        for (int k = 1; k < max_layer; k++){   // Layers 1-6
          
          // Create simple DetId
          int detId = createSimpleCSCDetId(endcap, 2, 1, i, k);
          
          std::cout << "\n--- Processing ME" << (j<0?"-":"+") << "2/1" 
                    << " Chamber " << i << " Layer " << k 
                    << " (DetId=" << detId << ") ---" << std::endl;
          
          TFile* tmpTF2 = new TFile("tmp2.root","recreate");
          TTree* tt_tmp;
          
          // Select data for this chamber/layer
          // NOTE: You need to adjust these branch names to match your tree!
          if(byLayer){
            tt_tmp = cutEn->CopyTree(Form("seg_endcap==%d && seg_station==2 && seg_ring==1 && seg_chamber==%d && seg_layer==%d", 
                                          endcap, i, k));
          }
          else{
            tt_tmp = cutEn->CopyTree(Form("seg_endcap==%d && seg_station==2 && seg_ring==1 && seg_chamber==%d", 
                                          endcap, i));
          }
          
          std::cout << "  Entries: " << tt_tmp->GetEntries() << std::endl;
          
          if (tt_tmp->GetEntries() < 10){
            std::cout << "  Skipping - too few entries" << std::endl;
            
            if(byLayer){
              myfile << detId << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                     << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
              myerrorfile << detId << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                          << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
            }
            
            delete tt_tmp;
            delete tmpTF2;
            continue;
          }
          
          // Histogram residuals
          TH1F *h1 = new TH1F("h1", "h1 title", 100, -20, 20);
          tt_tmp->Project("h1", "seg_RdPhi", "");  // Adjust branch name
          
          // Fit to get mean and std
          TF1 f1 = TF1("f1", "gaus", -2, 2);
          f1.SetParLimits(1, -2, 2);
          f1.SetParLimits(2, 0, 2);
          h1->Fit("f1", "RQ");
          float fitMean = f1.GetParameter(1);
          float fitStd = f1.GetParameter(2);
          
          std::cout << "  Fit Mean: " << fitMean << ", Std: " << fitStd << std::endl;
          
          // Apply sigma cut
          tt = tt_tmp->CopyTree(Form("seg_RdPhi <= (%f + (1.6*%f)) && seg_RdPhi >= (%f - (1.6*%f))", 
                                     fitMean, fitStd, fitMean, fitStd));
          
          std::cout << "  After sigma cut: " << tt->GetEntries() << " entries" << std::endl;
          
          if (tt->GetEntries() == 0){
            if(byLayer){
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
          
          // Set branch addresses - ADJUST THESE TO YOUR TREE BRANCHES!
          tt->SetBranchAddress("seg_RdPhi", &mResidual);
          tt->SetBranchAddress("seg_LP", &mLocalPoint);      // Local point
          tt->SetBranchAddress("seg_GP", &mGlobalPoint);     // Global point
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
          
          // Save to CSV
          if(byLayer){
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
    }
    
    myfile.close();
    myerrorfile.close();
    std::cout << "\n========================================" << std::endl;
    std::cout << "Finished cut number " << nCut << std::endl;
  }
  
  delete tmpTF;
  std::cout << "\nAll done!" << std::endl;
  return 0;
}
