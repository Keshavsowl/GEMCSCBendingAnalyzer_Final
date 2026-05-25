//cat > identify_bad_cut.cpp << 'ENDOFFILE'
#include <iostream>
#include "TFile.h"
#include "TTree.h"

int main() {
  TFile *tf = new TFile("/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_before_alignment_392278-393087/260302_013057/merged_output.root");
  TTree *tree = (TTree*)tf->Get("analyzer/ME21Seg_Prop");
  
  std::cout << "=== IDENTIFYING WHICH CUT REMOVES ALL ENTRIES ===" << std::endl;
  std::cout << "\nTotal entries: " << tree->GetEntries() << std::endl;
  
  // Test each cut individually
  std::cout << "\n--- Individual cuts ---" << std::endl;
  Long64_t n1 = tree->GetEntries("muon_pt > 5");
  Long64_t n2 = tree->GetEntries("abs(RdPhi) < 10000");
  Long64_t n3 = tree->GetEntries("has_fidcut");
  
  std::cout << "muon_pt > 5:           " << n1 << " entries" << std::endl;
  std::cout << "abs(RdPhi) < 10000:    " << n2 << " entries" << std::endl;
  std::cout << "has_fidcut:            " << n3 << " entries" << std::endl;
  
  // Test combinations
  std::cout << "\n--- Two-way combinations ---" << std::endl;
  Long64_t n12 = tree->GetEntries("muon_pt > 5 && abs(RdPhi) < 10000");
  Long64_t n13 = tree->GetEntries("muon_pt > 5 && has_fidcut");
  Long64_t n23 = tree->GetEntries("abs(RdPhi) < 10000 && has_fidcut");
  
  std::cout << "muon_pt > 5 && abs(RdPhi) < 10000:    " << n12 << " entries" << std::endl;
  std::cout << "muon_pt > 5 && has_fidcut:            " << n13 << " entries" << std::endl;
  std::cout << "abs(RdPhi) < 10000 && has_fidcut:     " << n23 << " entries" << std::endl;
  
  // Test all three
  std::cout << "\n--- All three cuts ---" << std::endl;
  Long64_t n123 = tree->GetEntries("muon_pt > 5 && abs(RdPhi) < 10000 && has_fidcut");
  std::cout << "muon_pt > 5 && abs(RdPhi) < 10000 && has_fidcut: " << n123 << " entries" << std::endl;
  
  // The culprit identification
  std::cout << "\n=== DIAGNOSIS ===" << std::endl;
  if (n2 == 0) {
    std::cout << "❌ PROBLEM: abs(RdPhi) < 10000 removes ALL entries!" << std::endl;
    std::cout << "   RdPhi values must be > 10000 or not filled properly." << std::endl;
    std::cout << "\n   Testing larger RdPhi cuts:" << std::endl;
    for (int cut : {100000, 1000000, 10000000}) {
      Long64_t n = tree->GetEntries(Form("abs(RdPhi) < %d", cut));
      std::cout << "   abs(RdPhi) < " << cut << ": " << n << " entries" << std::endl;
      if (n > 0) {
        std::cout << "   ✓ Use this cut value: " << cut << std::endl;
        break;
      }
    }
  } else if (n23 == 0 && n2 > 0 && n3 > 0) {
    std::cout << "❌ PROBLEM: RdPhi and has_fidcut don't overlap!" << std::endl;
    std::cout << "   Events with valid RdPhi don't pass has_fidcut." << std::endl;
  } else if (n12 == 0 && n1 > 0 && n2 > 0) {
    std::cout << "❌ PROBLEM: muon_pt and RdPhi don't overlap!" << std::endl;
    std::cout << "   Events with good muons don't have valid RdPhi." << std::endl;
  } else if (n123 == 0) {
    std::cout << "❌ PROBLEM: All cuts individually work, but combination gives 0!" << std::endl;
    std::cout << "   This suggests events are split between different conditions." << std::endl;
  } else {
    std::cout << "✓ Cuts are working! You have " << n123 << " entries passing all cuts." << std::endl;
  }
  
  return 0;
}
//ENDOFFILE

//g++ -o identify_bad_cut identify_bad_cut.cpp `root-config --cflags --libs`
//./identify_bad_cut
