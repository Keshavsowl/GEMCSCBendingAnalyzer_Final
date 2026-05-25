#!/usr/bin/env python3
import ROOT
from DataFormats.FWLite import Events, Handle

# Input file (STEP-3)
#file_path = "/afs/cern.ch/user/k/kkeshav/CMSSW_15_1_0/src/step3_phase2.root"
file_path = "/eos/user/k/kkeshav/SingleMuPt30to50_neg_end_step3/Phase2_RECO_neg_end3/260109_084949/0000/step3_RECO_1.root"

# Open the file
events = Events(file_path)

# Prepare handles for GE21 RecHits and Reco Muons
gemHandle = Handle("edm::RangeMap<GEMDetId,edm::OwnVector<GEMRecHit,edm::ClonePolicy<GEMRecHit> >,edm::ClonePolicy<GEMRecHit> >")
gemLabel = ("gemRecHits", "GE21", "RECO")

muonHandle = Handle("std::vector<reco::Muon>")
muonLabel = ("muons", "", "RECO")  # Standard reco muons

# Histograms
h_pt  = ROOT.TH1F("h_pt",  "Muon pT (with GE21 hits); pT [GeV]; Events", 50, 0, 100)
h_eta = ROOT.TH1F("h_eta", "Muon eta (with GE21 hits); eta; Events", 50, -3, 3)
h_phi = ROOT.TH1F("h_phi", "Muon phi (with GE21 hits); phi; Events", 50, -3.5, 3.5)

# Additional histograms
h_nGE21 = ROOT.TH1F("h_nGE21", "Number of GE21 hits per event; N_{GE21}; Events", 20, 0, 20)
h_nMuons = ROOT.TH1F("h_nMuons", "Number of muons per event; N_{muons}; Events", 10, 0, 10)
h_cls = ROOT.TH1F("h_cls", "GE21 RecHit cluster size; Cluster Size; Hits", 20, 0, 20)
h_bx = ROOT.TH1F("h_bx", "GE21 RecHit BX; BX; Hits", 11, -5, 6)
h_x = ROOT.TH1F("h_x", "GE21 RecHit x position; x [cm]; Hits", 100, -50, 50)

total_events = 0
events_with_ge21 = 0
events_with_muons = 0

# Loop over events
for i, event in enumerate(events):
    total_events += 1
    
    # Get GE21 RecHits
    event.getByLabel(gemLabel, gemHandle)
    gemRecHits = gemHandle.product()
    
    # Get Reco Muons
    event.getByLabel(muonLabel, muonHandle)
    muons = muonHandle.product()
    
    nGE21 = gemRecHits.size()
    nMuons = muons.size()
    
    h_nGE21.Fill(nGE21)
    h_nMuons.Fill(nMuons)
    
    if nGE21 > 0:
        events_with_ge21 += 1
        
        # Fill GE21 hit properties
        for hit in gemRecHits:
            h_cls.Fill(hit.clusterSize())
            h_bx.Fill(hit.BunchX())
            h_x.Fill(hit.localPosition().x())
    
    if nMuons > 0:
        events_with_muons += 1
    
    # If event has both GE21 hits and muons, plot muon properties
    if nGE21 > 0 and nMuons > 0:
        for muon in muons:
            # Check if muon is a good muon (optional quality cuts)
            if muon.pt() > 0:  # Basic cut, you can add more
                h_pt.Fill(muon.pt())
                h_eta.Fill(muon.eta())
                h_phi.Fill(muon.phi())
    
    if i % 100 == 0:
        print(f"Processed {i} events...")

print(f"\n=== Summary ===")
print(f"Total events: {total_events}")
print(f"Events with GE21 hits: {events_with_ge21}")
print(f"Events with muons: {events_with_muons}")

# Draw & save plots
ROOT.gStyle.SetOptStat(1111)

c_pt = ROOT.TCanvas("c_pt", "Muon pT", 800, 600)
h_pt.Draw()
c_pt.SaveAs("muon_with_GE21_pt.png")

c_eta = ROOT.TCanvas("c_eta", "Muon eta", 800, 600)
h_eta.Draw()
c_eta.SaveAs("muon_with_GE21_eta.png")

c_phi = ROOT.TCanvas("c_phi", "Muon phi", 800, 600)
h_phi.Draw()
c_phi.SaveAs("muon_with_GE21_phi.png")

c_nGE21 = ROOT.TCanvas("c_nGE21", "Number of GE21 hits", 800, 600)
h_nGE21.Draw()
c_nGE21.SaveAs("nGE21_hits.png")

c_nMuons = ROOT.TCanvas("c_nMuons", "Number of muons", 800, 600)
h_nMuons.Draw()
c_nMuons.SaveAs("nMuons.png")

c_cls = ROOT.TCanvas("c_cls", "GE21 cluster size", 800, 600)
h_cls.Draw()
c_cls.SaveAs("GE21_clusterSize.png")

c_bx = ROOT.TCanvas("c_bx", "GE21 BX", 800, 600)
h_bx.Draw()
c_bx.SaveAs("GE21_BX.png")

c_x = ROOT.TCanvas("c_x", "GE21 x position", 800, 600)
h_x.Draw()
c_x.SaveAs("GE21_x_position.png")

print("\nPlots saved!")