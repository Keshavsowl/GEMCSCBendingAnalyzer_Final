import ROOT, tdrstyle, sys, os, array

# Configuration
low_pt = 45
high_pt = 46
supch_cut = "both"
endcap = -1
layer = 1
muon_charge = "-"
chambers = [18]
y_min = 0.0
y_max = 0.18
x_min = -3.0
x_max = 3.0

# ============================================================
# File paths - THREE SLOTS: Data, MC2025, MC2025 Misaligned
# ============================================================
files_config = [
    {
        # ---- SLOT 1: DATA ----
        "path": "/eos/cms/store/group/alca_muonalign/kkeshav/Muon0/Run2025C_muon0_iteration1_after_alignment_392278-393087/260311_203216/merged.root",
        "tree": "analyzer/ME21Seg_Prop",
        "color": ROOT.kBlack,
        "name": "Run 2025C (Data)",
        "label": "Data",
        "linestyle": 1,
        "linewidth": 3,
    },
    {
        # ---- SLOT 2: MC 2025 Aligned ----
        "path": "/eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_z_csc_v1/TBMA_MC_Neg_muon_Pt25to70_csc_v1/260418_221708/merged.root",
        "tree": "analyzer/ME21Seg_Prop",
        "color": ROOT.kBlue,
        "name": "MC 2025 (Aligned)",
        "label": "MC",
        "linestyle": 1,
        "linewidth": 3,
    },
    {
        # ---- SLOT 3: MC 2025 MISALIGNED ----
        # <<< REPLACE PATH WITH YOUR MISALIGNED MC FILE >>>
        "path": "/eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_z_csc_v1/TBMA_MC_Neg_muon_Pt25to70_csc_v1/260418_221708/merged_misaligned.root",
        "tree": "analyzer/ME21Seg_Prop",
        "color": ROOT.kRed,
        "name": "MC 2025 (Misaligned)",
        "label": "MC Misaligned",
        "linestyle": 2,
        "linewidth": 3,
    },
]

# ============================================================
# ROOT style
# ============================================================
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

# Endcap string
if endcap == 1:
    reg_string = "+"
elif endcap == -1:
    reg_string = "-"

# Charge string for output
charge_str_map = {"+": "pos", "-": "neg", "both": "both"}
charge_str = charge_str_map.get(muon_charge, "both")

# Chamber string for output
if chambers == "all":
    chamber_str = "allCh"
elif isinstance(chambers, (list, range)):
    ch_list = list(chambers)
    if len(ch_list) <= 5:
        chamber_str = "Ch" + "_".join(map(str, ch_list))
    else:
        chamber_str = f"Ch{min(ch_list)}to{max(ch_list)}"
else:
    chamber_str = "allCh"

# ============================================================
# Canvas setup
# ============================================================
H_ref = 800
W_ref = 800
W = W_ref
H = H_ref
T = 0.12 * H_ref
B = 0.16 * H_ref
L = 0.16 * W_ref
R = 0.08 * W_ref

canvas = ROOT.TCanvas("c1", "c1", 100, 100, W, H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin(L / W)
canvas.SetRightMargin(R / W)
canvas.SetTopMargin(T / H)
canvas.SetBottomMargin(B / H)
canvas.SetTickx(0)
canvas.SetTicky(0)
canvas.SetGrid()

# Bending angle settings
xbins = 100
xlow  = x_min
xhigh = x_max
x_axis = "Bending Angle [mrad]"

# ============================================================
# Open files and process
# ============================================================
open_files = []
histograms  = []
max_entries = 0

for i, config in enumerate(files_config):
    print("\n" + "=" * 60)
    print(f"Processing SLOT {i+1}: {config['name']}")
    print("=" * 60)

    f = ROOT.TFile.Open(config["path"])
    if not f or f.IsZombie():
        print(f"ERROR: Could not open file {config['path']}")
        continue
    open_files.append(f)

    event = f.Get(config["tree"])
    if not event or not isinstance(event, ROOT.TTree):
        print(f"ERROR: Could not load tree {config['tree']}")
        continue
    print(f"Tree entries: {event.GetEntries()}")

    # Find bending-angle branch
    ba_var = None
    for var in ["bending_angle", "BendingAngle", "ba", "BA"]:
        if event.GetBranch(var):
            ba_var = var
            print(f"Found bending angle variable: {ba_var}")
            break

    if not ba_var:
        print("ERROR: Could not find bending angle variable!")
        print("Available branches:")
        for branch in event.GetListOfBranches():
            print(f"  - {branch.GetName()}")
        continue

    # Detect helper branches
    segment_var   = None
    location_var  = None
    chamber_var   = None
    chamber_index = None

    if event.GetBranch("n_ME11_segment"):
        segment_var = "n_ME11_segment"
    elif event.GetBranch("n_ME21_segment"):
        segment_var = "n_ME21_segment"

    if event.GetBranch("prop_location"):
        location_var = "prop_location"
    elif event.GetBranch("rechit_location"):
        location_var = "rechit_location"

    for var in ["chamber", "prop_location", "rechit_location"]:
        if event.GetBranch(var):
            if var == "chamber":
                chamber_var   = "chamber"
                chamber_index = None
            else:
                chamber_var   = var
                chamber_index = 2
            break

    # Build selection cut
    cut_parts = []

    if event.GetBranch("muon_pt"):
        cut_parts.append(f"muon_pt>={low_pt} && muon_pt<{high_pt}")

    if segment_var:
        cut_parts.append(f"{segment_var}==1")

    if event.GetBranch("has_fidcut"):
        cut_parts.append("has_fidcut")

    if location_var:
        cut_parts.append(f"{location_var}[0]=={endcap}")
        cut_parts.append(f"{location_var}[3]=={layer}")

    if event.GetBranch("muon_charge"):
        if muon_charge == "+":
            cut_parts.append("muon_charge==1")
            print("Selecting positive muons")
        elif muon_charge == "-":
            cut_parts.append("muon_charge==-1")
            print("Selecting negative muons")
        else:
            print("Selecting both charges")

    if chamber_var and chambers != "all":
        if isinstance(chambers, (list, range)):
            ch_list = list(chambers)
            if ch_list:
                if chamber_index is not None:
                    ch_cuts = [f"{chamber_var}[{chamber_index}]=={ch}" for ch in ch_list]
                else:
                    ch_cuts = [f"{chamber_var}=={ch}" for ch in ch_list]
                cut_parts.append("(" + " || ".join(ch_cuts) + ")")
                print(f"Selecting chambers: {ch_list}")
    elif chambers == "all":
        print("Selecting all chambers")

    selection_cut = " && ".join(cut_parts) if cut_parts else ""
    print(f"Selection cut: {selection_cut}")

    # Fill histogram
    h_temp = ROOT.TH1D(f"h_ba_temp{i}", f"h_ba_temp{i}", xbins, xlow, xhigh)
    x_plot = f"1000*{ba_var}"
    print(f"Projecting: {x_plot}")

    if selection_cut:
        event.Project(f"h_ba_temp{i}", x_plot, selection_cut)
    else:
        event.Project(f"h_ba_temp{i}", x_plot)

    h = h_temp.Clone(f"h_ba{i}")
    h.SetDirectory(0)

    print(f"Histogram entries: {h.GetEntries()}")
    if h.GetEntries() == 0:
        print(f"WARNING: No entries for {config['name']}!")
        continue

    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())

    h.SetLineWidth(config.get("linewidth", 3))
    h.SetLineStyle(config.get("linestyle", 1))
    h.SetMarkerSize(0)
    h.SetLineColor(config["color"])

    if h.GetMaximum() > max_entries:
        max_entries = h.GetMaximum()

    histograms.append((h, config))
    print(f"Mean: {h.GetMean():.4f},  RMS: {h.GetRMS():.4f}")

# ============================================================
# Safety check
# ============================================================
if len(histograms) == 0:
    print("\nERROR: No valid histograms created!")
    for f in open_files:
        f.Close()
    sys.exit(1)

# ============================================================
# Axes
# ============================================================
h_main = histograms[0][0]

xAxis = h_main.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
xAxis.SetTitle(x_axis)
xAxis.SetRangeUser(x_min, x_max)

yAxis = h_main.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("A.U.")
yAxis.SetRangeUser(y_min, y_max)
yAxis.SetMaxDigits(3)

# ============================================================
# Draw all three histograms
# ============================================================
for i, (h, config) in enumerate(histograms):
    draw_opt = "HIST" if i == 0 else "HIST SAME"
    h.Draw(draw_opt)

# ============================================================
# Legend
# ============================================================
legend = ROOT.TLegend(0.50, 0.68, 0.92, 0.88)
legend.SetNColumns(1)
for h, config in histograms:
    legend.AddEntry(h, config["name"], "L")
legend.SetTextSize(0.028)
legend.SetBorderSize(0)
legend.Draw()

# ============================================================
# CMS labels
# ============================================================
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)
latex.SetTextFont(42)

latex.SetTextSize(0.30 * canvas.GetTopMargin())
latex.SetTextAlign(32)
latex.DrawLatex(
    1 - 1.1 * canvas.GetRightMargin(),
    1 - canvas.GetTopMargin() + 0.20 * canvas.GetTopMargin(),
    "(13.6 TeV)"
)

latex.SetTextAlign(12)
latex.DrawLatex(
    0 + 1.1 * canvas.GetLeftMargin(),
    1 - canvas.GetTopMargin() - 1.0 * canvas.GetTopMargin(),
    "Run 2025C"
)

latex.SetTextSize(0.25 * canvas.GetTopMargin())
latex.DrawLatex(
    0.60 - 0.3 * canvas.GetRightMargin(),
    1 - canvas.GetTopMargin() - 1.8 * canvas.GetTopMargin(),
    f"{reg_string}Endcap  Layer {layer}"
)
latex.DrawLatex(
    0.60 - 0.3 * canvas.GetRightMargin(),
    1 - canvas.GetTopMargin() - 2.1 * canvas.GetTopMargin(),
    f"{low_pt} #leq p_{{T}} < {high_pt} GeV"
)

charge_label_map = {"+": "#mu^{+}", "-": "#mu^{-}", "both": "#mu^{#pm}"}
charge_label = charge_label_map.get(muon_charge, "#mu^{#pm}")
latex.DrawLatex(
    0.60 - 0.3 * canvas.GetRightMargin(),
    1 - canvas.GetTopMargin() - 2.4 * canvas.GetTopMargin(),
    charge_label
)

if chambers != "all" and isinstance(chambers, (list, range)):
    ch_list = list(chambers)
    if len(ch_list) <= 5:
        ch_label = "Ch: " + ", ".join(map(str, ch_list))
    else:
        ch_label = f"Ch: {min(ch_list)}-{max(ch_list)}"
    latex.DrawLatex(
        0.60 - 0.3 * canvas.GetRightMargin(),
        1 - canvas.GetTopMargin() - 2.7 * canvas.GetTopMargin(),
        ch_label
    )

latex.SetTextSize(0.50 * canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(
    0 + 1.1 * canvas.GetLeftMargin(),
    1 - canvas.GetTopMargin() - 0.27 * canvas.GetTopMargin(),
    "CMS"
)
latex.SetTextFont(52)
latex.SetTextSize(0.30 * canvas.GetTopMargin())
latex.DrawLatex(
    0 + 1.1 * canvas.GetLeftMargin(),
    1 - canvas.GetTopMargin() - 0.70 * canvas.GetTopMargin(),
    "Preliminary"
)

canvas.GetFrame().Draw()

# ============================================================
# Save plain comparison plot
# ============================================================
output_name = (
    f"BA_3way_R{endcap}L{layer}_pt{low_pt}to{high_pt}_{charge_str}_{chamber_str}.png"
)
canvas.SaveAs(output_name)
print(f"\nSaved: {output_name}")

# ============================================================
# Double-Gaussian fits for all three slots
# ============================================================
print("\n" + "=" * 60)
print("Performing double Gaussian fits (all three slots)...")
print("=" * 60)

fit_functions = []

for i, (h, config) in enumerate(histograms):
    if h.GetEntries() > 10:
        print(f"\nFitting {config['name']}...")

        f_fit = ROOT.TF1(
            f"f{i}",
            "[0]*exp(-0.5*((x-[1])/[2])**2) + [3]*exp(-0.5*((x-[4])/[5])**2)",
            x_min, x_max
        )
        f_fit.SetParameters(
            h.GetMaximum(), h.GetMean(), h.GetRMS(),
            0.2 * h.GetMaximum(), h.GetMean(), h.GetRMS()
        )
        f_fit.SetLineColor(config["color"])
        f_fit.SetLineStyle(7)
        f_fit.SetLineWidth(2)
        f_fit.SetMarkerSize(0)

        h.Fit(f"f{i}", "RQ")
        f_fit.Draw("same")

        fit_functions.append((f_fit, config))

        print(
            f"  G1: mean={f_fit.GetParameter(1):.4f}"
            f" +/- {f_fit.GetParError(1):.4f},"
            f"  sigma={f_fit.GetParameter(2):.4f}"
            f" +/- {f_fit.GetParError(2):.4f}"
        )
        print(
            f"  G2: mean={f_fit.GetParameter(4):.4f}"
            f" +/- {f_fit.GetParError(4):.4f},"
            f"  sigma={f_fit.GetParameter(5):.4f}"
            f" +/- {f_fit.GetParError(5):.4f}"
        )
    else:
        print(
            f"\nSkipping fit for {config['name']}"
            f" - insufficient entries ({h.GetEntries()})"
        )

# ============================================================
# Fit-result legend
# ============================================================
if len(fit_functions) > 0:
    n_fitted  = len(fit_functions)
    leg_y_top = 0.88
    leg_y_bot = max(0.10, leg_y_top - 0.055 * 3 * n_fitted)

    legend_fit = ROOT.TLegend(0.25, leg_y_bot, 0.95, leg_y_top)
    legend_fit.SetNColumns(1)

    for idx, (f_fit, config) in enumerate(fit_functions):
        h_ref = histograms[idx][0]

        legend_fit.AddEntry(h_ref, config["name"], "L")

        mu1    = f_fit.GetParameter(1)
        emu1   = f_fit.GetParError(1)
        sig1   = f_fit.GetParameter(2)
        esig1  = f_fit.GetParError(2)
        mu2    = f_fit.GetParameter(4)
        emu2   = f_fit.GetParError(4)
        sig2   = f_fit.GetParameter(5)
        esig2  = f_fit.GetParError(5)

        legend_fit.AddEntry(
            f_fit,
            f"  #mu_{{1}}:{mu1:.3f}#pm{emu1:.3f}  #sigma_{{1}}:{sig1:.3f}#pm{esig1:.3f}",
            "L"
        )
        legend_fit.AddEntry(
            f_fit,
            f"  #mu_{{2}}:{mu2:.3f}#pm{emu2:.3f}  #sigma_{{2}}:{sig2:.3f}#pm{esig2:.3f}",
            "L"
        )

    legend_fit.SetTextSize(0.022)
    legend_fit.SetBorderSize(0)
    legend_fit.Draw()

    output_fit_name = (
        f"BA_3way_R{endcap}L{layer}_pt{low_pt}to{high_pt}_{charge_str}_{chamber_str}_fit.png"
    )
    canvas.SaveAs(output_fit_name)
    print(f"\nSaved: {output_fit_name}")

# ============================================================
# Print summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("=" * 60)
for h, config in histograms:
    print(f"{config['name']}:")
    print(f"  Entries : {h.GetEntries()}")
    print(f"  Mean    : {h.GetMean():.4f}")
    print(f"  RMS     : {h.GetRMS():.4f}")

if len(fit_functions) > 0:
    print("\nFit Results:")
    print("-" * 60)
    for f_fit, config in fit_functions:
        print(f"{config['name']}:")
        print(f"  G1: mean = {f_fit.GetParameter(1):.4f} +/- {f_fit.GetParError(1):.4f}")
        print(f"  G1: sigma= {f_fit.GetParameter(2):.4f} +/- {f_fit.GetParError(2):.4f}")
        print(f"  G2: mean = {f_fit.GetParameter(4):.4f} +/- {f_fit.GetParError(4):.4f}")
        print(f"  G2: sigma= {f_fit.GetParameter(5):.4f} +/- {f_fit.GetParError(5):.4f}")

print("=" * 60)

# ============================================================
# Close files
# ============================================================
for f in open_files:
    f.Close()

print("\nDone!")
