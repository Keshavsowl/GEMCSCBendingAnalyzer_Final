#!/usr/bin/env python3
import ROOT
from DataFormats.FWLite import Events, Handle
import os
import glob
# Directory containing the files
#base_dir = "/eos/user/k/kkeshav/SingleMuPt30to50_2025_MC_v1/GEN_SIM_SingleMuPt30to50_2025_MC_v2/260120_011147/0000/"
#base_dir = "/eos/user/k/kkeshav/SingleMuPt30to50_2025_MC_v1/GEN_SIM_neg_muon/260131_014207/0000/"
base_dir = "/eos/user/k/kkeshav/SingleMuPt25to70_2025_MC_v1/GEN_SIM_neg_muon/260215_002236/0000/"

# Get all step1_*.root files except the merged one
all_files = glob.glob(os.path.join(base_dir, "step1_*.root"))
# Filter out merged file
file_list = [f for f in all_files if "merged" not in f]
# Sort files numerically
file_list.sort(key=lambda x: int(x.split("step1_")[-1].split(".root")[0]) if x.split("step1_")[-1].split(".root")[0].isdigit() else 0)
print(f"Found {len(file_list)} files to process")
print("Files to process:")
for f in file_list[:5]:  # Print first 5
    print(f"  {os.path.basename(f)}")
if len(file_list) > 5:
    print(f"  ... and {len(file_list)-5} more")
# Prepare the handle and label
handle = Handle("std::vector<reco::GenParticle>")
label = ("genParticles", "", "SIM")
# Histograms
h_pt  = ROOT.TH1F("h_pt",  "GenParticle pT; pT [GeV]; Events", 50, 0, 100)
h_eta = ROOT.TH1F("h_eta", "GenParticle eta; eta; Events", 50, -3, 3)
h_phi = ROOT.TH1F("h_phi", "GenParticle phi; phi; Events", 50, -3.5, 3.5)
# Counter for total events and particles
total_events = 0
total_muons = 0
# Loop over all files
for file_idx, file_path in enumerate(file_list):
    print(f"\nProcessing file {file_idx+1}/{len(file_list)}: {os.path.basename(file_path)}")
    
    try:
        # Open the file
        events = Events(file_path)
        
        file_events = 0
        file_muons = 0
        
        # Loop over events in this file
        for i, event in enumerate(events):
            try:
                event.getByLabel(label, handle)
                gen_particles = handle.product()
                
                file_events += 1
                
                for gp in gen_particles:
                    if gp.status() == 1 and abs(gp.pdgId()) == 13:
                        h_pt.Fill(gp.pt())
                        h_eta.Fill(gp.eta())
                        h_phi.Fill(gp.phi())
                        file_muons += 1
                        
            except Exception as e:
                print(f"  Warning: Error processing event {i} in {os.path.basename(file_path)}: {e}")
                continue
        
        print(f"  Events: {file_events}, Muons found: {file_muons}")
        total_events += file_events
        total_muons += file_muons
        
    except Exception as e:
        print(f"  ERROR: Could not process file {os.path.basename(file_path)}: {e}")
        continue
print("\n" + "="*60)
print("Summary:")
print("="*60)
print(f"Total files processed: {len(file_list)}")
print(f"Total events: {total_events}")
print(f"Total muons found: {total_muons}")
print(f"pT histogram entries: {h_pt.GetEntries()}")
print(f"eta histogram entries: {h_eta.GetEntries()}")
print(f"phi histogram entries: {h_phi.GetEntries()}")
print("="*60)
# Set up ROOT style - disable statistics box
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
# Draw & save pT plot
c_pt = ROOT.TCanvas("c_pt", "GenParticle pT", 800, 600)
c_pt.SetLeftMargin(0.12)
c_pt.SetBottomMargin(0.12)
h_pt.SetLineColor(ROOT.kBlue)
h_pt.SetLineWidth(2)
h_pt.GetXaxis().SetTitleSize(0.045)
h_pt.GetYaxis().SetTitleSize(0.045)
h_pt.Draw()
# Removed latex text
c_pt.SaveAs("genParticle_pt_all.png")
print("\nSaved: genParticle_pt_all.png")
# Draw & save eta plot
c_eta = ROOT.TCanvas("c_eta", "GenParticle eta", 800, 600)
c_eta.SetLeftMargin(0.12)
c_eta.SetBottomMargin(0.12)
h_eta.SetLineColor(ROOT.kBlue)
h_eta.SetLineWidth(2)
h_eta.GetXaxis().SetTitleSize(0.045)
h_eta.GetYaxis().SetTitleSize(0.045)
h_eta.Draw()
# Removed latex text
c_eta.SaveAs("genParticle_eta_all.png")
print("Saved: genParticle_eta_all.png")
# Draw & save phi plot
c_phi = ROOT.TCanvas("c_phi", "GenParticle phi", 800, 600)
c_phi.SetLeftMargin(0.12)
c_phi.SetBottomMargin(0.12)
h_phi.SetLineColor(ROOT.kBlue)
h_phi.SetLineWidth(2)
h_phi.GetXaxis().SetTitleSize(0.045)
h_phi.GetYaxis().SetTitleSize(0.045)
h_phi.Draw()
# Removed latex text
c_phi.SaveAs("genParticle_phi_all.png")
print("Saved: genParticle_phi_all.png")
print("\nDone!")