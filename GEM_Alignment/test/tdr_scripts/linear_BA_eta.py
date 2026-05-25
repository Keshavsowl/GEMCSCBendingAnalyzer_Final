import ROOT, tdrstyle, sys, os, array

par_var = "dx1cm"
low_pt=30
high_pt=200
endcap = -1
supch_cut = 1 #0=even, 1=odd superchamber cut
layer = 1
#eta = 1
#charge = -1

f0 = ROOT.TFile("../singleMuonGun_11_3_4_2021_design_idealGEMmisalignedME11_{par}.root".format(par=par_var))
#f2 = ROOT.TFile("../../../../../../BeamCommissioning_12_4_6/src/GEMCSCBendingAnalyzer/GEM_Alignment/test/singleMuonGun_11_3_4_2021_design_v0.root")

event0 = f0.Get("analyzer/ME11Seg_Prop")
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

ybins = 100
ylow = -10
yhigh = 10

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

#h = ROOT.TH1D("h", "h", xbins, xlow, xhigh)
h1 = ROOT.TH1D("h1", "h1", ybins, ylow, yhigh)
h2 = ROOT.TH1D("h2", "h2", ybins, ylow, yhigh)

if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"

ch_list = []
ch_list_even = []
ch_list_odd = []
even_cut = ""
odd_cut = ""

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

if supch_cut==0:
  cut = even_cut
  ch_string = "Even"
elif supch_cut==1:
  cut = odd_cut
  ch_string = "Odd"

mg = ROOT.TMultiGraph()

xAxis = mg.GetXaxis()
xAxis.SetTitleOffset(1)
xAxis.SetTitleSize(0.05)
xAxis.SetLimits(0.5, 8.5)
xAxis.SetTitle("#eta Partition")

yAxis = mg.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.04)
yAxis.SetRangeUser(ylow+2, 2)
yAxis.SetTitle("Average Bending Angle [mrad]")

counter = -11
for j in range(1, 37):
  if j % 2 == supch_cut:
    continue
  counter += 1
  eta_arr = array.array('d', [1, 2, 3, 4, 5, 6, 7, 8])
  BA_neg, BA_pos, BA_neg_err, BA_pos_err = array.array('d'), array.array('d'), array.array('d'), array.array('d')
  xerr_arr = array.array('d', [0, 0, 0, 0, 0, 0, 0, 0])

  for i in range(1, 9):
    event0.Project("h1", "1000*bending_angle", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && muon_pt > {low} && muon_pt < {high} && has_fidcut && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge==-1 && prop_location[2]=={ch} && prop_location[4]=={eta}".format(low=low_pt, high=high_pt, reg=endcap, ch=j, lay=layer, eta=i))
    event0.Project("h2", "1000*bending_angle", "abs(RdPhi_Corrected) < 2 && n_ME11_segment == 1 && muon_pt > {low} && muon_pt < {high} && has_fidcut && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge==1 && prop_location[2]=={ch} && prop_location[4]=={eta}".format(low=low_pt, high=high_pt, reg=endcap, ch=j, lay=layer, eta=i))

    BA_neg.append(h1.GetMean())
    BA_pos.append(h2.GetMean())
    BA_neg_err.append(h1.GetStdDev())
    BA_pos_err.append(h2.GetStdDev())

  gr_neg = ROOT.TGraphErrors(8, eta_arr, BA_neg, xerr_arr, BA_neg_err)
  gr_pos = ROOT.TGraphErrors(8, eta_arr, BA_pos, xerr_arr, BA_pos_err)

  gr_neg.SetMarkerColor(ROOT.kRed+counter)
  gr_pos.SetMarkerColor(ROOT.kBlue+counter)

  gr_neg.Fit("pol1")
  gr_pos.Fit("pol1")

  gr_neg.SetLineColor(ROOT.kRed+counter)
  gr_pos.SetLineColor(ROOT.kBlue+counter)

  if counter == 4:
    counter = -11

  mg.Add(gr_neg)
  mg.Add(gr_pos)

mg.Draw('AP') #'ACP' for joined Curve


latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.35*canvas.GetTopMargin())

latex.SetTextAlign(32)
latex.SetTextColor(ROOT.kBlack)
latex.SetTextAlign(12)
latex.SetTextSize(0.3*canvas.GetTopMargin())
latex.DrawLatex(0.5-0.4*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "{low} GeV < ".format(low=low_pt)+"p_{T}"+" < {high} GeV".format(high=high_pt))
latex.DrawLatex(0.45-0.4*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "{reg}Endcap, {ch} chambers, Layer {lay}".format(reg=reg_string, ch=ch_string, lay=layer))

latex.SetTextSize(0.4*canvas.GetTopMargin())
latex.SetTextColor(ROOT.kBlue)
latex.DrawLatex(0.7-0.4*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "#mu^{+}")
latex.SetTextColor(ROOT.kRed)
latex.DrawLatex(0.8-0.4*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "#mu^{-}")

latex.SetTextColor(ROOT.kBlack)
latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.4*canvas.GetTopMargin())
latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Simulation Preliminary")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

frame = canvas.GetFrame()
frame.Draw()

canvas.SaveAs("MC_idealGEMmisalignedME11/{par}/BA_eta_linear/linear_BA_pt{low}to{high}_R{reg}_{ch}Chambers_L{lay}.png".format(par=par_var, low=low_pt, high=high_pt, reg=endcap, lay=layer, ch=ch_string))
