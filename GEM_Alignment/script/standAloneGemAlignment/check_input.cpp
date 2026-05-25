//cd /afs/cern.ch/user/k/kkeshav/CMSSW_15_1_0/src/GEMCSCBendingAnalyzer/GEM_Alignment/standAloneGemAlignment
//# Create diagnostic file
//cat > check_input.cpp << 'EOF'
#include <iostream>
#include "TFile.h"
#include "TTree.h"
#include "TKey.h"
#include "TMath.h"

int main() {
  const char* input_name = "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_before_alignment_392278-393087/260302_013057/merged_output.root";
  
  std::cout << "=== Checking Input File ===" << std::endl;
  std::cout << "File: " << input_name << std::endl;
  
  TFile *tf = new TFile(input_name);
  if (!tf || tf->IsZombie()) {
    std::cerr << "ERROR: Cannot open file!" << std::endl;
    return 1;
  }
  
  std::cout << "✓ File opened" << std::endl;
  std::cout << "\nFile contents:" << std::endl;
  tf->ls();
  
  TTree *tree = (TTree*)tf->Get("analyzer/ME21Seg_Prop");
  if (!tree) {
    std::cerr << "\nERROR: Tree not found!" << std::endl;
    return 1;
  }
  
  std::cout << "\n✓ Tree found" << std::endl;
  std::cout << "Entries: " << tree->GetEntries() << std::endl;
  
  std::cout << "\nTesting cuts:" << std::endl;
  std::cout << "  muon_pt > 5: " << tree->GetEntries("muon_pt > 5") << std::endl;
  std::cout << "  abs(RdPhi) < 100: " << tree->GetEntries("abs(RdPhi) < 100") << std::endl;
  std::cout << "  has_fidcut: " << tree->GetEntries("has_fidcut") << std::endl;
  std::cout << "  Combined: " << tree->GetEntries("muon_pt > 5 && abs(RdPhi) < 100 && has_fidcut") << std::endl;
  
  return 0;
}

