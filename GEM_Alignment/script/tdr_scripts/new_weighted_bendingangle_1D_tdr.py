import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh

year = "2022D" #change between 2022B and 2022C for example
#version = "ZMu_PromptReco_RAWRECO_prealigned_v4" #File version
version0 = "ZMu_PromptReco_RAWRECO_globalMu_v2"
version1 = "ZMu_PromptReco_RAWRECO_globalMu_aligned_v2"

low_pt = 30
high_pt = 35
#layer = 1

#f = ROOT.TFile("{}".format(sys.argv[1]))
#f = ROOT.TFile("../Run{run}_{version}.root".format(run=year, version=version))
f0 = ROOT.TFile("../Run{run}_{version}.root".format(run=year, version=version0))
f1 = ROOT.TFile("../Run{run}_{version}.root".format(run=year, version=version1))
f2 = ROOT.TFile("../singleMuonGun_11_3_4_2021_design_v0.root")

#event = f.Get("analyzer/ME11Seg_Prop")
event0 = f0.Get("analyzer/ME11Seg_Prop")
event1 = f1.Get("analyzer/ME11Seg_Prop")
event2 = f2.Get("analyzer/ME11Seg_Prop")
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

xbins = 100
ybins = 100
xlow = 0
xhigh = 5
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
#canvas.SetLogy()

odd_cut = "(prop_location[2]== 1 || prop_location[2] == 3 || prop_location[2] == 5 || prop_location[2] ==7 || prop_location[2] ==9 || prop_location[2] ==11 || prop_location[2] ==13 || prop_location[2] ==15 || prop_location[2] ==17 || prop_location[2] ==19 || prop_location[2] ==21 || prop_location[2] ==23 || prop_location[2] ==25 || prop_location[2] ==27 || prop_location[2] ==29 || prop_location[2] ==31 || prop_location[2] ==33 || prop_location[2] ==35)"
even_cut = "(prop_location[2]== 2 || prop_location[2] == 4 || prop_location[2] == 6 || prop_location[2] ==8 || prop_location[2] ==10 || prop_location[2] ==12 || prop_location[2] ==14 || prop_location[2] ==16 || prop_location[2] ==18 || prop_location[2] ==20 || prop_location[2] ==22 || prop_location[2] ==24 || prop_location[2] ==26 || prop_location[2] ==28 || prop_location[2] ==30 || prop_location[2] ==32 || prop_location[2] ==34 || prop_location[2] ==36)"


MC = ROOT.TH1D("MC", "MC", xbins, low_pt, high_pt)
data = ROOT.TH1D("data", "data", xbins, low_pt, high_pt)
weight = ROOT.TH1D("weight", "weight", xbins, low_pt, high_pt)
h = ROOT.TH1D("h", "h", xbins, xlow, xhigh)
h0 = ROOT.TH1D("h0", "h0", xbins, xlow, xhigh)
h1 = ROOT.TH1D("h1", "h1", xbins, xlow, xhigh)
h2 = ROOT.TH1D("h2", "h2", xbins, xlow, xhigh)

xAxis = h0.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
xAxis.SetNdivisions(-505)
#xAxis.SetTitle("#DeltaR#phi [cm]")
xAxis.SetTitle("|bending angle| [mrad]")
#xAxis.SetTitle("p_{T} [GeV]")
#xAxis.CenterTitle()

event2.Project("MC", "muon_pt", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && muon_pt>{low} && muon_pt<{high}".format(low=low_pt, high=high_pt))

#weight = data.Clone()
event1.Project("weight", "muon_pt", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && muon_pt>{low} && muon_pt<{high}".format(low=low_pt, high=high_pt)) #this is the aligned data histogram
weight.Divide(MC)



event0.Project("h0", "1000*abs(bending_angle)", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && muon_pt>{low} && muon_pt<{high} && {cut}".format(low=low_pt, high=high_pt, cut=odd_cut)) #&& prop_location[3]=={L}".format(low=low_pt, high=high_pt, cut=even_cut, L=layer))
event1.Project("h1", "1000*abs(bending_angle)", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && muon_pt>{low} && muon_pt<{high} && {cut}".format(low=low_pt, high=high_pt, cut=odd_cut)) # && prop_location[3]=={L}".format(low=low_pt, high=high_pt, cut=even_cut, L=layer))
#event2.Project("h", "1000*abs(bending_angle)", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && has_fidcut && muon_pt>{low} && muon_pt<{high} && {cut}".format(low=low_pt, high=high_pt, cut=odd_cut)) # && prop_location[3]=={L}".format(low=low_pt, high=high_pt, cut=even_cut, L=layer))

#counter_data = 0
'''
for i in event1:
  #counter_data += 1
  #bin_pt = weight.FindBin(i.muon_pt)
  #print("data: \t", bin_pt, weight.GetBinContent(bin_pt))
  #if counter_data > 10000: break
  if i.muon_pt > low_pt and i.muon_pt < high_pt and i.n_ME11_segment == 1 and i.has_fidcut and abs(i.RdPhi_Corrected) < 2 and i.prop_location[2] % 2 != 0:
    bin_pt = weight.FindBin(i.muon_pt)
    print("data: \t", bin_pt, weight.GetBinContent(bin_pt))
    #print("\t\t", i.bending_angle, i.muon_pt)
    h1.Fill(abs(i.bending_angle), weight.GetBinContent(bin_pt))
'''
counter = 0

for i in event2:
  counter += 1
  #bin_pt = weight.FindBin(i.muon_pt)
  #print("MC: \t", bin_pt, weight.GetBinContent(bin_pt))
  #if counter > 1: break
  if i.muon_pt > low_pt and i.muon_pt < high_pt and i.n_ME11_segment == 1 and i.has_fidcut and abs(i.RdPhi_Corrected) < 2 and i.prop_location[2] % 2 != 0:# and i.prop_location[3] == layer:
    bin_pt = weight.FindBin(i.muon_pt)
    #print("MC: event:\t", counter, bin_pt, weight.GetBinContent(bin_pt))
    #print("\t\t", i.bending_angle, i.muon_pt)
    h2.Fill(1000*abs(i.bending_angle), weight.GetBinContent(bin_pt))

#h.SetLineColor(ROOT.kViolet+1)
h0.SetLineColor(ROOT.kBlue)
h1.SetLineColor(ROOT.kGreen+2)
h2.SetLineColor(ROOT.kRed)

#h.SetLineStyle(10)
h0.SetLineStyle(1)
h1.SetLineStyle(2)
h2.SetLineStyle(9)

#h.Scale(1/h.Integral())
h0.Scale(1/h0.Integral())
h1.Scale(1/h1.Integral())
h2.Scale(1/h2.Integral())

yList = [h0.GetMaximum(), h1.GetMaximum(), h2.GetMaximum()]
yAxis = h0.GetYaxis()
yAxis.SetRangeUser(0, 1.1*max(h0.GetMaximum(), h1.GetMaximum(), h2.GetMaximum()))#, h.GetMaximum()))
#yAxis.SetRangeUser(0, 0.05)
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("A.U.")

#h.SetMarkerSize(0)
h0.SetMarkerSize(0)
h1.SetMarkerSize(0)
h2.SetMarkerSize(0)

#h.SetLineWidth(1)
h0.SetLineWidth(2)
h1.SetLineWidth(4)
h2.SetLineWidth(4)

#h.Draw("HIST")
h0.Draw("HIST")
h1.Draw("HIST SAME")
h2.Draw("HIST SAME")
#h.Draw("HIST SAME")

colorPal = [ROOT.kBlue, ROOT.kGreen+2, ROOT.kRed]#, ROOT.kViolet+1, ROOT.kTeal, ROOT.kPink+6]
histList = [h0, h1, h2]#, h3, h4, h5]
lineList = ["l0", "l1", "l2"]#, "l3", "l4", "l5"]

for i in range(3):
  mean = round(histList[i].GetMean(),3)
  lineList[i] = ROOT.TLine(mean, 0, mean, yList[i])
  lineList[i].SetLineColor(colorPal[i])
  #if i<3:
  lineList[i].SetLineStyle(1)
  #else:
  #lineList[i].SetLineStyle(3)
  lineList[i].Draw()

rootkde = ROOT.TLegend(0.5,0.72,0.9,0.87)
#rootkde.AddEntry(h0,"30 GeV < p_{T} < 40 GeV")
#rootkde.AddEntry(h,"40 GeV < p_{T} < 50 GeV")
#rootkde.AddEntry(h1,"50 GeV < p_{T} < 90 GeV")
#rootkde.AddEntry(h2,"90 GeV < p_{T} < 200 GeV")
#rootkde.AddEntry(h,"Before Alignment Run 2022D")
#rootkde.AddEntry(h,"SingleMuonGun 2021 design: Unweighted Mean: {mean}".format(mean = round(h.GetMean(),3)))
rootkde.AddEntry(h0,"Before Alignment")# Mean: {mean}".format(mean = round(h0.GetMean(),3)))
rootkde.AddEntry(h1,"After Alignment")# Mean: {mean}".format(mean = round(h1.GetMean(),3)))
rootkde.AddEntry(h2,"Design: Weighted")# Mean: {mean}".format(mean = round(h2.GetMean(),3)))
rootkde.SetTextSize(0.)
rootkde.SetBorderSize(0)
rootkde.Draw()

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.35*canvas.GetTopMargin())

latex.SetTextAlign(32)
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())+int(h1.GetEntries())))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))
latex.SetTextColor(ROOT.kBlack)
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(12)
latex.SetTextSize(0.26*canvas.GetTopMargin())
latex.DrawLatex(0.65-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "2022D")
latex.SetTextSize(0.33*canvas.GetTopMargin())
#latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.5*canvas.GetTopMargin(), "Run 2022D Pre-Alignment")
#latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.5*canvas.GetTopMargin(), "singleMuonGun 2021 Design")
latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.6*canvas.GetTopMargin(), "{low} GeV".format(low=low_pt)+" < p_{T}^{GLB} "+"< {high} GeV".format(high=high_pt))
latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.0*canvas.GetTopMargin(), "Odd Chambers")#, Layer {L}".format(L=layer))
#latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.1*canvas.GetTopMargin(), "positive muons")
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Region: {reg}".format(reg = reg))

latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.4*canvas.GetTopMargin())
latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Simulation Preliminary")
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Work in Progress")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()


#if os.path.exists("Run{run}/{version}".format(run=year, version=version0)) == False:
#  os.mkdir("Run{run}/{version}".format(run=year, version=version0))
#canvas.SaveAs("Run{run}/{version}/bending_angle_pTdependency.png".format(run=year, version=version0))

#canvas.SaveAs("singleMuonGun_11_3_4_2021_design/bending_angle_pTdependency.png")
#canvas.SaveAs("singleMuonGun_11_3_4_2021_design/evenChambers_L1.png")
canvas.SaveAs("Run2022D/Bending_Angle_single_plots/Weighted/v2/pt{low}to{high}_oddChambers_test.png".format(low=low_pt, high=high_pt))
