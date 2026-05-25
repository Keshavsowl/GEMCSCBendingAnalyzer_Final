from CRABClient.UserUtilities import config
config = config()
  
# ---------------------
# General settings
# ---------------------
config.General.requestName = 'SingleMuPt25to70_RECO_v1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True
  
# ---------------------
# Job type
# ---------------------
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step3_RECO_cfg.py'
config.JobType.maxMemoryMB = 8000
config.JobType.numCores = 4
  
# ---------------------
# Data settings - Using all step2 files from step2 job
# ---------------------
base_path = 'root://eoscms.cern.ch//eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_MC_v1/DIGI_RAW_neg_muon/260221_210857/0000/'
  
# Generate list of step2 files (we'll process all available files)
# Since you have 249 files currently, we'll set up for 250 (after resubmit)
config.Data.userInputFiles = [base_path + f'step2_{i}.root' for i in range(1, 251)]
  
config.Data.outputPrimaryDataset = 'SingleMuPt25to70_2025_MC_v1'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1              # 1 file per job for fastest processing
config.Data.totalUnits = 250             # Total 250 step2 files
config.Data.outLFNDirBase = '/store/group/alca_muonalign/kkeshav/'
config.Data.publication = False
config.Data.outputDatasetTag = 'RECO_neg_muon'
  
# ---------------------
# Site settings
# ---------------------
config.Site.storageSite = 'T2_CH_CERN'
config.Site.whitelist = ['T2_CH_CERN']
