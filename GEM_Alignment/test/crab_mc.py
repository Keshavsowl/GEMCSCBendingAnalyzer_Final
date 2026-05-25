from CRABClient.UserUtilities import config
config = config()

#section general
config.General.requestName = '2025mc_v3'
config.General.workArea = 'crabLogs'  # working dir 
config.General.transferOutputs = True
config.General.transferLogs = True

#section JobType
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_GE21ana.py'
config.JobType.numCores = 1
config.JobType.maxMemoryMB = 2500  # Phase2 reconstruction needs more memory
config.JobType.allowUndistributedCMSSW = True  # Needed for Phase2

#section Data - Single specific file
#config.Data.userInputFiles = [
#    '/store/mc/Phase2Spring24DIGIRECOMiniAOD/DYTo2L_Bin-M-50_TuneCP5_14TeV_pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU140_Trk1GeV_140X_mcRun4_realistic_v5-v1/2810000/ffdecd4e-5d0f-45d7-9764-895db238294c.root'
#]
#config.Data.userInputFiles = ['/eos/user/k/kkeshav/SingleMuPt30to50/Phase2_RECO_v1/251222_014014/0000/step3_RECO_1.root']
#config.Data.userInputFiles = [
#    '/store/user/kkeshav/SingleMuPt30to50/Phase2_RECO_v1/251222_014014/0000/step3_RECO_1.root'
#]
#config.Data.userInputFiles = [
#    'root://eoscms.cern.ch//eos/cms/store/user/kkeshav/SingleMuPt30to50/Phase2_RECO_v1/251222_014014/0000/step3_RECO_1.root'
#]
config.Data.userInputFiles = [
    'root://eosuser.cern.ch//eos/user/k/kkeshav/SingleMuPt30to50_neg_end_step3/Phase2_RECO_neg_end3/260109_084949/0000/step3_RECO_1.root'
]

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1                    # 1 file per job (will create exactly 1 job)
config.Data.outLFNDirBase = '/store/user/kkeshav/tamu_mual/2025/mcfinal'
config.Data.publication = False                # Set to True if you want to publish
config.Data.outputDatasetTag = config.General.requestName

#config.Site.storageSite = 'T1_US_FNAL_Disk'
config.Site.storageSite = 'T3_CH_CERNBOX'
config.Site.whitelist = ['T2_CH_CERN']
