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
# process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('RecoMuon.GlobalMuonProducer.globalMuons_cfi')
process.load('TrackingTools.TrackFitters.TrackFitters_cff')
process.load('Geometry.GEMGeometryBuilder.gemGeometryDB_cfi')
process.load('Configuration.StandardSequences.Digi_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

### Alignment flags
misalign = True
do_GEM   = False
do_CSC   = True  # Set to True only if you also provide a CSC db file below

# ── 1. Initialize GlobalTag FIRST ──────────────────────────────────────────
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2025_realistic', '')

# ── 2. Append custom alignment payloads on top ──────────────────────────────
if misalign:
    #gem_db_file = 'sqlite_file:Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_v3.db'
    csc_db_file = 'sqlite_file:Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_v3.db'
    # gpr_db_file = 'sqlite_file:gpr.db'

    process.GlobalTag.toGet = cms.VPSet(
        # GE11 alignment
        #cms.PSet(
        #    connect = cms.string(gem_db_file),
        #    record  = cms.string('GEMAlignmentRcd'),
        #    tag     = cms.string('GEMAlignmentRcd')
        #),
        #cms.PSet(
        #    connect = cms.string(gem_db_file),
        #    record  = cms.string('GEMAlignmentErrorExtendedRcd'),
        #    tag     = cms.string('GEMAlignmentErrorExtendedRcd')
        #),
        # Uncomment below if using CSC alignment
         cms.PSet(
             connect = cms.string(csc_db_file),
             record  = cms.string('CSCAlignmentRcd'),
             tag     = cms.string('CSCAlignmentRcd')
         ),
         cms.PSet(
             connect = cms.string(csc_db_file),
             record  = cms.string('CSCAlignmentErrorExtendedRcd'),
             tag     = cms.string('CSCAlignmentErrorExtendedRcd')
         ),
        # cms.PSet(
        #     connect = cms.string(gpr_db_file),
        #     record  = cms.string('GlobalPositionRcd'),
        #     tag     = cms.string('GlobalPositionRcd')
        # ),
    )

# ── 3. Apply alignment flags to geometry modules ────────────────────────────
process.GEMGeometryESModule.applyAlignment = cms.bool(do_GEM)
process.CSCGeometryESModule.applyAlignment = cms.bool(do_CSC)
############################################################################


process.MessageLogger.cerr.FwkReport.reportEvery = 5000

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.register('nEvents',
            -1,
            VarParsing.multiplicity.singleton,
            VarParsing.varType.int,
            "Number of events")
options.parseArguments()

process.maxEvents.input = cms.untracked.int32(-1)

process.source = cms.Source("PoolSource",
            fileNames = cms.untracked.vstring(options.inputFiles),
            inputCommands = cms.untracked.vstring(
                "keep *",
                'keep *_*muonGEMDigis*_*_*',
                "drop TotemTimingDigiedmDetSetVector_totemTimingRawToDigi_TotemTiming_reRECO",
                "drop TotemTimingRecHitedmDetSetVector_totemTimingRecHits__reRECO"
            )
        )

outfile = "output_test.root"

#process.source.fileNames.append('root://cms-xrd-global.cern.ch//store/data/Run2025C/Muon0/RAW-RECO/ZMu-PromptReco-v1/000/392/301/00000/04bb4908-87cd-4f6c-ae36-d7c2830bdd3f.root')
#process.source.fileNames.append('root://cms-xrd-global.cern.ch//store/data/Run2025C/Muon1/RAW-RECO/ZMu-PromptReco-v1/000/393/087/00000/5073ffca-f70d-49b4-9509-f1bc4e0fd0fb.root')
process.source.fileNames.append('file:/eos/cms/store/group/alca_muonalign/kkeshav/SingleMuPt25to70_2025_MC_v1/RECO_neg_muon/260221_224551/0000/step3_2025_v1_25.root')

# process.source.fileNames.append('root://cms-xrd-global.cern.ch//store/data/Run2025D/Muon0/RAW-RECO/ZMu-PromptReco-v1/000/394/637/00000/ee69153e-ff93-47a3-ba0a-75604725d4b3.root')

process.options = cms.untracked.PSet(
    numberOfThreads = cms.untracked.uint32(4),
    numberOfStreams = cms.untracked.uint32(0),
    TryToContinue  = cms.untracked.vstring('ProductNotFound')
)

process.TFileService = cms.Service("TFileService", fileName = cms.string(outfile))

from RecoLocalMuon.CSCSegment.cscSegments_cfi import *
process.cscSegments = cscSegments.clone()

process.load('RecoLocalMuon.GEMRecHit.gemRecHits_cfi')
process.gemRecHits = cms.EDProducer("GEMRecHitProducer",
    recAlgoConfig = cms.PSet(),
    recAlgo       = cms.string('GEMRecHitStandardAlgo'),
    gemDigiLabel  = cms.InputTag("muonGEMDigis"),
    ge21Off       = cms.bool(False),
)

process.analyzer = cms.EDAnalyzer('ge21analyzer',
        process.MuonServiceProxy,
        cscSegmentsReco      = cms.InputTag("cscSegments"),
        gemRecHits           = cms.InputTag("gemRecHits"),
        # gemRecHits           = cms.InputTag("gemRecHits", "GE21", "RECO"),
        # gemRecHits           = cms.InputTag("gemRecHits", "", "GEMLocalRECO"),
        gemSimHits           = cms.InputTag("g4SimHits", "MuonGEMHits"),
        muons                = cms.InputTag("muons"),
        # ref_track            = cms.InputTag("MuonAlignmentFromReferenceGlobalMuonRefit:Refitted"),
        vertexCollection     = cms.InputTag("offlinePrimaryVertices"),
        tracker_prop         = cms.bool(True),
        CSC_prop             = cms.bool(False),
        Segment_prop         = cms.bool(True),
        trackerRefit_prop    = cms.bool(False),
        SegmentReco_prop     = cms.bool(False),
        debug                = cms.bool(False),
        isCosmic             = cms.bool(False)
)

process.p = cms.Path(process.gemRecHits * process.analyzer)

