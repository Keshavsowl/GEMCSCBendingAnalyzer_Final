import FWCore.ParameterSet.Config as cms

process = cms.Process("GEMLocalRECO")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1))

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True),
                                     TryToContinue = cms.untracked.vstring('ProductNotFound')
                                     )  

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load("Configuration.StandardSequences.GeometryDB_cff")
# process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('RecoLocalMuon.GEMRecHit.gemRecHits_cfi')
#process.load('RecoLocalMuon.GEMRecHit.me0RecHits_cfi')
process.load('RecoLocalMuon.GEMRecHit.me0LocalReco_cff')
process.load('Geometry.GEMGeometryBuilder.gemGeometryDB_cfi')

### Try to do RecoLocalMuon on all muon detectors ###
#####################################################
from RecoLocalMuon.Configuration.RecoLocalMuon_cff import *
process.localreco = cms.Sequence(muonlocalreco)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_Prompt_v1', '')

# Skip Digi2Raw and Raw2Digi steps for Al Muon detectors #
##########################################################
process.gemRecHits.gemDigiLabel = cms.InputTag('muonGEMDigis', 'GEMDigi')
#process.rpcRecHits.rpcDigiLabel = cms.InputTag('muonRPCDigis')
process.csc2DRecHits.wireDigiTag = cms.InputTag("muonCSCDigis","MuonCSCWireDigi")
process.csc2DRecHits.stripDigiTag = cms.InputTag("muonCSCDigis","MuonCSCStripDigi")
#process.dt1DRecHits.dtDigiLabel = cms.InputTag('muonDTDigis')
#process.dt1DCosmicRecHits.dtDigiLabel = cms.InputTag('muonDTDigis')

# Explicit configuration of CSC for postls1 = run2 #
####################################################

process.gemRecHits = cms.EDProducer("GEMRecHitProducer",
    recAlgoConfig = cms.PSet(),
    recAlgo = cms.string('GEMRecHitStandardAlgo'),
    gemDigiLabel = cms.InputTag("muonGEMDigis"),
    ge21Off = cms.bool(False),
    # maskSource = cms.string('File'),
    # maskvecfile = cms.FileInPath('RecoLocalMuon/GEMRecHit/data/GEMMaskVec.dat'),
    # deadSource = cms.string('File'),
    # deadvecfile = cms.FileInPath('RecoLocalMuon/GEMRecHit/data/GEMDeadVec.dat')
)

### Input and Output Files
##########################
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'root://cms-xrd-global.cern.ch//store/data/Run2025C/Muon0/RAW-RECO/ZMu-PromptReco-v1/000/392/301/00000/04bb4908-87cd-4f6c-ae36-d7c2830bdd3f.root'
    )
)

process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string( 
        'file:/eos/user/t/toakhter/tamu_mual/2025/2025C/out_local_reco_test.root'
    ),
    outputCommands = cms.untracked.vstring( #'type_module_label_process'
        'drop *',
        'keep *Track*_*_*_RECO',
        'keep *TrackExtra*_globalMuons_*_RECO',
        'keep *TrackingRecHit*_*_*_*',
        'keep  *_*gemRecHits*_*_*',
        'keep *_*cscSegment*_*_*',
        'keep *_*csc2DRecHits*_*_*',
        # 'keep *_*muonGEMDigis*_*_*',
        # 'keep *_*muonCSCDigis*_*_*',
        'keep *_*muons*_*_*',
        'keep *_*offlinePrimaryVertices*_*_*',
        'drop *GsfTrack*_*_*_*',
        'drop *_*_*muPF*_*',
        'drop *_*_*muid*_*',
        'drop *_*tevMuons*_*_*',
        'drop *_*uncleanedOnlyCkfInOutTracksFromConversions*_*_*',
        'drop *_*pfImpactParameterTagInfos*_*_*',
        'drop *_*ckfInOutTracksFromConversions*_*_*'
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('rechit_step')
    )
)

### Paths and Schedules
#######################
# process.rechit_step  = cms.Path(process.localreco+process.gemRecHits+process.me0LocalReco)
#process.rechit_step  = cms.Path(process.localreco+process.gemRecHits+process.me0RecHits)
process.rechit_step  = cms.Path(process.gemRecHits)
process.endjob_step  = cms.Path(process.endOfProcess)
process.out_step     = cms.EndPath(process.output)


process.schedule = cms.Schedule(
    process.rechit_step,
    process.endjob_step,
    process.out_step
)

