import ROOT, tdrstyle, sys, os

# Configuration
endcaps = [-1, 1]  # Both endcaps
layer = [1,2]

# File paths and configurations
files_config = [
    {       
         "path" :"/afs/cern.ch/user/k/kkeshav/CMSSW_15_1_0/src/GEMCSCBendingAnalyzer/GEM_Alignment/test/output_test.root",
       # "path": "/eos/user/k/kkeshav/tamu_mual/2025/mc/CRAB_UserFiles/2025mc_v2/251225_020143/0000/output_test_1.root",
#        "path" : "/eos/user/k/kkeshav/tamu_mual/2025/2025D/Muon0/Run2025D_muon0_iter0_v1/251106_015013/merged.root",
        "tree": "analyzer/ME21Seg_Prop",
        "color": ROOT.kBlue,
        "name": "Test Output",
        "label": "output1_test"
    },
    {  

       # "path": "/eos/user/k/kkeshav/tamu_mual/2025/2025C/Muon0/Run2025C_muon0_v3_NEW2_ME21_backprop/250701_171347/merged.root"
        "path": "/eos/user/k/kkeshav/tamu_mual/2025/mcfinal/CRAB_UserFiles/2025mc_v3/260109_111904/0000/output_test_1.root",
#        "path" : "/eos/user/k/kkeshav/tamu_mual/2025/2025D/Muon0/Run2025D_muon0_iter0_v1/251106_015013/merged.root",
        "tree": "analyzer/ME21Seg_Prop",
        "color": ROOT.kRed,
        "name": "Run 2025C",
        "label": "2025C_merged"
    }
]

ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

# Canvas setup
H_ref = 800
W_ref = 800
W = W_ref
H = H_ref

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.08*W_ref


endcap_layer_cuts = []
for ec in endcaps:
    for ly in layer:
        endcap_layer_cuts.append(f"(rechit_location[0]=={ec} && rechit_location[3] =={ly})")

# Build combined selection cut for both endcaps
combined_cuts = " || ".join(endcap_layer_cuts)
print(f"Combined cuts: {combined_cuts}")
#base_cut = f"n_ME21_segment==1 && abs(RdPhi_Corrected) < 2 && ({endcap_cuts})"
base_cut = f" ({combined_cuts})"

print("\n" + "="*60)
print(f"Configuration: Both Endcaps (±), Layer {layer}")
print(f"Selection cut: {base_cut}")
print("="*60)

# ============================================
# Plot 1: pT Distribution
# ============================================
print("\n" + "="*60)
print("Creating pT Distribution Plot")
print("="*60)

canvas_pt = ROOT.TCanvas("c_pt", "c_pt", 100, 100, W, H)
canvas_pt.SetFillColor(0)
canvas_pt.SetBorderMode(0)
canvas_pt.SetFrameFillStyle(0)
canvas_pt.SetFrameBorderMode(0)
canvas_pt.SetLeftMargin(L/W)
canvas_pt.SetRightMargin(R/W)
canvas_pt.SetTopMargin(T/H)
canvas_pt.SetBottomMargin(B/H)
canvas_pt.SetTickx(0)
canvas_pt.SetTicky(0)
canvas_pt.SetGrid()

# pT settings
pt_bins = 50
pt_low = 20
pt_high = 100
pt_plot = "muon_pt"
pt_axis = "Muon p_{T} [GeV]"

open_files_pt = []
histograms_pt = []
max_entries_pt = 0

for i, config in enumerate(files_config):
    # Open file
    f = ROOT.TFile.Open(config["path"])
    if not f or f.IsZombie():
        print(f"ERROR: Could not open file {config['path']}")
        continue
    
    open_files_pt.append(f)
    
    # Get tree
    event = f.Get(config["tree"])
    if not event or not isinstance(event, ROOT.TTree):
        print(f"ERROR: Could not load tree {config['tree']} from {config['path']}")
        continue
    
    # Create histogram
    h_temp = ROOT.TH1D(f"h_pt_temp{i}", f"h_pt_temp{i}", pt_bins, pt_low, pt_high)
    
    # Fill histogram
    event.Project(f"h_pt_temp{i}", pt_plot, base_cut)
    
    # Clone and detach
    h = h_temp.Clone(f"h_pt{i}")
    h.SetDirectory(0)
    
    # Normalize
    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())
    
    # Style
    h.SetLineWidth(3)
    h.SetMarkerSize(0)
    h.SetLineColor(config["color"])
    
    if h.GetMaximum() > max_entries_pt:
        max_entries_pt = h.GetMaximum()
    
    histograms_pt.append((h, config))
    print(f"Loaded {config['name']}: {h.GetEntries()} entries, Mean pT: {h.GetMean():.2f} GeV")

if len(histograms_pt) > 0:
    # Set up axes
    h_main_pt = histograms_pt[0][0]
    h_main_pt.SetTitle(f"Muon p_{{T}} Distribution with p_{{T}} cut (p_{{T}} > {pt_low} GeV)")
    
    xAxis = h_main_pt.GetXaxis()
    xAxis.SetTitleOffset(0)
    xAxis.SetTitleSize(0.05)
    xAxis.SetTitle(pt_axis)

    yAxis = h_main_pt.GetYaxis()
    yAxis.SetTitleOffset(0)
    yAxis.SetTitleSize(0.05)
    yAxis.SetTitle("A.U.")
    yAxis.SetRangeUser(0, 1.4*max_entries_pt)
    yAxis.SetMaxDigits(3)

    # Draw histograms
    for i, (h, config) in enumerate(histograms_pt):
        if i == 0:
            h.Draw("HIST")
        else:
            h.Draw("HIST SAME")

    # Create legend
    legend_pt = ROOT.TLegend(0.55, 0.70, 0.9, 0.88)
    for h, config in histograms_pt:
        mean = h.GetMean()
        rms = h.GetRMS()
        legend_pt.AddEntry(h, f"{config['name']} (#mu={mean:.2f}, RMS={rms:.2f})")
    legend_pt.SetTextSize(0.03)
    legend_pt.SetBorderSize(0)
    legend_pt.Draw()

    # Add labels
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)

    latex.SetTextFont(42)
    latex.SetTextSize(0.3*canvas_pt.GetTopMargin())
    latex.SetTextAlign(32)
    latex.DrawLatex(1-1.1*canvas_pt.GetRightMargin(), 1-canvas_pt.GetTopMargin()+0.2*canvas_pt.GetTopMargin(), "(13.6 TeV)")
    latex.SetTextAlign(12)
    latex.DrawLatex(0+1.1*canvas_pt.GetLeftMargin(), 1-canvas_pt.GetTopMargin()-1.0*canvas_pt.GetTopMargin(), "Run 2025C")

    latex.SetTextSize(0.25*canvas_pt.GetTopMargin())
    latex.DrawLatex(0.65-0.3*canvas_pt.GetRightMargin(), 1-canvas_pt.GetTopMargin()-1.8*canvas_pt.GetTopMargin(), f"Both Endcaps Layer {layer}")

    latex.SetTextSize(0.5*canvas_pt.GetTopMargin())
    latex.SetTextFont(61)
    latex.DrawLatex(0+1.1*canvas_pt.GetLeftMargin(), 1-canvas_pt.GetTopMargin()-0.27*canvas_pt.GetTopMargin(), "CMS")
    latex.SetTextFont(52)
    latex.SetTextSize(0.3*canvas_pt.GetTopMargin())
    latex.DrawLatex(0+1.1*canvas_pt.GetLeftMargin(), 1-canvas_pt.GetTopMargin()-0.7*canvas_pt.GetTopMargin(), "Preliminary")

    # Update canvas to draw everything, THEN draw frame (or remove frame.Draw())
    canvas_pt.Update()
    
    output_pt = f"muon_pt_comparison_BothEndcaps_L{layer}.png"
    canvas_pt.SaveAs(output_pt)
    print(f"Saved plot: {output_pt}")

# Clean up pT files
for f in open_files_pt:
    f.Close()

# ============================================
# Plot 2: Eta Distribution
# ============================================
print("\n" + "="*60)
print("Creating Eta Distribution Plot")
print("="*60)

canvas_eta = ROOT.TCanvas("c_eta", "c_eta", 100, 100, W, H)
canvas_eta.SetFillColor(0)
canvas_eta.SetBorderMode(0)
canvas_eta.SetFrameFillStyle(0)
canvas_eta.SetFrameBorderMode(0)
canvas_eta.SetLeftMargin(L/W)
canvas_eta.SetRightMargin(R/W)
canvas_eta.SetTopMargin(T/H)
canvas_eta.SetBottomMargin(B/H)
canvas_eta.SetTickx(0)
canvas_eta.SetTicky(0)
canvas_eta.SetGrid()

# Eta settings
eta_bins = 50
eta_low = -3.0
eta_high = 3.0
eta_plot = "muon_eta"
eta_axis = "Muon #eta"

open_files_eta = []
histograms_eta = []
max_entries_eta = 0

for i, config in enumerate(files_config):
    # Open file
    f = ROOT.TFile.Open(config["path"])
    if not f or f.IsZombie():
        print(f"ERROR: Could not open file {config['path']}")
        continue
    
    open_files_eta.append(f)
    
    # Get tree
    event = f.Get(config["tree"])
    if not event or not isinstance(event, ROOT.TTree):
        print(f"ERROR: Could not load tree {config['tree']} from {config['path']}")
        continue
    
    # Create histogram
    h_temp = ROOT.TH1D(f"h_eta_temp{i}", f"h_eta_temp{i}", eta_bins, eta_low, eta_high)
    
    # Fill histogram
    event.Project(f"h_eta_temp{i}", eta_plot, base_cut)
    
    # Clone and detach
    h = h_temp.Clone(f"h_eta{i}")
    h.SetDirectory(0)
    
    # Normalize
    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())
    
    # Style
    h.SetLineWidth(3)
    h.SetMarkerSize(0)
    h.SetLineColor(config["color"])
    
    if h.GetMaximum() > max_entries_eta:
        max_entries_eta = h.GetMaximum()
    
    histograms_eta.append((h, config))
    print(f"Loaded {config['name']}: {h.GetEntries()} entries, Mean eta: {h.GetMean():.3f}")

if len(histograms_eta) > 0:
    # Set up axes
    h_main_eta = histograms_eta[0][0]
    h_main_eta.SetTitle(f"Muon #eta Distribution with p_{{T}} cut (p_{{T}} > {pt_low} GeV)")

    xAxis = h_main_eta.GetXaxis()
    xAxis.SetTitleOffset(0)
    xAxis.SetTitleSize(0.05)
    xAxis.SetTitle(eta_axis)

    yAxis = h_main_eta.GetYaxis()
    yAxis.SetTitleOffset(0)
    yAxis.SetTitleSize(0.05)
    yAxis.SetTitle("A.U.")
    yAxis.SetRangeUser(0, 1.4*max_entries_eta)
    yAxis.SetMaxDigits(3)

    # Draw histograms
    for i, (h, config) in enumerate(histograms_eta):
        if i == 0:
            h.Draw("HIST")
        else:
            h.Draw("HIST SAME")

    # Create legend
    legend_eta = ROOT.TLegend(0.55, 0.70, 0.9, 0.88)
    for h, config in histograms_eta:
        mean = h.GetMean()
        rms = h.GetRMS()
        legend_eta.AddEntry(h, f"{config['name']} (#mu={mean:.3f}, RMS={rms:.3f})")
    legend_eta.SetTextSize(0.03)
    legend_eta.SetBorderSize(0)
    legend_eta.Draw()

    # Add labels
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)

    latex.SetTextFont(42)
    latex.SetTextSize(0.3*canvas_eta.GetTopMargin())
    latex.SetTextAlign(32)
    latex.DrawLatex(1-1.1*canvas_eta.GetRightMargin(), 1-canvas_eta.GetTopMargin()+0.2*canvas_eta.GetTopMargin(), "(13.6 TeV)")
    latex.SetTextAlign(12)
    latex.DrawLatex(0+1.1*canvas_eta.GetLeftMargin(), 1-canvas_eta.GetTopMargin()-1.0*canvas_eta.GetTopMargin(), "Run 2025C")

    latex.SetTextSize(0.25*canvas_eta.GetTopMargin())
    latex.DrawLatex(0.55-0.1*canvas_eta.GetRightMargin(), 1-canvas_eta.GetTopMargin()-1.5*canvas_eta.GetTopMargin(), f"Both Endcaps Layers {layer}")

    latex.SetTextSize(0.5*canvas_eta.GetTopMargin())
    latex.SetTextFont(61)
    latex.DrawLatex(0+1.1*canvas_eta.GetLeftMargin(), 1-canvas_eta.GetTopMargin()-0.27*canvas_eta.GetTopMargin(), "CMS")
    latex.SetTextFont(52)
    latex.SetTextSize(0.3*canvas_eta.GetTopMargin())
    latex.DrawLatex(0+1.1*canvas_eta.GetLeftMargin(), 1-canvas_eta.GetTopMargin()-0.7*canvas_eta.GetTopMargin(), "Preliminary")

#    latex.SetTextSize(0.5*canvas_eta.GetTopMargin())
#    latex.SetTextFont(61)
#    latex.DrawLatex(canvas_eta.GetLeftMargin(), 1-canvas_eta.GetTopMargin()+0.2*canvas_eta.GetTopMargin(), "CMS")
    # Update canvas to draw everything, THEN remove or comment out frame.Draw()
    canvas_eta.Update()
    
    output_eta = f"muon_eta_comparison_BothEndcaps_L{layer}.png"
    canvas_eta.SaveAs(output_eta)
    print(f"Saved plot: {output_eta}")

# Clean up eta files
for f in open_files_eta:
    f.Close()

print("\n" + "="*60)
print("All plots completed!")
print("="*60)

