from CRABClient.UserUtilities import config
config = config()

# General settings
config.General.requestName = 'SingleMuPt30to50_GEN_SIM_v4'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

# Job type - PrivateMC for generation
config.JobType.pluginName = 'PrivateMC'      # FIXED
config.JobType.psetName = 'step1_GEN_SIM_cfg.py'
config.JobType.maxMemoryMB = 8000            # Increased slightly
config.JobType.numCores = 4
#config.JobType.maxJobRuntimeMin = 180        # FIXED: 3 hours

# Data settings
config.Data.outputPrimaryDataset = 'SingleMuPt25to70_2025_MC_v1'
config.Data.splitting = 'EventBased'         # FIXED
config.Data.unitsPerJob = 2000              # FIXED: events per job
config.Data.totalUnits = 1000000             # FIXED: total events (adjust as needed)
config.Data.outLFNDirBase = '/store/user/kkeshav/'
config.Data.publication = False
config.Data.outputDatasetTag = 'GEN_SIM_neg_muon'

# Site settings
config.Site.storageSite = 'T3_CH_CERNBOX'
