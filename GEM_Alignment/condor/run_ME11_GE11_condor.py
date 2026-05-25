import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_cff import Run3


process = cms.Process('GEMCSCanalyzer',Run3)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('RecoMuon.TrackingTools.MuonServiceProxy_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')

from Configuration.AlCa.GlobalTag import GlobalTag

### This is the misalignment part
misalign = True
if misalign:
  #db_file = 'sqlite_file:CRAFT2022_ME11Iter1_GEMIter0.db'
  db_file = 'sqlite_file:CRAFT2022_ME11Iter2_GEMIter0.db'
  #db_file = 'sqlite_file:CRAFT2022_ME11Iter2_GEMIter1.db'
  #db_file = 'sqlite_file:CRAFT2022_ME11Iter2_GEMIter2.db'
  process.GlobalTag.toGet = cms.VPSet(
    #GE11 rec/tag
    cms.PSet(
        connect = cms.string(db_file),
        record = cms.string('GEMAlignmentRcd'),
        tag = cms.string('GEMAlignmentRcd')
    ),
    cms.PSet(
        connect = cms.string(db_file),
        record = cms.string('GEMAlignmentErrorExtendedRcd'),
        tag = cms.string('GEMAlignmentErrorExtendedRcd')
    ),
    #ME11 rec/tag
    cms.PSet(
        connect = cms.string(db_file),
        record = cms.string('CSCAlignmentRcd'),
        tag = cms.string('CSCAlignmentRcd')
    ),
    cms.PSet(
        connect = cms.string(db_file),
        record = cms.string('CSCAlignmentErrorExtendedRcd'),
        tag = cms.string('CSCAlignmentErrorExtendedRcd')
    ),
    cms.PSet(record=cms.string('GlobalPositionRcd'), tag = cms.string('IdealGeometry'))
  )

  process.GEMGeometryESModule.applyAlignment = cms.bool(True)
  process.CSCGeometryESModule.applyAlignment = cms.bool(True)
################################


process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run3_data_prompt', '') #Antonello Comparison

process.MessageLogger.cerr.FwkReport.reportEvery = 5000

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.outputFile = 'out_ana.root'
options.inputFiles = 'input.root'
options.register ('nEvents',
			-1, #Max number of events
			VarParsing.multiplicity.singleton,
			VarParsing.varType.int,
			"Number of events")
options.parseArguments()
print(options.inputFiles)
print(options.outputFile)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(options.nEvents)
)
process.maxEvents.input = cms.untracked.int32(-1)


process.source = cms.Source("PoolSource",
				fileNames = cms.untracked.vstring(options.inputFiles),
				inputCommands = cms.untracked.vstring(
			"keep *",
			"drop TotemTimingDigiedmDetSetVector_totemTimingRawToDigi_TotemTiming_reRECO",
			"drop TotemTimingRecHitedmDetSetVector_totemTimingRecHits__reRECO"
			)
				)


#process.source.fileNames.append('file:'+file)

process.options = cms.untracked.PSet(
                        SkipEvent = cms.untracked.vstring('ProductNotFound')
                        )

process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile)) #variable name set above

process.ME11ana = cms.EDAnalyzer('ME11ana',
	process.MuonServiceProxy,
        csc2DRecHits = cms.InputTag("csc2DRecHits"),
	gemRecHits = cms.InputTag("gemRecHits"),
	gemSimHits = cms.InputTag("g4SimHits", "MuonGEMHits"),
        #muons = cms.InputTag("muons"),
        muons = cms.InputTag("ALCARECOMuAlGlobalCosmics:SelectedMuons"),
	vertexCollection = cms.InputTag("offlinePrimaryVerticies"),
        debug = cms.bool(False),
        isCosmic = cms.bool(True)
)



process.analyzer = cms.EDAnalyzer('analyzer',
        process.MuonServiceProxy,
        gemRecHits = cms.InputTag("gemRecHits"),
        gemSimHits = cms.InputTag("g4SimHits", "MuonGEMHits"),
        #muons = cms.InputTag("muons"),
        muons = cms.InputTag("ALCARECOMuAlGlobalCosmics:SelectedMuons"),
        vertexCollection = cms.InputTag("offlinePrimaryVerticies"),
        tracker_prop = cms.bool(True),
        CSC_prop = cms.bool(True),
        Segment_prop = cms.bool(True),
        debug = cms.bool(True),
        isCosmic = cms.bool(True)
)

process.p = cms.Path(process.analyzer + process.ME11ana)
