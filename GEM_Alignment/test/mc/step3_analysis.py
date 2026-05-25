#!/usr/bin/env python3
import ROOT
from DataFormats.FWLite import Events, Handle
import math

file_path = "/afs/cern.ch/user/k/kkeshav/CMSSW_15_1_0/src/step3_RECO.root"
events = Events(file_path)

handle = Handle("edm::RangeMap<GEMDetId, edm::OwnVector<GEMRecHit> >")
label = ("gemRecHits", "GE21", "RECO")

h_eta = ROOT.TH1F("h_eta", "GE21 GEMRecHits eta; eta; Hits", 50, -3.0, 3.0)
h_phi = ROOT.TH1F("h_phi", "GE21 GEMRecHits phi; phi; Hits", 50, -3.5, 3.5)
h_r   = ROOT.TH1F("h_r", "GE21 GEMRecHits radius; r [cm]; Hits", 50, 0, 500)

for i, event in enumerate(events):
    event.getByLabel(label, handle)
    gem_map = handle.product()

    # Loop over all detids
    for detid in gem_map.keys():
        hits = gem_map[detid]  # hits is an edm::OwnVector<GEMRecHit>
        for hit in hits:        # now this works
            pos = hit.localPosition()
            h_eta.Fill(pos.eta())
            h_phi.Fill(pos.phi())
            r = math.sqrt(pos.x()**2 + pos.y()**2)
            h_r.Fill(r)

# Save plots
c_eta = ROOT.TCanvas("c_eta", "GE21 eta", 800, 600)
h_eta.Draw()
c_eta.SaveAs("GE21_eta.png")

c_phi = ROOT.TCanvas("c_phi", "GE21 phi", 800, 600)
h_phi.Draw()
c_phi.SaveAs("GE21_phi.png")

c_r = ROOT.TCanvas("c_r", "GE21 radius", 800, 600)
h_r.Draw()
c_r.SaveAs("GE21_r.png")

print("Plots saved: GE21_eta.png, GE21_phi.png, GE21_r.png")

