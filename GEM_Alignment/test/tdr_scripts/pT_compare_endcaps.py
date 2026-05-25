import ROOT, tdrstyle, sys, os, array

year = "2024H" #change between 2022B and 2022C for example
version = "v1" #File version

f = ROOT.TFile("/eos/user/t/toakhter/tamu_mual/2024/{run}/Run{run}_muon0_alignedreco_{v}.root".format(run=year, v=version))
#f = ROOT.TFile("/eos/user/t/toakhter/tamu_mual/2022/singleMuonGun_11_3_4_2021_design_v0.root")


event = f.Get("analyzer/ME11SegReco_Prop")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

H_ref = 800
W_ref = 1000
W = W_ref
H = H_ref#

T = 0.12*H_ref
B = 0.16*H_ref
L = 0.16*W_ref
R = 0.08*W_ref

xbins = 100
ybins = 100
xlow = 0
xhigh = 200
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
#canvas.SetLogx() #log x axis
canvas.SetLogy()
canvas.SetGrid()

h = ROOT.TH1D("h", "h", xbins, xlow, xhigh)
h0 = ROOT.TH1D("h0", "h0", xbins, xlow, xhigh)

xAxis = h.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
#xAxis.SetNdivisions(-505)
xAxis.SetTitle("p_{T} [GeV]")
#xAxis.CenterTitle()

ch_list = []
ch_list_even = []
ch_list_odd = []
even_cut = ""
odd_cut = ""

#event.Project("h", "muon_pt", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && prop_location[0]=={reg}".format(reg=-1))
#event.Project("h0", "muon_pt", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && prop_location[0]=={reg}".format(reg=1))

event.Project("h", "muon_pt", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && prop_location[0]=={reg} && has_TightID".format(reg=-1))
event.Project("h0", "muon_pt", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && prop_location[0]=={reg} && has_TightID".format(reg=1))


yAxis = h.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("Entries")

h.SetMarkerSize(0)
h0.SetMarkerSize(0)

h.SetFillColorAlpha(ROOT.kAzure+1, 0.3)
h0.SetFillColorAlpha(ROOT.kRed-7, 0.3)

#h.SetFillStyle(3345)
#h0.SetFillStyle(3354)

h.SetLineWidth(2)
h0.SetLineWidth(2)

h.Draw("HIST")
h0.Draw("HIST SAME")

rootkde = ROOT.TLegend(0.5,0.73,0.9,0.85)
rootkde.AddEntry(h,"-Endcap: {entries}".format(entries=int(h.GetEntries())))
rootkde.AddEntry(h0,"+Endcap: {entries}".format(entries=int(h0.GetEntries())))
rootkde.SetBorderSize(0)
rootkde.Draw()

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.35*canvas.GetTopMargin())

latex.SetTextAlign(32)
latex.SetTextColor(ROOT.kBlack)
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(12)
latex.SetTextSize(0.3*canvas.GetTopMargin())
latex.DrawLatex(3.0*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "{y} Data".format(y=2024))

latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.4*canvas.GetTopMargin())
latex.DrawLatex(1.7*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()


#canvas.SaveAs("{run}/1D_ptDist.png".format(run=year))
canvas.SaveAs("{run}/{v}/1D_ptDist_tight.png".format(run=year, v=version))
