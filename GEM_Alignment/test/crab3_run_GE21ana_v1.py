from CRABClient.UserUtilities import config
config = config()

# ---------------------
# General settings
# ---------------------
config.General.requestName = 'GE21_Alignment_MC_2025_v4'
config.General.workArea = 'crabLogs'
config.General.transferOutputs = True
config.General.transferLogs = True

# ---------------------
# Job type
# ---------------------
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_GE21ana_v1.py'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000
#config.JobType.maxJobRuntimeMin = 180

# Misalignment (if needed)
misalign = False
if misalign:
    config.JobType.inputFiles = ['./filename.db']

# ---------------------
# Data settings - Your MC RECO files
# ---------------------
base_path = 'root://eosuser.cern.ch//eos/user/k/kkeshav/SingleMuPt30to50_2025_MC_v1/RECO_neg_muon/260131_203850/0000/'

config.Data.userInputFiles = [
    base_path + 'step3_2025_v1_1.root',
    base_path + 'step3_2025_v1_2.root',
    base_path + 'step3_2025_v1_3.root',
    base_path + 'step3_2025_v1_4.root',
    base_path + 'step3_2025_v1_5.root',
    base_path + 'step3_2025_v1_6.root',
    base_path + 'step3_2025_v1_7.root',
    base_path + 'step3_2025_v1_8.root',
    base_path + 'step3_2025_v1_9.root',
    base_path + 'step3_2025_v1_10.root',
    base_path + 'step3_2025_v1_11.root',
    base_path + 'step3_2025_v1_12.root',
    base_path + 'step3_2025_v1_13.root',
    base_path + 'step3_2025_v1_14.root',
    base_path + 'step3_2025_v1_15.root',
    base_path + 'step3_2025_v1_16.root',
    base_path + 'step3_2025_v1_17.root',
    base_path + 'step3_2025_v1_18.root',
    base_path + 'step3_2025_v1_19.root',
    base_path + 'step3_2025_v1_20.root',
    base_path + 'step3_2025_v1_21.root',
    base_path + 'step3_2025_v1_22.root',
    base_path + 'step3_2025_v1_23.root',
    base_path + 'step3_2025_v1_24.root',
    base_path + 'step3_2025_v1_25.root',
    base_path + 'step3_2025_v1_26.root',
    base_path + 'step3_2025_v1_27.root',
    base_path + 'step3_2025_v1_28.root',
    base_path + 'step3_2025_v1_29.root',
    base_path + 'step3_2025_v1_30.root',
    base_path + 'step3_2025_v1_31.root',
    base_path + 'step3_2025_v1_32.root',
    base_path + 'step3_2025_v1_33.root',
    base_path + 'step3_2025_v1_34.root',
    base_path + 'step3_2025_v1_35.root',
    base_path + 'step3_2025_v1_36.root',
    base_path + 'step3_2025_v1_37.root',
    base_path + 'step3_2025_v1_38.root',
    base_path + 'step3_2025_v1_39.root',
    base_path + 'step3_2025_v1_40.root',
    base_path + 'step3_2025_v1_41.root',
    base_path + 'step3_2025_v1_42.root',
    base_path + 'step3_2025_v1_43.root',
    base_path + 'step3_2025_v1_44.root',
    base_path + 'step3_2025_v1_45.root',
    base_path + 'step3_2025_v1_46.root',
    base_path + 'step3_2025_v1_47.root',
    base_path + 'step3_2025_v1_48.root',
    base_path + 'step3_2025_v1_49.root',
    base_path + 'step3_2025_v1_50.root',
]

config.Data.outputPrimaryDataset = 'SingleMuPt30to50_2025_MC_v1'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1              # Process 2 files per job
config.Data.totalUnits = 50              # Total 50 files
config.Data.outLFNDirBase = '/store/user/kkeshav/'
config.Data.publication = False
config.Data.outputDatasetTag = 'TBMA_MC_Neg_muon_v1'

# ---------------------
# Site settings
# ---------------------
config.Site.storageSite = 'T3_CH_CERNBOX'
config.Site.whitelist = ['T2_CH_CERN']

