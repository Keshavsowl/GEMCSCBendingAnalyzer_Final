import ROOT, tdrstyle, sys, os, array

low_pt=30
high_pt=200
supch_cut = "both" #0 even, 1 odd, for both "both"
endcap = -1
layer = 1
#charge = -1
x_var = "rdphi" #"BA" or "rdphi" 

year = "2024H" #change between 2022B and 2022C for example

f0 = ROOT.TFile("/eos/user/t/toakhter/tamu_mual/2024/2024H/Run2024H_muon0_150X_dataRun3_Prompt_v1.root")
#fMC = ROOT.TFile("/eos/user/t/toakhter/tamu_mual/2022/singleMuonGun_11_3_4_2021_design_v0.root")

event0 = f0.Get("analyzer/ME11SegReco_Prop")
event1 = f0.Get("analyzer/InnerRefit_Prop")
#event = f.Get("analyzer/Inner_Prop")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

if x_var == "BA":
  xlow = -10
  xhigh = 10
  x_plot = "1000*bending_angle"
  x_axis = "Bending Angle [mrad]"
elif x_var == "rdphi":
  xlow = -2
  xhigh = 2
  x_plot = "RdPhi_Corrected"
  x_axis = "#DeltaR#phi [cm]"

if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"
'''
if charge==1:
  mu_str = "posmu"
  mu_notation = "#mu^{+}"
elif charge==-1:
  mu_str = "negmu"
  mu_notation ="#mu^{-}"
'''
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
xlow = -2
xhigh = 2
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
canvas.SetGrid()

#h0 = ROOT.TH1D("h0", "h0", xbins, xlow, xhigh)
h = ROOT.TH1D("h", "h", xbins, xlow, xhigh)
h1 = ROOT.TH1D("h1", "h1", xbins, xlow, xhigh)
#h2 = ROOT.TH1D("h2", "h2", xbins, xlow, xhigh)
xAxis = h.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
#xAxis.SetNdivisions(-505)
xAxis.SetTitle("#DeltaR#phi [cm]")
#xAxis.SetTitle("|bending angle| [mrad]")
#xAxis.SetTitle("p_{T} [GeV]")
#xAxis.CenterTitle()

yAxis = h.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
#yAxis.SetTitle("A.U.")
yAxis.SetTitle("Entries")
#yAxis.CenterTitle()

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
elif supch_cut=="both":
  ch_string = "All"

#print(even_cut)
#print(odd_cut)

event0.Project("h", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer))
event1.Project("h1", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer))

#h.ResetStats()
#h.GetSumOfWeights()
#h.Scale(1/h.Integral())
#h1.Scale(1/h1.Integral())
#h2.Scale(1/h2.Integral())

h.SetLineWidth(3) #3
h1.SetLineWidth(3)
# h2.SetLineWidth(3)

h.SetMarkerSize(0)
h1.SetMarkerSize(0)
# h2.SetMarkerSize(0)

h.SetLineColor(ROOT.kBlue)
h1.SetLineColor(ROOT.kGreen+2)
# h2.SetLineColor(ROOT.kRed)
#h.SetFillColorAlpha(ROOT.kBlue, 0.3)
#h1.SetFillColorAlpha(ROOT.kGreen+2, 0.3)
#h2.SetFillColorAlpha(ROOT.kRed, 0.3)

yAxis.SetRangeUser(0, 1.6*max(h.GetMaximum(), h1.GetMaximum() ))
yAxis.SetMaxDigits(3)

h.Draw("HIST")
h1.Draw("HIST SAME")
# h2.Draw("HIST SAME")

legend = ROOT.TLegend(0.55, 0.75, 0.9, 0.85)
legend.AddEntry(h, f"CSC back prop")
legend.AddEntry(h1, f"track prop")
legend.SetTextSize(0.)
legend.SetBorderSize(0)
legend.Draw()

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextAngle(0)
latex.SetTextColor(ROOT.kBlack)

latex.SetTextFont(42)
latex.SetTextSize(0.3*canvas.GetTopMargin())

latex.SetTextAlign(32)
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(12)

latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-1.0*canvas.GetTopMargin(), "Run {run}".format(run=year))

latex.SetTextSize(0.25*canvas.GetTopMargin())
#latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-1.2*canvas.GetTopMargin(), "{low} GeV".format(low=low_pt)+" < p_{T}^{GLB} < "+"{high} GeV".format(high=high_pt)) 
latex.DrawLatex(0.65-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.8*canvas.GetTopMargin(), "{reg}Endcap Layer {lay}".format(reg=reg_string, lay=layer))
latex.DrawLatex(0.65-0.3*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.1*canvas.GetTopMargin(), "{ch_string} chambers".format(ch_string=ch_string))

latex.SetTextSize(0.5*canvas.GetTopMargin())
latex.SetTextFont(61)
#latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.27*canvas.GetTopMargin(), "CMS")
latex.SetTextFont(52)
latex.SetTextSize(0.3*canvas.GetTopMargin())
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Preliminary")
#latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Work in Progress")

latex.SetTextFont(42)
latex.SetTextSize(0.4*canvas.GetTopMargin())

###fit function part below
latex.SetTextAlign(12)
latex.SetTextSize(0.03)
latex.SetTextFont(61)
#latex.DrawLatex(0.3*canvas.GetLeftMargin(), -0.04+ 0.5*canvas.GetBottomMargin(), "{zer}* exp(-0.5*((x- {one}) / {two})^2) + {three}* exp(-0.5*((x- {four}) / {five})^2)".format(zer = round(f1.GetParameter(0), 3), one = round(f1.GetParameter(1), 3), two = round(f1.GetParameter(2), 3), three = round(f1.GetParameter(3), 3), four = round(f1.GetParameter(4), 3), five = round(f1.GetParameter(5), 3),))

###


frame = canvas.GetFrame()
frame.Draw()


#if os.path.exists("Run{run}/{version}".format(run=year, version=version)) == False:
#  os.mkdir("Run{run}/{version}".format(run=year, version=version))
#canvas.SaveAs("Run{run}/{version}/1D_RdPhi_pt{low}to{high}_{ch_string}chambers_R{reg}_L{lay}.png".format(run=year, version=version, low=low_pt, high=high_pt, reg=endcap, lay=layer, ch_string=ch_string))
canvas.SaveAs("{x_var}_1D_R{reg}L{lay}_{ch_string}chambers.png".format(reg=endcap, ch_string=ch_string, lay=layer, x_var=x_var))



##########fit

# h.SetFillColorAlpha(ROOT.kBlue, 0.3)
# h1.SetFillColorAlpha(ROOT.kGreen+2, 0.2)

#f = ROOT.TF1("f", "[0]* exp([1]*x**2 + [2]) + [3]* exp([4]*x**2 + [5])", -1.5, 1.5)
f = ROOT.TF1("f", "[0]* exp(-0.5*((x-[1])/[2])**2) + [3]* exp(-0.5*((x-[4])/[5])**2)", -0.5, 0.5)
# f = ROOT.TF1("f", "gaus(0)+gaus(3)", -0.5, 0.5)
f.SetParameters(h.GetMaximum(), h.GetMean(), h.GetStdDev(), 0.2*h.GetMaximum(), h.GetMean(), h.GetStdDev())
f.SetLineColor(ROOT.kRed)
f.SetLineStyle(7)
f.SetMarkerSize(0)
h.Fit("f")
f.Draw("same")

f1 = ROOT.TF1("f1", "[0]* exp(-0.5*((x-[1])/[2])**2) + [3]* exp(-0.5*((x-[4])/[5])**2)", -0.5, 0.5)
f1.SetParameters(h1.GetMaximum(), h1.GetMean(), h1.GetStdDev(), 0.2*h1.GetMaximum(), h1.GetMean(), h1.GetStdDev())
f1.SetLineColor(ROOT.kOrange)
f1.SetLineStyle(7)
f1.SetMarkerSize(0)
h1.Fit("f1")
f1.Draw("same")

legend_fit = ROOT.TLegend(0.4, 0.7, 0.95, 0.87)
legend_fit.AddEntry(h, f"CSC back prop")
legend_fit.AddEntry(f, f"  gaus 1  mean: {f.GetParameter(1):.3f} #pm {f.GetParError(1):.3f} , std dev: {f.GetParameter(2):.3f} #pm {f.GetParError(2):.3f}")
legend_fit.AddEntry(f, f"  gaus 2  mean: {f.GetParameter(4):.3f} #pm {f.GetParError(4):.3f} , std dev: {f.GetParameter(5):.3f} #pm {f.GetParError(5):.3f}")
legend_fit.AddEntry(h1, f"track prop")
legend_fit.AddEntry(f1, f"  gaus 1  mean: {f1.GetParameter(1):.3f} #pm {f1.GetParError(1):.3f} , std dev: {f1.GetParameter(2):.3f} #pm {f1.GetParError(2):.3f}")
legend_fit.AddEntry(f1, f"  gaus 2  mean: {f1.GetParameter(4):.3f} #pm {f1.GetParError(4):.3f} , std dev: {f1.GetParameter(5):.3f} #pm {f1.GetParError(5):.3f}")

legend_fit.SetTextSize(0.)
legend_fit.SetBorderSize(0)
legend_fit.Draw()

canvas.SaveAs("{x_var}_1D_R{reg}L{lay}_{ch_string}chambers_fit.png".format(reg=endcap, ch_string=ch_string, lay=layer, x_var=x_var))
