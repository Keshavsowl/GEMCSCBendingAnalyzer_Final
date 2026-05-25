import ROOT
import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# CONFIGURATION
# ============================================================================
PT_CUT = 20.0  # GeV - minimum pT requirement
ENDCAPS = [-1, 1]  # Both endcaps
LAYERS = [1, 2]    # Both layers (ME21)
# ============================================================================

# Open the ROOT file
file_path = "/eos/user/k/kkeshav/tamu_mual/2025/2025C/Muon0/Run2025C_muon0_v3_NEW2_ME21_backprop/250701_171347/merged.root"
f = ROOT.TFile.Open(file_path)
tree = f.Get("analyzer/ME21Seg_Prop")

print("="*70)
print("MUON ETA DISTRIBUTION ANALYSIS (PT > {} GeV + RECHIT CUTS)".format(PT_CUT))
print("="*70)
print(f"Total entries in tree: {tree.GetEntries()}")
print(f"Selection cuts:")
print(f"  - pT > {PT_CUT} GeV")
print(f"  - Rechit endcaps: {ENDCAPS}")
print(f"  - Rechit layers (ME21): {LAYERS}")
print("="*70)

# Storage for selected muon eta values
eta_selected = []

n_entries = tree.GetEntries()
print("\nReading entries...")

for i in range(n_entries):
    tree.GetEntry(i)
    
    pt = tree.muon_pt
    eta = tree.muon_eta
    
    # Apply pT cut
    if pt <= PT_CUT:
        continue
    
    # Apply rechit location cut
    if hasattr(tree, 'rechit_location'):
        rechit_endcap = tree.rechit_location[0]
        rechit_layer = tree.rechit_location[3]
        if rechit_endcap in ENDCAPS and rechit_layer in LAYERS:
            eta_selected.append(eta)
    
    if (i + 1) % 50000 == 0:
        print(f"  Processed {i+1}/{n_entries} entries...")

n_selected = len(eta_selected)
print(f"\nTotal muons passing pT > {PT_CUT} GeV + rechit cuts: {n_selected}")

if n_selected > 0:
    print(f"Mean η: {np.mean(eta_selected):.3f}")
    print(f"Std Dev η: {np.std(eta_selected):.3f}")
    print(f"Range: [{np.min(eta_selected):.3f}, {np.max(eta_selected):.3f}]")

# =====================
# PLOT HISTOGRAM
# =====================
plt.figure(figsize=(8, 6))

plt.hist(eta_selected, bins=60, range=(-3, 3), color='tomato', 
         edgecolor='darkred', linewidth=1.2, alpha=0.7, density=True, histtype = 'step')

plt.xlabel('Muon η', fontsize=13, fontweight='bold')
plt.ylabel('Normalized Counts (A.U.)', fontsize=13, fontweight='bold')
plt.title(f'Muon η Distribution (pT > {PT_CUT} GeV + Rechit cuts)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# Optional: Detector acceptance regions
plt.axvspan(-2.4, -0.9, alpha=0.1, color='green', label='Endcap (CSC)')
plt.axvspan(0.9, 2.4, alpha=0.1, color='green')
plt.axvspan(-0.9, 0.9, alpha=0.1, color='orange', label='Barrel (DT)')
plt.legend(loc='upper right', fontsize=10)

plt.savefig('muon_eta_pt30_rechit.png', dpi=300, bbox_inches='tight')
print("\nPlot saved as 'muon_eta_pt30_rechit.png'")

plt.show()

# Close ROOT file
f.Close()

print("\nANALYSIS COMPLETE")

