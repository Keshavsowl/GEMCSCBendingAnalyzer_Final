import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh
low_pt = 30
high_pt = 200
endcap = 1
layer = 2

f = ROOT.TFile("/eos/user/t/toakhter/tamu_mual/2025/Run2025B_muon0_ZMu_150X_dataRun3_Prompt_v1.root")
#event = f.Get("analyzer/ME11Seg_Prop")
event = f.Get("analyzer/Inner_Prop")
#event = f.Get("analyzer/CSC_Prop")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

H_ref = 800
W_ref = 800
W = W_ref
H = H_ref

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.20*W_ref

xbins = 300
ybins = 300
xlow = -300
xhigh = 300
ylow = -300
yhigh = 300
zlow = -1
zhigh = 1

canvas = ROOT.TCanvas("c1", "c1", 100, 100, W, H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)

h = ROOT.TProfile2D("h", "h", xbins, xlow, xhigh, ybins, ylow, yhigh)

ablue = array.array("d", [1,1,0])
ared = array.array("d", [0,1,1])
agreen = array.array("d", [0,1,0])
astop = array.array("d", [0,.5,1])
myPalette = []
fi = ROOT.TColor.CreateGradientColorTable(3, astop, ared, agreen, ablue, 100)
for x in range(100):
  myPalette.append(fi+x)
ROOT.gStyle.SetPalette(100, array.array("i", myPalette))

xAxis = h.GetXaxis()
xAxis.SetTitleOffset(2)
xAxis.SetTitleSize(0.04)
#xAxis.SetTitle("Local x [cm]")
xAxis.SetTitle("Global X [cm]")
#xAxis.CenterTitle()

yAxis = h.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.04)
#yAxis.SetTitle("Local y [cm]")
yAxis.SetTitle("Global Y [cm]")
#yAxis.CenterTitle()

zAxis = h.GetZaxis()
zAxis.SetTitle("#DeltaR#phi [cm]")
#zAxis.SetTitle("bending angle [mrad]")
#zAxis.CenterTitle()
zAxis.SetTitleOffset(2)
zAxis.SetTitleSize(0.04)
zAxis.SetRangeUser(zlow, zhigh)
'''
for reg in [-1, 0, 1]:
  if reg == 0:
    event.Project("h", "RdPhi_Corrected:prop_GP[1]:prop_GP[0]", "has_prop && abs(RdPhi) < 5 && n_ME11_segment == 1 && muon_pt > 3")
  else:
    event.Project("h", "RdPhi_Corrected:prop_GP[1]:prop_GP[0]", "has_prop && abs(RdPhi) < 5 && n_ME11_segment == 1 && muon_pt > 3 && prop_location[0] == {reg}".format(reg = reg))
'''
event.Project("h", "RdPhi_Corrected:prop_GP[1]:prop_GP[0]", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && has_TightID && muon_pt>{low} && muon_pt<{high} && prop_location[0]=={reg} && prop_location[3]=={lay}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer))
h.Draw("colz")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.27*canvas.GetTopMargin())

latex.SetTextAlign(32)
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())))
# latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "4.03 fb^{-1} (13.6 TeV)")
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(12)
if endcap==1:
  reg_str="+"
elif endcap==-1:
  reg_str="-"
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "{reg}Endcap Layer {lay}".format(reg = reg_str, lay=layer))
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.5*canvas.GetTopMargin(), "2025B")
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Region {reg}".format(reg=endcap))
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "R{reg} L{lay}".format(reg=endcap, lay=layer))
latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.3*canvas.GetTopMargin())
latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Work in Progress")

latex.SetTextFont(42)
latex.SetTextSize(0.5*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()

#if os.path.exists("Run{run}/{version}/".format(run=year, version=version)) == False:
#  os.mkdir("Run{run}/{version}/".format(run=year, version=version))
#canvas.SaveAs("Run{run}/{version}/2Drdphi_pt{low}to{high}_R{reg}.png".format(run=year, version=version, low=low_pt, high=high_pt, reg=endcap, lay=layer))
canvas.SaveAs("residual_2D_R{reg}L{lay}_trackerProp.png".format(reg=endcap, lay=layer))
