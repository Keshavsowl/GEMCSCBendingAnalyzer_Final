
import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh

#f = ROOT.TFile("{}".format(sys.argv[1]))
#f = ROOT.TFile("afs/cern.ch/work/t/toakhter/private/mual_tamu/BeamCommissioning_12_4_0/src/GEMCSCBendingAnalyzer/GEM_Alignment/test/Run2022B_ZMu_RAWRECO_v0.root")
#f = ROOT.TFile("../Run2022B_ZMu_RAWRECO_v0.root")
f = ROOT.TFile("/afs/cern.ch/user/d/daebi/public/forTowsifa/2022/out_Run2022C_allruns_usingCosmicDB6DOF.root")
event = f.Get("analyzer/ME11Seg_Prop")
#event = f.Get("analyzer/Inner_Prop")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

H_ref = 800
W_ref = 800
W = W_ref
H = H_ref

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.08*W_ref

xbins = 10
ybins = 100
xlow = -0.5
xhigh = 9.5
ylow = -300
yhigh = 300
zlow = -2
zhigh = 2

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

h = ROOT.TEfficiency("h", "h", xbins, xlow, xhigh)

num = 0
den = 0

for i in event:
  eta = i.prop_location[4]
  #if i.has_prop==1 and i.prop_location[0]==-1 and i.prop_location[2]==28 and i.muon_pt>20 and i.n_ME11_segment==1 and i.muonIdx in muonIndex and i.has_fidcut==1:
  if i.has_prop==1 and i.n_ME11_segment==1 and i.has_fidcut==1 and i.muon_pt>25 and i.prop_location[3]==2 and i.prop_location[0]==1 and i.runNum==356005:
    if i.has_rechit==1 and abs(i.RdPhi_Corrected)<5:
      num += 1
      den += 1
      h.Fill(True, eta)
    else:
      den += 1
      h.Fill(False, eta)

gr = h.CreateGraph()

xAxis = gr.GetXaxis()
xAxis.SetTitleOffset(1)
xAxis.SetTitleSize(0.05)
xAxis.SetTitle("#eta partition")
#xAxis.CenterTitle()

yAxis = gr.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("Efficiency")
#yAxis.CenterTitle()

gr.SetLineWidth(3)
yAxis.SetRangeUser(0,1.0)
gr.Draw("ap")

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

latex.SetTextAlign(32)
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(22)
latex.DrawLatex(0.4+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-5.0*canvas.GetTopMargin(), "Passed: {a}, Total: {b}".format(a=num, b=den))
latex.DrawLatex(0.5+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-5.5*canvas.GetTopMargin(), "Region 1 Layer 2")
latex.SetTextAlign(12)

latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Run 2022C: 356005")
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "30<Muon pT<200GeV") 
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Region: {reg}".format(reg = reg))

latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.4*canvas.GetTopMargin())
latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Work in Progress")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()

if os.path.exists("v0/") == False:
  os.mkdir("v0/")
canvas.SaveAs("v0/eff2022C_356005_R1layer2.png")
 # canvas.SaveAs("plots/res1D_R{reg}.png".format(reg = reg))
