import ROOT
from DataFormats.FWLite import Events, Handle

file_path = "/eos/user/k/kkeshav/SingleMuPt30to50_neg_end_step3/Phase2_RECO_neg_end3/260109_084949/0000/step3_RECO_1.root"
events = Events(file_path)

handle = Handle("edm::RangeMap<GEMDetId,edm::OwnVector<GEMRecHit,edm::ClonePolicy<GEMRecHit> >,edm::ClonePolicy<GEMRecHit> >")
label = ("gemRecHits", "GE21", "RECO")

total_ge21_hits = 0
chambers_with_hits = {}

for i, event in enumerate(events):
    event.getByLabel(label, handle)
    gemRecHits = handle.product()
    
    if gemRecHits.size() > 0:
        print(f"Event {i}: {gemRecHits.size()} GE21 hits")
        
        for hit in gemRecHits:
            total_ge21_hits += 1
            detid = hit.gemId()
            chamber_id = (detid.region(), detid.station(), detid.chamber(), detid.layer(), detid.roll())
            
            if chamber_id not in chambers_with_hits:
                chambers_with_hits[chamber_id] = 0
            chambers_with_hits[chamber_id] += 1
            
            if i == 0:
                print(f"  Hit: region={detid.region()}, station={detid.station()}, "
                      f"chamber={detid.chamber()}, layer={detid.layer()}, roll={detid.roll()}")
    
    if i >= 100:
        break

print(f"\nTotal GE21 hits: {total_ge21_hits}")
print(f"\nChambers with hits:")
for chamber, count in sorted(chambers_with_hits.items()):
    print(f"  Region={chamber[0]}, Station={chamber[1]}, Chamber={chamber[2]}, "
          f"Layer={chamber[3]}, Roll={chamber[4]}: {count} hits")
