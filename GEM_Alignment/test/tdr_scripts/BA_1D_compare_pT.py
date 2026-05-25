import ROOT, tdrstyle, sys, os, array

supch_cut = 0 #0 even, 1 odd, for both "both"
endcap = 1
layer = 1
charge = 1
x_var = "BA" #"BA" or "rdphi" 

year = "2025C" #change between 2022B and 2022C for example
fdata_post = ROOT.TFile(f"/eos/user/t/toakhter/tamu_mual/2025/{year}/Run{year}_muon0_ZMu_150X_dataRun3_Prompt_v1_aligned_backprop.root")
eventme11_post = fdata_post.Get("analyzer/ME11Seg_Prop")

ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

if x_var == "BA":
  xlow = -6 #-10
  xhigh = 6 #10
  x_plot = "1000*bending_angle"
  x_axis = "#Phi_{bending} [mRad]" #"Bending Angle [mrad]"
elif x_var == "rdphi":
  xlow = -2
  xhigh = 2
  x_plot = "RdPhi_Corrected"
  x_axis = "#DeltaR#phi [cm]"

if endcap==1:
  reg_string="+"
elif endcap==-1:
  reg_string="-"

if charge==1:
  mu_str = "posmu"
  mu_notation = "#mu^{+}"
elif charge==-1:
  mu_str = "negmu"
  mu_notation ="#mu^{-}"

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
pt10 = ROOT.TH1D("pt10", "pt10", xbins, xlow, xhigh)
pt20 = ROOT.TH1D("pt20", "pt20", xbins, xlow, xhigh)
pt30 = ROOT.TH1D("pt30", "pt30", xbins, xlow, xhigh)
pt60 = ROOT.TH1D("pt60", "pt60", xbins, xlow, xhigh)
xAxis = pt10.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
#xAxis.SetNdivisions(-505)
# xAxis.SetTitle("#DeltaR#phi [cm]")
xAxis.SetTitle(f"{x_axis}")
#xAxis.SetTitle("p_{T} [GeV]")
#xAxis.CenterTitle()

yAxis = pt10.GetYaxis()
yAxis.SetTitleOffset(0)
yAxis.SetTitleSize(0.05)
yAxis.SetTitle("A.U.")
# yAxis.SetTitle("Entries")
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

# eventMCme11.Project("hMCme11", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, cut=cut))
# eventMCtrack.Project("hMCtrak", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, cut=cut))
# eventme11.Project("hme11", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, cut=cut))
# eventtrack.Project("htrack", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, cut=cut))
eventme11_post.Project("pt10", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=10, high=10.5, reg=endcap, lay=layer, charge=charge, cut=cut))
eventme11_post.Project("pt20", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=20, high=21, reg=endcap, lay=layer, charge=charge, cut=cut))
eventme11_post.Project("pt30", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=30, high=31.5, reg=endcap, lay=layer, charge=charge, cut=cut))
eventme11_post.Project("pt60", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=60, high=63, reg=endcap, lay=layer, charge=charge, cut=cut))


#h.ResetStats()
#h.GetSumOfWeights()
pt10.Scale(1/pt10.Integral())
pt20.Scale(1/pt20.Integral())
pt30.Scale(1/pt30.Integral())
pt60.Scale(1/pt60.Integral())

pt10.SetLineWidth(3)
pt20.SetLineWidth(3)
pt30.SetLineWidth(3)
pt60.SetLineWidth(3)


#hMCme11.SetLineStyle(1) 
#hme11.SetLineStyle(1) #2

pt10.SetMarkerSize(0)
pt20.SetMarkerSize(0)
pt30.SetMarkerSize(0)
pt60.SetMarkerSize(0)

pt10.SetLineColor(ROOT.kViolet-2)
pt20.SetLineColor(ROOT.kBlue)
pt30.SetLineColor(ROOT.kGreen+2)
pt60.SetLineColor(ROOT.kRed)
#h.SetFillColorAlpha(ROOT.kBlue, 0.3)
#h1.SetFillColorAlpha(ROOT.kGreen+2, 0.3)
#h2.SetFillColorAlpha(ROOT.kRed, 0.3)

#yAxis.SetRangeUser(0, 1.1*h.GetMaximum())
yAxis.SetRangeUser(0, 1.6*max(pt10.GetMaximum(), pt20.GetMaximum(), pt30.GetMaximum(), pt60.GetMaximum() ))
yAxis.SetMaxDigits(3)

pt10.Draw("HIST")
pt20.Draw("HIST SAME")
pt30.Draw("HIST SAME")
pt60.Draw("HIST SAME")

legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.85)
legend.AddEntry(pt10, "10<p_{T}<10.5 GeV")
legend.AddEntry(pt20, "20<p_{T}<21 GeV")
legend.AddEntry(pt30, "30<p_{T}<31.5 GeV")
legend.AddEntry(pt60, "60<p_{T}<63 GeV")
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
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
#latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))
latex.DrawLatex(1-3.5*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "{run}".format(run=year[:-1]))
latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
latex.SetTextAlign(12)



latex.SetTextSize(0.25*canvas.GetTopMargin())
latex.DrawLatex(0.65-0.5*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.7*canvas.GetTopMargin(), "{reg}Endcap Station 1 Layer {lay}".format(reg=reg_string, lay=layer))
latex.DrawLatex(0.65-0.5*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.0*canvas.GetTopMargin(), "{ch_string} chambers".format(ch_string=ch_string))
latex.DrawLatex(1-2.0*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-2.0*canvas.GetTopMargin(), f"{mu_notation}")

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
# canvas.SaveAs("{x_var}_1D_R{reg}L{lay}_{ch_string}chambers.png".format(reg=endcap, ch_string=ch_string, lay=layer, x_var=x_var))
canvas.SaveAs("{x_var}_1D_R{reg}L{lay}_{ch_string}chambers_{mu_str}_pt.png".format(reg=endcap, ch_string=ch_string, lay=layer, x_var=x_var, mu_str=mu_str))
