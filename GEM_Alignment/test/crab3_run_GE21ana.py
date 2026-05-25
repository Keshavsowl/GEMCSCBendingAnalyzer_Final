#from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from CRABClient.UserUtilities import config
config = config()
#section general
config.General.requestName = 'Run2025C_muon0_v11' #Run2023D_muon0_alignedreco_v1
config.General.workArea = 'crabLogs'#working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_GE21ana.py'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000


misalign = True  #Make sure to change the run_GE21ana.py too!!!
if misalign:
  config.JobType.inputFiles =  ['./Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_v3.db']

#section Data
#config.Data.runRange = '348776,348773,349073'
config.Data.runRange = '392278-393087'
config.Data.inputDataset = '/Muon0/Run2025C-ZMu-PromptReco-v1/RAW-RECO'


#config.Data.outputPrimaryDataset = '/Muon0_Run2025D-ZMu-PromptReco-v1_RAW-RECO'


config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.Data.outLFNDirBase = '/store/group/alca_muonalign/kkeshav/'
config.Data.publication = False
config.Data.outputDatasetTag = 'Run2025C_muon0_after_alignment_iteration_2'

#config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.storageSite = 'T2_CH_CERN'
