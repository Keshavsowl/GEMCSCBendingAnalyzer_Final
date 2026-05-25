import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh

low_pt=75
high_pt=200
supch_cut = 1 #0=even, 1=odd superchamber cut
endcap = -1
layer = 2
charge = -1
if charge==1:
  mu_str = "posmu"
  mu_notation = "#mu^{+}"
elif charge==-1:
  mu_str = "negmu"
  mu_notation ="#mu^{-}"

year = "2022D" #change between 2022B and 2022C for example
version0 = "ZMu_PromptReco_RAWRECO_globalMu_pfisotight_v7" #File version
version1 = "ZMu_PromptReco_RAWRECO_globalMu_pfisotight_aligned_v7"
version = "Bending_Angles/chamberLevel/cutPFIsoTight_onDataOnly/byCharge/pt{low}to{high}_Region{reg}_layer{lay}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer)

#f = ROOT.TFile("{}".format(sys.argv[1]))
f0 = ROOT.TFile("../Run{run}_{version}.root".format(run=year, version=version0))
f1 = ROOT.TFile("../Run{run}_{version}.root".format(run=year, version=version1))
f2 = ROOT.TFile("../../../../../../BeamCommissioning_12_4_6/src/GEMCSCBendingAnalyzer/GEM_Alignment/test/singleMuonGun_11_3_4_2021_design_v0.root")

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

#h0 = ROOT.TH1D("h0", "h0", xbins, xlow, xhigh)
h = ROOT.TH1D("h", "h", xbins, xlow, xhigh)
h1 = ROOT.TH1D("h1", "h1", xbins, xlow, xhigh)
h2 = ROOT.TH1D("h2", "h2", xbins, xlow, xhigh)
xAxis = h.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
xAxis.SetNdivisions(-505)
#xAxis.SetTitle("#DeltaR#phi [cm]")
xAxis.SetTitle("|bending angle| [mrad]")
#xAxis.SetTitle("p_{T} [GeV]")
#xAxis.CenterTitle()

ch_list = []
ch_list_even = []
ch_list_odd = []
even_cut = ""
odd_cut = ""

if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"

for i in range(1,37):
  ch_list.append(str(i))
  if i%2 == 0:
    ch_list_even.append(str(i))
    if i==2:
      even_cut += "(prop_location[2]== {i} ||".format(i=i)
    elif i==36:
      even_cut += " prop_location[2] == {i})".format(i=i)
    else:
      even_cut += " prop_location[2] == {i} ||".format(i=i)
  else:
    ch_list_odd.append(str(i))
    if i==1:
      odd_cut += "(prop_location[2]== {i} ||".format(i=i)
    elif i==35:
      odd_cut += " prop_location[2] == {i})".format(i=i)
    else:
      odd_cut += " prop_location[2] == {i} ||".format(i=i)

#print(even_cut)
#print(odd_cut)

if supch_cut==0:
  cut = even_cut
  ch_string = "Even"
elif supch_cut==1:
  cut = odd_cut
  ch_string = "Odd"


for ch in range(1, 37):
  if (endcap==-1 and (ch==25 or ch==26)):
    continue
  if ch % 2 == supch_cut: #odd chambers ch % 2 ==1; even chambers ch % 2 ==0;
    event0.Project("h", "1000*abs(bending_angle)", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && muon_pt>{low} && muon_pt<{high} && has_fidcut && has_TightID==1 && prop_location[2]=={ch} && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={mu}".format(low=low_pt, high=high_pt, ch=ch, reg=endcap, lay=layer, mu=charge))
    event1.Project("h1", "1000*abs(bending_angle)", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && muon_pt>{low} && muon_pt<{high} && has_fidcut && has_TightID==1 && prop_location[2]=={ch} && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={mu}".format(low=low_pt, high=high_pt, ch=ch, reg=endcap, lay=layer, mu=charge))
    event2.Project("h2", "1000*abs(bending_angle)", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && muon_pt>{low} && muon_pt<{high} && has_fidcut && prop_location[2]=={ch} && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={mu}".format(low=low_pt, high=high_pt, ch=ch, reg=endcap, lay=layer, mu=charge))


#h0.SetLineColor(ROOT.kViolet+1)
    h.SetLineColor(ROOT.kGreen+2)
    h1.SetLineColor(ROOT.kBlue)
    h2.SetLineColor(ROOT.kRed)

    h.SetLineStyle(1)
    h1.SetLineStyle(2)
    h2.SetLineStyle(9)
#h0.Scale(1/h0.Integral())
    h.Scale(1/h.Integral())
    h1.Scale(1/h1.Integral())
    h2.Scale(1/h2.Integral())

    yList = [h.GetMaximum(), h1.GetMaximum(), h2.GetMaximum()]
    yAxis = h.GetYaxis()
    yAxis.SetRangeUser(0, 1.2*max(h.GetMaximum(), h1.GetMaximum(), h2.GetMaximum()))
#yAxis.SetRangeUser(0, 0.24)
    yAxis.SetTitleOffset(0)
    yAxis.SetTitleSize(0.05)
    yAxis.SetTitle("A.U.")

    h.SetMarkerSize(0)
    h1.SetMarkerSize(0)
    h2.SetMarkerSize(0)
#h0.SetLineWidth(3)
#h.SetLineWidth(2)
    h1.SetLineWidth(4)
#h2.SetLineWidth(2)
#h0.Draw("hist")
    h.Draw("HIST")
    h1.Draw("HIST SAME")
    h2.Draw("HIST SAME")

    colorPal = [ROOT.kGreen+2, ROOT.kBlue, ROOT.kRed]
    histList = [h, h1, h2]
    lineList = ["l", "l1", "l2"]

    for i in range(3):
      mean = round(histList[i].GetMean(),3)
      lineList[i] = ROOT.TLine(mean, 0, mean, yList[i])
      lineList[i].SetLineColor(colorPal[i])
      #if i<3:
      lineList[i].SetLineStyle(1)
      #else:
      #lineList[i].SetLineStyle(3)
      lineList[i].Draw()

    rootkde = ROOT.TLegend(0.5,0.73,0.9,0.85)
    rootkde.AddEntry(h,"Before Alignment")
    rootkde.AddEntry(h1,"After Alignment")
    rootkde.AddEntry(h2,"2021 Design")
    rootkde.SetBorderSize(0)
    rootkde.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)

    latex.SetTextFont(42)
    latex.SetTextSize(0.35*canvas.GetTopMargin())

    latex.SetTextAlign(32)
#latex.SetTextColor(ROOT.kViolet+1)
#latex.SetTextColor(ROOT.kRed)
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())+int(h1.GetEntries())))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))
    latex.SetTextColor(ROOT.kBlack)
    latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
    latex.SetTextAlign(12)
    latex.SetTextSize(0.27*canvas.GetTopMargin())
    latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.5*canvas.GetTopMargin(), "{low} GeV".format(low=low_pt) +"< p_{T}^{GLB} < "+"{high} GeV".format(high=high_pt))
    latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.8*canvas.GetTopMargin(), "{reg}Endcap, superChamber {ch}".format(reg=reg_string, ch=ch))
    latex.DrawLatex(0.55-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.1*canvas.GetTopMargin(), "Layer {lay}, {mu}".format(lay=layer, mu=mu_notation))

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


    if os.path.exists("Run{run}/{version}".format(run=year, version=version)) == False:
      os.mkdir("Run{run}/{version}".format(run=year, version=version))
    canvas.SaveAs("Run{run}/{version}/pt{low}to{high}_{ch_str}SC{ch}_R{reg}L{lay}_{mu}.png".format(run=year, version=version, low=low_pt, high=high_pt, ch_str=ch_string, ch=ch, reg=endcap, lay=layer, mu=mu_str))
