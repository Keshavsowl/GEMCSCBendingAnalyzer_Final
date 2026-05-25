import ROOT, tdrstyle, sys, os, array

# ARGUMENTS ************ file, shift (-.1cm), direction (X), Zlow, Zhigh

f = ROOT.TFile("{}".format(sys.argv[1]))
proplist = ["ME11Seg_Prop", "CSC_Prop"]
for prop in proplist:
  for layer in [1, 2]:
    for region in [-1, 1]:
      event = f.Get("analyzer/"+prop)
      ROOT.gROOT.SetBatch(1)
      tdrstyle.setTDRStyle()

      H_ref = 600
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
      xhigh = 40
      ylow = -300
      yhigh = 300

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

      h = ROOT.TEfficiency("h", "h;Chamber;Efficiency", xbins, xlow, xhigh)
      h_1 = ROOT.TH1D("h_1", "h_1", xbins, xlow, xhigh)
      h_2 = ROOT.TH1D("h_2", "h_2", xbins, xlow, xhigh)
      """
      ablue = array.array("d", [1,1,0])
      ared = array.array("d", [0,1,1])
      agreen = array.array("d", [0,1,0])
      astop = array.array("d", [0,.5,1])
      myPalette = []
      fi = ROOT.TColor.CreateGradientColorTable(3, astop, ared, agreen, ablue, 100)
      for x in range(100):
        myPalette.append(fi+x)
      ROOT.gStyle.SetPalette(100, array.array("i", myPalette))
      """

      xAxis = h_1.GetXaxis()
      xAxis.SetTitle("Chamber")
      #xAxis.CenterTitle()

      yAxis = h_1.GetYaxis()
      yAxis.SetTitleOffset(0)
      yAxis.SetTitle("Efficiency")
      #yAxis.CenterTitle()

      #zAxis = h.GetZaxis()
      #zAxis.SetTitle("Entries")
      #zAxis.CenterTitle()
      #zAxis.SetTitleOffset(.8)
      #zAxis.SetRangeUser(zlow, zhigh)

      event.Project("h_1", "prop_location[2]", "has_prop && prop_location[4] < 10 && n_ME11_segment == 1 && prop_location[0] == {region} && prop_location[3] == {layer} && has_fidcut && muon_pt > 3 && (runNum == 346307 || runNum == 346396 || runNum == 346490)".format(layer = layer, region = region))
      event.Project("h_2", "prop_location[2]", "has_rechit && abs(RdPhi) < 5 && has_prop && prop_location[4] < 10 && n_ME11_segment == 1 && prop_location[0] == {region} && prop_location[3] == {layer} && has_fidcut && muon_pt > 3 && (runNum == 346307 || runNum == 346396 || runNum == 346490)".format(region = region, layer = layer))
      h.SetPassedHistogram(h_2, "F")
      h.SetTotalHistogram(h_1, "F")

      for i in range(0, h_1.GetNbinsX()):
        if h_1.GetBinContent(i) != 0:
          print("total = ", h_1.GetBinContent(i))
        if h_2.GetBinContent(i) != 0:
          print("passed = ", h_2.GetBinContent(i))


      h.SetLineWidth(3)
      h.Draw()
      canvas.Update()
      tmpgraph = h.GetPaintedGraph()
      tmpgraph.SetMinimum(0)
      tmpgraph.SetMaximum(1)
      #h.Draw("colz")

      latex = ROOT.TLatex()
      latex.SetNDC()
      latex.SetTextAngle(0)
      latex.SetTextColor(ROOT.kBlack)

      latex.SetTextFont(42)
      #latex.SetTextAlign(31)
      latex.SetTextSize(0.4*canvas.GetTopMargin())
      #latex.DrawLatex(1-1.2*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = h.GetEntries()))
      #latex.DrawLatex(1-1.2*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.6*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
      #latex.DrawLatex(1-1.2*canvas.GetRightMargin(), 1-canvas.GetTopMargin()-0.9*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))

      #latex.DrawLatex(0+4.4*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.3*canvas.GetTopMargin(), "Entries: {entries}".format(entries = int(h.GetEntries())))
      #latex.DrawLatex(0+4.4*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-0.7*canvas.GetTopMargin(), "Mean: {mean}".format(mean = round(h.GetMean(),3)))
      #latex.DrawLatex(0+4.4*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()-1.1*canvas.GetTopMargin(), "Std Dev: {stddev}".format(stddev = round(h.GetStdDev(),3)))


      latex.SetTextSize(0.6*canvas.GetTopMargin())
      latex.SetTextFont(61)
      latex.DrawLatex(canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "CMS")
      latex.SetTextFont(52)
      latex.SetTextSize(0.5*canvas.GetTopMargin())
      #latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Preliminary")
      latex.DrawLatex(1.9*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "Work in Progress")
      latex.SetTextSize(0.3*canvas.GetTopMargin())
      latex.DrawLatex(4*canvas.GetLeftMargin(), 1-canvas.GetTopMargin()+0.2*canvas.GetTopMargin(), "{prop}, R{region} L{layer}".format(prop = prop, region = region, layer = layer))

      latex.SetTextFont(42)
      latex.SetTextSize(0.5*canvas.GetTopMargin())
      #latex.DrawLatex(4*canvas.GetLeftMargin(), 2*canvas.GetBottomMargin(), "{} {} Shift".format(sys.argv[3], sys.argv[2]))

      frame = canvas.GetFrame()
      frame.Draw()

      if os.path.exists("plots/") == False:
        os.mkdir("plots/")
      if os.path.exists("plots/effi") == False:
        os.mkdir("plots/effi")
      canvas.SaveAs("plots/effi/"+prop+"_R{region}L{layer}_fidcut.png".format(region = region, layer = layer))



      c1 = ROOT.TCanvas("", "", 1200, 800)
      h_1.SetMarkerColor(ROOT.kBlue)
      h_2.SetMarkerColor(ROOT.kRed)
      h_1.SetMarkerSize(2)
      h_2.SetMarkerSize(2)
      h_1.SetStats(0)
      h_1.GetYaxis().SetRangeUser(0, 1.4*max(h_2.GetMaximum(), h_1.GetMaximum()))
      h_1.Draw("p")
      h_2.Draw("p same")
      legend = ROOT.TLegend(0.8, 0.8, 1.0, 0.9)
      legend.AddEntry(h_1, "All Props")
      legend.AddEntry(h_2, "Matched Props")
      legend.Draw("same")
      c1.SaveAs("plots/effi/"+prop+"_R{region}L{layer}_hist_fidcut.png".format(region = region, layer = layer))
