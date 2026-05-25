#include <iostream>
#include <fstream>
#include <string>
#include "TMath.h"
#include "TMinuit.h"
#include "TTree.h"
#include "TFile.h"
#include "TString.h"
#include "TH1.h"
#include "TF1.h"
#include "TSystem.h"

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
  
  if (try_again) {
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
  
  for (int i = 0; i < 3; i++) {
    double v, e;
    mfit.GetParameter(i, v, e);
    mResult[i] = v;
    mError[i] = e;
  }
}

int main() {
  //////////////////////////////////////////////////////////////////////////////////////////
  // CONFIGURATION SECTION
  //////////////////////////////////////////////////////////////////////////////////////////
  const char* input_name = "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_before_alignment_392278-393087/260302_013057/merged_output.root";
  const char* tree_name = "analyzer/ME21Seg_Prop";
  const char* Rdphi_name = "RdPhi";
  const char* outname_prefix = "Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop";
  const char* cuts = "muon_pt > 5 && abs(RdPhi) < 100 && has_fidcut";
  bool doDx = true;
  bool doDy = true;
  bool doDphiz = true;
  bool byLayer = true;
  int nCuts = 2;
  //////////////////////////////////////////////////////////////////////////////////////////
  
  int max_layer = 2;
  if (byLayer) max_layer = 3;
  
  TFile *tf = new TFile(input_name);
  if (!tf || tf->IsZombie()) {
    std::cerr << "Error: Cannot open input file!" << std::endl;
    return 1;
  }
  
  TTree *tmpTr = (TTree*)tf->Get(tree_name);
  if (!tmpTr) {
    std::cerr << "Error: Cannot find tree!" << std::endl;
    return 1;
  }
  
  TFile* tmpTF1 = new TFile("tmp1.root", "recreate");
  std::cout << "Copying Tree" << std::endl;
  TTree *cutEn = tmpTr->CopyTree(cuts);
  std::cout << "Copied" << std::endl;
  std::cout << "Closing input" << std::endl;
  tf->Close();
  delete tf;
  
  for (int nCut = 1; nCut < nCuts; nCut++) {
    std::cout << "Starting cut number " << nCut << std::endl;
    std::cout << "Current number of entries = " << cutEn->GetEntries() << std::endl;
    
    if (nCut == 1) {
      std::cout << "nCut 1, using full file" << std::endl;
    } else {
      std::cout << "Slimming tmp file" << std::endl;
      int total_entries = cutEn->GetEntries();
      int nCut_entries = int(total_entries / 2.0);
      std::cout << "nCut = " << nCut << std::endl;
      std::cout << "total_entries = " << total_entries << std::endl;
      std::cout << "nCut_entries = " << nCut_entries << std::endl;
      std::cout << "Taking first half" << std::endl;
      cutEn = cutEn->CloneTree(nCut_entries);
    }
    
    std::cout << "New number of entries = " << cutEn->GetEntries() << std::endl;
    std::ofstream myfile;
    std::ofstream myerrorfile;
    std::cout << "Creating CSV file " << Form("%s.csv", outname_prefix) << std::endl;
    std::cout << "Creating error CSV file " << Form("%s_error.csv", outname_prefix) << std::endl;
    myfile.open(Form("%s.csv", outname_prefix));
    myerrorfile.open(Form("%s_error.csv", outname_prefix));
    
    double dx, dy, dz, dphix, dphiy, dphiz;
    double dx_error, dy_error, dz_error, dphix_error, dphiy_error, dphiz_error;
    int detNum;
    dz = 0.0; dphix = 0.0; dphiy = 0.0;
    dz_error = 0.0; dphix_error = 0.0; dphiy_error = 0.0;
    
    std::cout << "Starting Chamber loop" << std::endl;
    for (int j = -1; j < 2; j = j + 2) {
      for (int i = 0; i < 36; i++) {
        for (int k = 1; k < max_layer; k++) {
          detNum = j * (i + 101);
          std::cout << "at chamber " << detNum << " and layer " << k << std::endl;
          
          TString tmpFileName = Form("tmp2_det%d_layer%d.root", detNum, k);
          TFile* tmpTF2 = new TFile(tmpFileName, "recreate");
          std::cout << "About to copy tree" << std::endl;
          TTree* tt_tmp;
          
          if (byLayer) {
            tt_tmp = cutEn->CopyTree(Form("rechit_detId==%d && prop_location[3] == %d", detNum, k));
          } else {
            tt_tmp = cutEn->CopyTree(Form("rechit_detId==%d", detNum));
          }
          std::cout << "Entries are on chamber are " << tt_tmp->GetEntries() << std::endl;

          if (tt_tmp->GetEntries() < 10) {
            tmpTF2->Close();
            delete tmpTF2;
            gSystem->Unlink(tmpFileName);
            continue;
          }
          
          TH1F *h1 = new TH1F("h1", "h1 title", 100, -20, 20);
          tt_tmp->Project("h1", "RdPhi", "");
          
          TF1 *f1 = new TF1("f1", "gaus", -2, 2);
          f1->SetParLimits(1, -2, 2);
          f1->SetParLimits(2, 0, 2);
          h1->Fit("f1", "RQ");
          float fitMean = f1->GetParameter(1);
          float fitStd = f1->GetParameter(2);
          
          delete f1;
          delete h1;
          
          std::cout << "Starting small copy" << std::endl;
          tt = tt_tmp->CopyTree(Form("RdPhi <= (%f + (1.6*%f)) && RdPhi >= (%f - (1.6*%f))", 
                                      fitMean, fitStd, fitMean, fitStd));
          
          if (tt->GetEntries() == 0) {
            myfile << detNum << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                   << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
            myerrorfile << detNum << ", " << 0 << ", " << 0 << ", " << 0 << ", " 
                        << 0 << ", " << 0 << ", " << 0 << ", " << 0 << "\n";
            tmpTF2->Close();
            delete tmpTF2;
            gSystem->Unlink(tmpFileName);
            continue;
          }
          
          tt->SetBranchAddress("RdPhi", &mResidual);
          tt->SetBranchAddress("prop_LP", &mLocalPoint);
          tt->SetBranchAddress("prop_GP", &mGlobalPoint);
          mEvents = tt->GetEntries();
          doFit(doDx, doDy, doDphiz);
          
          dx = mResult[0];
          dx_error = mError[0];
          dy = mResult[1];
          dy_error = mError[1];
          dphiz = mResult[2];
          dphiz_error = mError[2];
          
          if (byLayer) {
            myfile << detNum << k << ", " << dx << ", " << dy << ", " << dz << ", " 
                   << dphix << ", " << dphiy << ", " << dphiz << ", " << mEvents << "\n";
            myerrorfile << detNum << k << ", " << dx_error << ", " << dy_error << ", " << dz_error << ", " 
                        << dphix_error << ", " << dphiy_error << ", " << dphiz_error << ", " << mEvents << "\n";
          } else {
            myfile << detNum << ", " << dx << ", " << dy << ", " << dz << ", " 
                   << dphix << ", " << dphiy << ", " << dphiz << ", " << mEvents << "\n";
            myerrorfile << detNum << ", " << dx_error << ", " << dy_error << ", " << dz_error << ", " 
                        << dphix_error << ", " << dphiy_error << ", " << dphiz_error << ", " << mEvents << "\n";
          }
          
          tmpTF2->Close();
          delete tmpTF2;
          gSystem->Unlink(tmpFileName);
        }
      }
    }
    myfile.close();
    myerrorfile.close();
  }
  
  tmpTF1->Close();
  delete tmpTF1;
  gSystem->Unlink("tmp1.root");
  
  return 0;
}
