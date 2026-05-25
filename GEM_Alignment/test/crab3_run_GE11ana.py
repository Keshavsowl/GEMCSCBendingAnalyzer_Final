from CRABClient.UserUtilities import config
config = config()

#section General
config.General.requestName = 'Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_aligned_trackerprop' 
config.General.workArea = 'crabLogs'#working directory
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_GE11ana.py'
config.JobType.numCores = 1

misalign = True  #Make sure to change the run_GE11ana.py too!!!
if misalign:
  config.JobType.inputFiles =  ['./Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_trackerprop.db']

#section Data
config.Data.runRange = '392280-392700'
config.Data.inputDataset = '/Muon0/Run2025C-ZMu-PromptReco-v1/RAW-RECO'
# config.Data.userInputFiles = open('singleMuonGun_11_3_4_2021_design.list').readlines()
# config.Data.lumiMask = '/eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Muon.json'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/toakhter/tamu_mual/2025'
config.Data.publication = False

config.Data.outputDatasetTag = config.General.requestName
config.Site.storageSite = 'T3_CH_CERNBOX' #'T3_US_FNALLPC'
