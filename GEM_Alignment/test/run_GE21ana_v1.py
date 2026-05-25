import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('analyzer',Run3)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
#process.load('Configuration.StandardSequences.MagneticField_0T_cff') #0T for cruzet runs
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
#process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
# process.load('TrackingTools.TrackRefitter.globalMuonTrajectories_cff')
process.load('RecoMuon.GlobalMuonProducer.globalMuons_cfi')
process.load('TrackingTools.TrackFitters.TrackFitters_cff')
process.load('Geometry.GEMGeometryBuilder.gemGeometryDB_cfi')
process.load('Configuration.StandardSequences.Digi_cff')


from Configuration.AlCa.GlobalTag import GlobalTag

### This is the misalignment part
misalign = True
do_GEM = True
do_CSC = True

if misalign:
  #db_file = 'sqlite_file:dummy_dx1.db'
  gem_db_file = 'sqlite_file:Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_v2.db' #for GEM
  # csc_db_file = 'sqlite_file:csc.db' #for csc alignment only in this case
  # gpr_db_file = 'sqlite_file:gpr.db' #for gpr only in this case
  process.GlobalTag.toGet = cms.VPSet(
    #GE11 rec/tag
     cms.PSet(
         connect = cms.string(gem_db_file),
         record = cms.string('GEMAlignmentRcd'),
         tag = cms.string('GEMAlignmentRcd')
     ),
     cms.PSet(
         connect = cms.string(gem_db_file),
         record = cms.string('GEMAlignmentErrorExtendedRcd'),
         tag = cms.string('GEMAlignmentErrorExtendedRcd')
     )
    #ME11 rec/tag
    # cms.PSet(
    #     connect = cms.string(csc_db_file),
    #     record = cms.string('CSCAlignmentRcd'),
    #     tag = cms.string('CSCAlignmentRcd')
    # ),
    # cms.PSet(
    #     connect = cms.string(csc_db_file),
    #     record = cms.string('CSCAlignmentErrorExtendedRcd'),
    #     tag = cms.string('CSCAlignmentErrorExtendedRcd')
    # ),
    # cms.PSet(
    #     connect = cms.string(gpr_db_file), 
    #     record = cms.string('GlobalPositionRcd'), 
    #     tag = cms.string('GlobalPositionRcd') #cms.string('IdealGeometry')
    # )
  )

process.GEMGeometryESModule.applyAlignment = cms.bool(do_GEM)
process.CSCGeometryESModule.applyAlignment = cms.bool(do_CSC)
################################


#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data_prompt', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2025_realistic', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_Prompt_v1', '')

process.MessageLogger.cerr.FwkReport.reportEvery = 5000

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register ('nEvents',
			-1, #Max number of events 
			VarParsing.multiplicity.singleton, 
			VarParsing.varType.int, 
			"Number of events")
options.parseArguments()

# process.maxEvents = cms.untracked.PSet(
#   input = cms.untracked.int32(options.nEvents)
# )
process.maxEvents.input = cms.untracked.int32(-1)


process.source = cms.Source("PoolSource", 
			fileNames = cms.untracked.vstring(options.inputFiles), 
			inputCommands = cms.untracked.vstring(
			  "keep *",
        'keep *_*muonGEMDigis*_*_*',
        'keep *_gemRecHits_*_*',
			  "drop TotemTimingDigiedmDetSetVector_totemTimingRawToDigi_TotemTiming_reRECO", 
			  "drop TotemTimingRecHitedmDetSetVector_totemTimingRecHits__reRECO"
			)
      # SelectEvents = cms.untracked.PSet(
      #   SelectEvents = cms.vstring('rechit_step')
      # )
		)

#testfile = "/eos/cms/store/group/alca_muonalign/singleMuonGun_11_3_4_2021_design/singleMuonGun_pT_20_200_CMSSW_11_3_4_GT_2021_design/crab_singleMuonGun_11_3_4_2021_design_RAW2DIGI_RECO_v3/210816_170519/0000/step2_83.root"
#process.source.fileNames.append('file:'+testfile)
outfile = "output_test_phase2.root"

#process.source.fileNames.append('root://cms-xrd-global.cern.ch/')
#process.source.fileNames.append('root://cms-xrd-global.cern.ch//store/data/Run2025C/Muon0/RAW-RECO/ZMu-PromptReco-v1/000/392/301/00000/04bb4908-87cd-4f6c-ae36-d7c2830bdd3f.root')
#process.source.fileNames.append('file:/eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_MC_v1/RECO_neg_muon/260221_224551/0000/step3_2025_v1_25.root')
#process.source.fileNames.append('file:/eos/user/k/kkeshav/SingleMuPt30to50_neg_end_step3/Phase2_RECO_neg_end3/260109_084949/0000/step3_RECO_1.root')
#process.source.fileNames.append('file:/afs/cern.ch/user/k/kkeshav/CMSSW_15_1_0/src/step3_2025_v1.root')
#process.source.fileNames.append('file:/afs/cern.ch/user/k/kkeshav/CMSSW_15_1_0/src/step3_phase2.root')  # <<< CHANGED: Your Phase2 file
process.source.fileNames.append('root://cms-xrd-global.cern.ch//store/data/Run2025C/Muon0/RAW-RECO/ZMu-PromptReco-v1/000/392/301/00000/04bb4908-87cd-4f6c-ae36-d7c2830bdd3f.root')

process.options = cms.untracked.PSet(
                        TryToContinue = cms.untracked.vstring('ProductNotFound') #SkipEvent parameter does not work for CMSSW_13_3_X and above
                        )

process.options = cms.untracked.PSet(
    numberOfThreads = cms.untracked.uint32(4),  # ← 4 threads
    numberOfStreams = cms.untracked.uint32(0),
    TryToContinue = cms.untracked.vstring('ProductNotFound')
)


process.TFileService = cms.Service("TFileService", fileName = cms.string(outfile)) 

from RecoLocalMuon.CSCSegment.cscSegments_cfi import *
process.cscSegments = cscSegments.clone()

process.load('RecoLocalMuon.GEMRecHit.gemRecHits_cfi')
#process.gemRecHits = cms.EDProducer("GEMRecHitProducer",
#    recAlgoConfig = cms.PSet(),
#    recAlgo = cms.string('GEMRecHitStandardAlgo'),
#    gemDigiLabel = cms.InputTag("muonGEMDigis"),
#    ge21Off = cms.bool(False),
#)

process.analyzer = cms.EDAnalyzer('ge21analyzer', 
          process.MuonServiceProxy,
        cscSegmentsReco = cms.InputTag("cscSegments"),
       gemRecHits = cms.InputTag("gemRecHits"),
#          gemRecHits = cms.InputTag("gemRecHits", "GE21", "RECO"),  # <<< CHANGED: Added "GE21" instance name and "RECO" process
#                    gemRecHits = cms.InputTag("gemRecHits", "RECO"),  # <<< CHANGED: Added "GE21" instance name and "RECO" process

          gemSimHits = cms.InputTag("g4SimHits", "MuonGEMHits"), 
        muons = cms.InputTag("muons"),
          vertexCollection = cms.InputTag("offlinePrimaryVertices"),
        tracker_prop = cms.bool(True),
        CSC_prop = cms.bool(False),
        Segment_prop = cms.bool(True),
        trackerRefit_prop = cms.bool(False),
        SegmentReco_prop = cms.bool(False),
        debug = cms.bool(True),
        isCosmic = cms.bool(False)
)

process.p = cms.Path(process.analyzer)  # <<< CHANGED: Removed gemRecHits producer from path
