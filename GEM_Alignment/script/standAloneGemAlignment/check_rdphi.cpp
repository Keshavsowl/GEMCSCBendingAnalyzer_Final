//#cat > check_rdphi.cpp << 'EOF'
#include <iostream>
#include "TFile.h"
#include "TTree.h"
include "TH1F.h"
#include "TCanvas.h"

int main() {
  const char* input_name = "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_before_alignment_392278-393087/260302_013057/merged_output.root";
  
  TFile *tf = new TFile(input_name);
  TTree *tree = (TTree*)tf->Get("analyzer/ME21Seg_Prop");
  
  std::cout << "Total entries: " << tree->GetEntries() << std::endl;
  
  // Check if RdPhi branch exists
  TBranch* br = tree->GetBranch("RdPhi");
  if (!br) {
    std::cout << "ERROR: RdPhi branch not found!" << std::endl;
    std::cout << "\nAvailable branches:" << std::endl;
    TObjArray* branches = tree->GetListOfBranches();
    for (int i = 0; i < branches->GetEntries(); i++) {
      std::cout << "  - " << branches->At(i)->GetName() << std::endl;
    }
    return 1;
  }
  
  std::cout << "✓ RdPhi branch found" << std::endl;
  
  // Create histogram
  TH1F *h = new TH1F("h", "RdPhi Distribution", 200, -1000, 1000);
  tree->Project("h", "RdPhi");
  
  std::cout << "\nRdPhi Statistics:" << std::endl;
  std::cout << "  Entries: " << h->GetEntries() << std::endl;
  std::cout << "  Mean: " << h->GetMean() << std::endl;
  std::cout << "  RMS: " << h->GetRMS() << std::endl;
  std::cout << "  Min: " << h->GetXaxis()->GetBinCenter(h->FindFirstBinAbove(0)) << std::endl;
  std::cout << "  Max: " << h->GetXaxis()->GetBinCenter(h->FindLastBinAbove(0)) << std::endl;
  
  // Count in ranges
  std::cout << "\nEntries in different ranges:" << std::endl;
  std::cout << "  |RdPhi| < 10: " << tree->GetEntries("abs(RdPhi) < 10") << std::endl;
  std::cout << "  |RdPhi| < 50: " << tree->GetEntries("abs(RdPhi) < 50") << std::endl;
  std::cout << "  |RdPhi| < 100: " << tree->GetEntries("abs(RdPhi) < 100") << std::endl;
  std::cout << "  |RdPhi| < 500: " << tree->GetEntries("abs(RdPhi) < 500") << std::endl;
  std::cout << "  |RdPhi| < 1000: " << tree->GetEntries("abs(RdPhi) < 1000") << std::endl;
  std::cout << "  RdPhi == -999 or -9999: " << tree->GetEntries("RdPhi < -990") << std::endl;
  
  // Check with other cuts
  std::cout << "\nWith muon_pt > 5:" << std::endl;
  std::cout << "  |RdPhi| < 100: " << tree->GetEntries("muon_pt > 5 && abs(RdPhi) < 100") << std::endl;
  std::cout << "  |RdPhi| < 500: " << tree->GetEntries("muon_pt > 5 && abs(RdPhi) < 500") << std::endl;
  
  std::cout << "\nWith has_fidcut:" << std::endl;
  std::cout << "  |RdPhi| < 100: " << tree->GetEntries("has_fidcut && abs(RdPhi) < 100") << std::endl;
  std::cout << "  |RdPhi| < 500: " << tree->GetEntries("has_fidcut && abs(RdPhi) < 500") << std::endl;
  
  return 0;
}
//EOF

//# Compile and run
//g++ -o check_rdphi check_rdphi.cpp `root-config --cflags --libs`
//./check_rdphi
