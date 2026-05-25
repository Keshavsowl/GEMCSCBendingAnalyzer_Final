import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh

#f = ROOT.TFile("{}".format(sys.argv[1]))
run = "2022G"
low_pt = 30
high_pt = 200

#txt_description = "dPhi=rechit local phi - prophit local phi [created in units of mRad]. dPhi corrected calculation takes the firmware long and short superchambers orientation into account on +/- endcaps, i.e.\n"+"        R+1    R-1\n"+"Even   -1       +1\n"+"Odd   +1       -1\n"+"Shift [strip(8)] is calculated by the following conversion rule: 0.37 [mRad] = 1 [strip(8)]\n"+"cuts: 30GeV<muon_pt<200GeV, has_fidcut, n_ME11_segment=1, |RdPhi_Corrected|<2cm, |dPhi_Corrected|<3mRad, has_TightID, endcap, station, superchamber, eta\n"+"[filename for TA's notekeeping]: ntuple: Run2022D_ZMu_PromptReco_RAWRECO_globalMu_pfisotight_idealGEMonCSC_v1.root]\n"+"=================================================================================================================\n"

f0 = ROOT.TFile("../Run362695_ZMu_PromptReco_RAWRECO_idealGEMidealCSC_v0.root")
f1 = ROOT.TFile("../Run2022G_ZMu_PromptReco_RAWRECO_idealGEMidealCSC_v0.root")
event0 = f0.Get("analyzer/ME11Seg_Prop")
event1 = f1.Get("analyzer/ME11Seg_Prop")
ROOT.gROOT.SetBatch(1)
tdrstyle.setTDRStyle()

nX_row = 9
nY_col = 4

H_ref = 800
W_ref = 800
W = W_ref# * nX_row
H = H_ref# * nY_col

T = 0.12*H
B = 0.16*H
L = 0.16*W
R = 0.08*W

xbins = 100
xlow = -4
xhigh = 4


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

def strip_conversion(phi): #0.37 [mRad] = 1 [strip(8)]
  strip = round(phi/0.37, 0)
  return strip

'''#below excerpt is for all plots on one canvas is needed
name_mark = ROOT.TText(0.89, 0.25, "Towsifa")
name_mark.SetTextSize(0.025)
name_mark.SetTextColor(ROOT.kViolet+1)
name_mark.Draw()
canvas.Divide(nX_row, nY_col)
'''
for reg in [-1, 1]:
  t = open("Run{run}/LUT_R{r}_st1.txt".format(run=run, r=reg), "w")
  t0 = open("Run{run}/2022G_LUT_R{r}_st1.txt".format(run=run, r=reg), "w")
  t1 = open("Run{run}/362695_LUT_R{r}_st1.txt".format(run=run, r=reg), "w")
  #t.writelines(txt_description)
  #t.writelines("Endcap | Station | Superchamber | eta | Shift [strip(8)] | SuperChamber dPhi mean [mRad] | Layer1 dPhi mean [mRad] | Layer2_dPhi_mean[mRad]\n")
  t.writelines("SuperchamberEta | 2022G Shift [strip(8)] | 362695 Shift [strip(8)] | Difference in Shift (i.e. 2022G-362695)\n")
  t0.writelines("SuperchamberEta | Shift [strip(8)]\n")
  t1.writelines("SuperchamberEta | Shift [strip(8)]\n")

  #t1= open("LookupTable_R{r}_3mRad.txt".format(r=reg), "w")
  #t1.writelines(txt_description)
  #t1.writelines("Endcap | Station | Superchamber | eta | Shift [strip(8)] | SuperChamber dPhi mean [mRad]\n")

  for st in [1]: #[1, 2] for both stations
    for ch in range(1, 37):
      h_index = -1
      h1_index = -1
      h2_index = -1
      h_list = []
      h1_list = []
      h2_list = []
      for eta in range(1, 9):
        h_index+=1
        h1_index+=1
        h2_index+=1
        if st==2:
          t.writelines("{ch}{e} {strip}\n".format(ch=ch, e=eta, strip=0))
          #t.writelines("{reg} {st} {ch} {e} {strip} {h} {h1} {h2}\n".format(reg=reg, st=st, ch=ch, e=eta, strip=0, h=0, h1=0, h2=0))
          #t1.writelines("{reg} {st} {ch} {e} {strip} {h}\n".format(reg=reg, st=st, ch=ch, e=eta, strip=0, h=0))
          continue
        
        #canvas.cd(ch)
        #ROOT.gPad.SetGridx()
        #ROOT.gPad.SetGridy()
        h_list.append(ROOT.TH1D("h_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), "h_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), xbins, xlow, xhigh))
        h1_list.append(ROOT.TH1D("h1_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), "h1_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), xbins, xlow, xhigh))
        h2_list.append(ROOT.TH1D("h2_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), "h2_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), xbins, xlow, xhigh))

        xAxis = h_list[h_index].GetXaxis()
        xAxis.SetTitleOffset(1)
        xAxis.SetTitleSize(0.05)
        xAxis.SetTitle("#Delta#phi [mRad]")
        #xAxis.CenterTitle()

        yAxis = h_list[h_index].GetYaxis()
        yAxis.SetTitleOffset(0)
        yAxis.SetTitleSize(0.05)
        #yAxis.SetTitle("A.U.")
        yAxis.SetTitle("Entries")
        #yAxis.CenterTitle()

        event0.Project("h_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), "1000*dPhi_Corrected", "abs(RdPhi_Corrected) < 2 && 1000*abs(dPhi_Corrected)<4 && n_ME11_segment == 1 && has_fidcut && muon_pt > {low} && muon_pt<{high} && has_TightID==1 && prop_location[0]=={reg} && prop_location[1]=={st} && prop_location[2]=={ch} && prop_location[4]=={e}".format(reg=reg, st=st, ch=ch, e=eta, low=low_pt, high=high_pt))
        event1.Project("h1_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), "1000*dPhi_Corrected", "abs(RdPhi_Corrected)< 2 && 1000*abs(dPhi_Corrected)<4 && n_ME11_segment == 1 && has_fidcut && muon_pt > {low} && muon_pt<{high} && has_TightID==1 && prop_location[0]=={reg} && prop_location[1]=={st} && prop_location[2]=={ch} && prop_location[4]=={e}".format(reg=reg, st=st, ch=ch, e=eta, low=low_pt, high=high_pt))

        #event.Project("h1_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta), "RdPhi_Corrected_mrad", "abs(RdPhi_Corrected) < 2 && abs(RdPhi_Corrected_mrad)<4 && n_ME11_segment == 1 && has_fidcut && muon_pt > {low} && muon_pt<{high} && has_TightID==1 && prop_location[0]=={reg} && prop_location[1]=={st} && prop_location[2]=={ch} && prop_location[3]==1 && prop_location[4]=={e}".format(reg=reg, st=st, ch=ch, e=eta, low=low_pt, high=high_pt))
        #event.Project("h2_{r}{st}{sc}eta{e}".format(r=reg, st=st, sc=ch, e=eta),"RdPhi_Corrected_mrad", "abs(RdPhi_Corrected) < 2 && abs(RdPhi_Corrected_mrad)<4 && n_ME11_segment == 1 && has_fidcut && muon_pt > {low} && muon_pt<{high} && has_TightID==1 && prop_location[0]=={reg} && prop_location[1]=={st} && prop_location[2]=={ch} && prop_location[3]==2 && prop_location[4]=={e}".format(reg=reg, st=st, ch=ch, e=eta, low=low_pt, high=high_pt))

        #h.Scale(1/h.Integral())
        #h1.Scale(1/h1.Integral())
        #h2.Scale(1/h2.Integral())

        h=h_list[h_index]
        h1=h1_list[h1_index]
        #h2=h2_list[h2_index]

        h.SetLineWidth(3)
        h1.SetLineWidth(2)
        #h2.SetLineWidth(2)

        h.SetLineStyle(1)
        h1.SetLineStyle(1)
        #h2.SetLineStyle(1)

        h.SetMarkerSize(0)
        h1.SetMarkerSize(0)
        #h2.SetMarkerSize(0)

        h.SetLineColor(ROOT.kBlack)
        h1.SetLineColor(ROOT.kBlue)
        #h2.SetLineColor(ROOT.kRed)

        yAxis.SetRangeUser(0, 1.1*max(h.GetMaximum(), h1.GetMaximum()))

        #h.Draw("hist")
        #h1.Draw("hist same")
        #h2.Draw("hist same")

        #rootkde = ROOT.TLegend(0.6,0.75,0.9,0.87)
        #rootkde.AddEntry(h, "SC {ch} mean: {mean}".format(ch=ch, mean=round(h.GetMean(), 3)))
        #rootkde.AddEntry(h1, "Layer 1 mean: {mean}".format(mean=round(h1.GetMean(), 3)))
        #rootkde.AddEntry(h2, "Layer 2 mean: {mean}".format(mean=round(h2.GetMean(), 3)))
        #rootkde.SetBorderSize(0)
        #rootkde.Draw()

        t.writelines("{ch}{e} {strip0} {strip1} {diff}\n".format(ch=ch, e=eta, strip0=round(strip_conversion(h.GetMean())), strip1=round(strip_conversion(h1.GetMean())), diff=round(strip_conversion(h.GetMean()))-round(strip_conversion(h1.GetMean())) ))
        t0.writelines("{ch}{e} {strip}\n".format(ch=ch, e=eta, strip=round(strip_conversion(h.GetMean())) ))
        t1.writelines("{ch}{e} {strip}\n".format(ch=ch, e=eta, strip=round(strip_conversion(h1.GetMean())) ))
        #t.writelines("{reg} {st} {ch} {e} {strip} {h} {h1} {h2}\n".format(reg=reg, st=st, ch=ch, e=eta, strip=strip_conversion(h.GetMean()), h=h.GetMean(), h1=h1.GetMean(), h2=h2.GetMean()))
        #t1.writelines("{reg} {st} {ch} {e} {strip} {h}\n".format(reg=reg, st=st, ch=ch, e=eta, strip=strip_conversion(h.GetMean()), h=round(h.GetMean(), 3)))
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(ROOT.kBlack)

        latex.SetTextFont(42)
        latex.SetTextSize(0.4*canvas.GetTopMargin())

        latex.SetTextAlign(32)
        #latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())))
        #latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.8*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
        #latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))
        latex.DrawLatex(1-1.1*canvas.GetRightMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "(13.6 TeV)")
        latex.SetTextAlign(12)
        latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.2*canvas.GetTopMargin(), "Run {run}".format(run=run))

        latex.SetTextSize(0.25*canvas.GetTopMargin())
        latex.DrawLatex(0+1.1*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.6*canvas.GetTopMargin(), "Region{reg}, Station{st}, SC{sc}, eta{e}".format(reg=reg, st=st, sc=ch, e=eta))
        #latex.DrawLatex(0+1.2*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Layer 2")
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
        #if os.path.exists("Run{y}/{ver}/LookupTable_byChamber_4mRad/R{r}/st{st}/SC{sc}".format(y=year, ver=version, r=reg, st=st, sc=ch)) == False:
        #  os.mkdir("Run{y}/{ver}/LookupTable_byChamber_4mRad/R{r}/st{st}/SC{sc}".format(y=year, ver=version, r=reg, st=st, sc=ch))
        #canvas.SaveAs("Run{y}/{ver}/LookupTable_byChamber_4mRad/R{r}/st{st}/SC{sc}/dPhi_R{r}_st{st}_SC{sc}_eta{e}.png".format(y=year, ver=version, e=eta, r=reg, st=st, sc=ch))

t.close()
t0.close()
t1.close()
