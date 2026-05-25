from CRABClient.UserUtilities import config
config = config()
  
# ---------------------
# General settings
# ---------------------
config.General.requestName = 'SingleMuPt25to70_Alignment_v214'
config.General.workArea = 'crabLogs'
config.General.transferOutputs = True
config.General.transferLogs = True
  
# ---------------------
# Job type
# ---------------------
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_GE21ana_v4.py'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000
  
# Misalignment (if needed)
misalign = True
if misalign:
    config.JobType.inputFiles = ['./Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_v3.db']
  
# ---------------------
# Data settings - Your step3 RECO files from Pt25to70
# ---------------------
#base_path = 'root://eoscms.cern.ch//eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_MC_v1/RECO_neg_muon/260221_214448/0000/'
base_path = 'root://eoscms.cern.ch//eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_MC_v1/RECO_neg_muon/260221_224551/0000/'  
# Generate list of all 250 step3 files automatically
config.Data.userInputFiles = [base_path + f'step3_2025_v1_{i}.root' for i in range(1, 251)]
  
config.Data.outputPrimaryDataset = 'SingleMuPt25to70_2025_phi_X_0point001r_csc_v1'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1              # Process 1 file per job (250 jobs)
config.Data.totalUnits = 250             # Total 250 files
config.Data.outLFNDirBase = '/store/group/alca_muonalign/kkeshav/'
config.Data.publication = False
config.Data.outputDatasetTag = 'TBMA_MC_Neg_muon_Pt25to70_csc_v1'
  
# ---------------------
# Site settings - CORRECTED
# ---------------------
config.Site.storageSite = 'T2_CH_CERN'      # Fixed from T3_CH_CERNBOX
config.Site.whitelist = ['T2_CH_CERN']
