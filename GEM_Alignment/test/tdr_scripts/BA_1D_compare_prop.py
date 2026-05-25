import ROOT, tdrstyle, sys, os, array

low_pt=30
high_pt=35
supch_cut = 1 #0 even, 1 odd, for both "both"
endcap = 1
layer = 1
charge = -1
x_var = "BA" #"BA" or "rdphi" 

year = "2025C" #change between 2022B and 2022C for example

fdata_pre = ROOT.TFile(f"/eos/user/t/toakhter/tamu_mual/2025/{year}/Run{year}_muon0_ZMu_150X_dataRun3_Prompt_v1.root")
fdata_post = ROOT.TFile(f"/eos/user/t/toakhter/tamu_mual/2025/{year}/Run{year}_muon0_ZMu_150X_dataRun3_Prompt_v1_aligned_backprop.root")
fMC = ROOT.TFile("/eos/user/t/toakhter/tamu_mual/2022/singleMuonGun_11_3_4_2021_design_v0.root")

eventme11_pre = fdata_pre.Get("analyzer/ME11Seg_Prop")
eventme11_post = fdata_post.Get("analyzer/ME11Seg_Prop")
eventMCme11 = fMC.Get("analyzer/ME11Seg_Prop")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

if x_var == "BA":
  xlow = -5
  xhigh = 5
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
hMCme11 = ROOT.TH1D("hMCme11", "hMCme11", xbins, xlow, xhigh)
hme11_pre = ROOT.TH1D("hme11_pre", "hme11_pre", xbins, xlow, xhigh)
hme11_post = ROOT.TH1D("hme11_post", "hme11_post", xbins, xlow, xhigh)
xAxis = hMCme11.GetXaxis()
xAxis.SetTitleOffset(0)
xAxis.SetTitleSize(0.05)
#xAxis.SetNdivisions(-505)
# xAxis.SetTitle("#DeltaR#phi [cm]")
xAxis.SetTitle(f"{x_axis}")
#xAxis.SetTitle("p_{T} [GeV]")
#xAxis.CenterTitle()

yAxis = hMCme11.GetYaxis()
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
eventMCme11.Project("hMCme11", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, charge=charge, cut=cut))
eventme11_pre.Project("hme11_pre", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, charge=charge, cut=cut))
eventme11_post.Project("hme11_post", "{x}".format(x=x_plot), "muon_pt>{low} && muon_pt<{high} && n_ME11_segment==1 && has_fidcut && abs(RdPhi_Corrected) < 2 && prop_location[0]=={reg} && prop_location[3]=={lay} && muon_charge=={charge} && {cut}".format(low=low_pt, high=high_pt, reg=endcap, lay=layer, charge=charge, cut=cut))

#h.ResetStats()
#h.GetSumOfWeights()
hMCme11.Scale(1/hMCme11.Integral())
hme11_pre.Scale(1/hme11_pre.Integral())
hme11_post.Scale(1/hme11_post.Integral())

hMCme11.SetLineWidth(3) #3
hme11_pre.SetLineWidth(3)
hme11_post.SetLineWidth(3)

#hMCme11.SetLineStyle(1) 
#hme11.SetLineStyle(1) #2

hMCme11.SetMarkerSize(0)
hme11_pre.SetMarkerSize(0)
hme11_post.SetMarkerSize(0)

hMCme11.SetLineColor(ROOT.kRed)
hme11_pre.SetLineColor(ROOT.kBlue)
hme11_post.SetLineColor(ROOT.kGreen+2)
#h.SetFillColorAlpha(ROOT.kBlue, 0.3)
#h1.SetFillColorAlpha(ROOT.kGreen+2, 0.3)
#h2.SetFillColorAlpha(ROOT.kRed, 0.3)

#yAxis.SetRangeUser(0, 1.1*h.GetMaximum())
yAxis.SetRangeUser(0, 1.6*max(hMCme11.GetMaximum(), hme11_pre.GetMaximum(), hme11_post.GetMaximum() ))
yAxis.SetMaxDigits(3)

hMCme11.Draw("HIST")
hme11_pre.Draw("HIST SAME")
hme11_post.Draw("HIST SAME")

legend = ROOT.TLegend(0.6, 0.75, 0.9, 0.85)
legend.AddEntry(hme11_pre, f"Before alignment")
legend.AddEntry(hme11_post, f"After alignment")
legend.AddEntry(hMCme11, f"Ideal Geometry")
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
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-1.6*canvas.GetTopMargin(), "{low} GeV".format(low=low_pt)+" < p_{T}^{GLB} < "+"{high} GeV".format(high=high_pt)) 
latex.DrawLatex(0.65-0.5*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.6*canvas.GetTopMargin(), "{reg}Endcap Station 1 Layer {lay}".format(reg=reg_string, lay=layer))
latex.DrawLatex(0.65-0.5*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.9*canvas.GetTopMargin(), "{ch_string} chambers".format(ch_string=ch_string))
latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-1.9*canvas.GetTopMargin(), f"{mu_notation}")

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
canvas.SaveAs("{x_var}_1D_R{reg}L{lay}_{ch_string}chambers_{mu_str}.png".format(reg=endcap, ch_string=ch_string, lay=layer, x_var=x_var, mu_str=mu_str))
