# GEMCSCBendingAnalyzer

## how to set up CMS Software environment and check out this alignment analyzer package

```
cmsrel CMSSW_15_0_1 
```
or if you want to name your work environment differently: 

```scram p -n Your_Choice_of_Name CMSSW_15_0_1```


```
cd CMSSW_15_0_1/src/
cmsenv
git cms-init

git clone https://github.com/akhter-towsifa/GEMCSCBendingAnalyzer.git -b 15_X_RawReco

scram b -j 8
```

## Residual Packages
Located under `GEM_Alignment`. To run the relevant alignment configuration files, access the `test` folder and set up proxy for the server if necessary: 
```
cd GEMCSCBendingAnalyzer/GEM_Alignment/test/
voms-proxy-init --valid 192:00 --voms cms #setting up the proxy
```
### GE1/1 Analyzer configuration
The associated code `analyzer.cc` is located in the `plugins` folder.
```
cmsRun run_GE11ana.py
```
### ME1/1 Analyzer (Legacy)
```
cmsRun run_ME11ana.py
```
### GE1/1 and ME1/1 Analyzer (Legacy)
```
cmsRun run_both_analyzers.py
```
## GEM DB Maker
The associated code `GEMAlDBWriter.cc` is located in the `plugins` folder
```
cd GEMCSCBendingAnalyzer/GEM_Alignment/test/
cmsRun GEMAlDBWriter_cfg.py
```
## GEM_fitter.cpp: package for creating alignment estimates
```
cd GEMCSCBendingAnalyzer/GEM_Alignment/script/standAloneGemAlignment
./run_3DOF_Fitter.sh
```
![alignment_cfg_flowchart](https://github.com/akhter-towsifa/GEMCSCBendingAnalyzer/assets/51368122/e4141fa9-64f3-4be7-b0d0-6a545466a1dd)



## Resources
The package is inherited from Jason Lee's MuonPerformance and it is used for GEM related analysis at TAMU group. The major target is to analyze GEM-CSC bending angle in real data from CMS.

The previous working version (extensively tested with cosmic data) can be found at https://github.com/aebid/GEMCSCBendingAnalyzer

GEM alignment draft TDR for reference: https://gitlab.cern.ch/tdr/notes/DN-24-012
