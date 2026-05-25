from CRABClient.UserUtilities import config
config = config()

# General settings
config.General.requestName = 'SingleMuPt25to70_DIGI_v4'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

# Job type - Analysis for processing existing files
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'step2_DIGI_cfg.py'
config.JobType.maxMemoryMB = 8000
config.JobType.numCores = 4
#config.JobType.maxJobRuntimeMin = 120

# Data settings - All 500 Step1 files
base_path = 'root://eosuser.cern.ch//eos/user/k/kkeshav/SingleMuPt25to70_2025_MC_v1/GEN_SIM_neg_muon/260215_002236/0000/'

# Generate list of 500 files
config.Data.userInputFiles = [base_path + f'step1_{i}.root' for i in range(1, 501)]

config.Data.outputPrimaryDataset = 'SingleMuPt25to70_2025_MC_v1'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2           # Process 2 files per job (250 jobs total)
config.Data.totalUnits = 500          # Total 500 input files
config.Data.outLFNDirBase = '/store/group/alca_muonalign/kkeshav'
config.Data.publication = False
config.Data.outputDatasetTag = 'DIGI_RAW_neg_muon'

# Site settings
config.Site.storageSite = 'T2_CH_CERN'
config.Site.whitelist = ['T2_CH_CERN']
