import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process("TEST", Run3)
# Message logger service
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')


from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, "auto:run3_data_prompt", '')
#process.GlobalTag = GlobalTag(process.GlobalTag, "auto:phase1_2025_design")
# process.GlobalTag = GlobalTag(process.GlobalTag, '150X_mcRun3_2025_realistic_Candidate_2025_05_21_14_21_17', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_mcRun3_2025_realistic_v6', '')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.source = cms.Source("EmptySource")

import Geometry.DTGeometryBuilder.dtGeometryDB_cfi
process.DTGeometryMuonMisalignedProducer = Geometry.DTGeometryBuilder.dtGeometryDB_cfi.DTGeometryESModule.clone()
process.DTGeometryMuonMisalignedProducer.appendToDataLabel = 'idealForMuonMisalignedProducer'
process.DTGeometryMuonMisalignedProducer.applyAlignment = cms.bool(False)
import Geometry.CSCGeometryBuilder.cscGeometryDB_cfi
process.CSCGeometryMuonMisalignedProducer = Geometry.CSCGeometryBuilder.cscGeometryDB_cfi.CSCGeometryESModule.clone()
process.CSCGeometryMuonMisalignedProducer.appendToDataLabel = 'idealForMuonMisalignedProducer'
process.CSCGeometryMuonMisalignedProducer.applyAlignment = cms.bool(True) #by default, in the GT, this is True. if this is set to False, need to comment it out. set to True when doing alignment for CSC specificlly 
import Geometry.GEMGeometryBuilder.gemGeometryDB_cfi
process.GEMGeometryMuonMisalignedProducer = Geometry.GEMGeometryBuilder.gemGeometryDB_cfi.GEMGeometryESModule.clone()
process.GEMGeometryMuonMisalignedProducer.appendToDataLabel = 'idealForMuonMisalignedProducer'
process.GEMGeometryMuonMisalignedProducer.applyAlignment = cms.bool(False) #set to true when GEM alignment is needed. otherwise False during CSC alignment

process.GEMAlDBWriter = cms.EDAnalyzer("GEMAlDBWriter",
                                       doChamber = cms.untracked.bool(False),
                                       doChamberError = cms.untracked.bool(False),
                                       doEndcap = cms.untracked.bool(False),
                                       doME11Chamber = cms.untracked.bool(True),
                                       doCSCEndcap = cms.untracked.bool(False),
                                       chamberFile = cms.untracked.string('../script/standAloneGemAlignment/Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop.csv'),          # GEM Chamber Alignment csv
                                       chamberErrorFile = cms.untracked.string('../script/standAloneGemAlignment/Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_error.csv'), # GEM Chamber Error Alignment csv
                                       endcapFile = cms.untracked.string('gemEndcap.csv'),       # GEM Endcap Alignment csv
                                       ME11ChamberFile = cms.untracked.string('../script/standAloneGemAlignment/test.csv'),      # ME1/1 Chamber Alignment csv
                                       CSCEndcapFile = cms.untracked.string('cscEndcap.csv')     # ME1/1 Endcap Alignment csv
                                      )

# Database output service if you want to store soemthing in MisalignedMuon
from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup

'''
#only use the needed lines below when using an geometry db file. when doing GEM alignment, don't have CSC file. same for when doing ME11 or CSC alignment, don't use GEM, only CSC db file
#TA commenting out below
old_db = 'GEMAllZeros.db' #Starting geometry DB

#process.muonCscAlignment = cms.ESSource("PoolDBESSource", CondDBSetup,
#                                     connect = cms.string('sqlite_file:{old_db}'.format(old_db = old_db)),
                                     #For some reason, CSC.db has a typo, the tag is 'CSCAlignmentRecored" not "CSCAlignmentRcd"
#                                     toGet   = cms.VPSet(cms.PSet(record = cms.string("CSCAlignmentRcd"), tag = cms.string("CSCAlignmentRcd")))
                                     #toGet   = cms.VPSet(cms.PSet(record = cms.string("CSCAlignmentRcd"), tag = cms.string("CSCAlignmentRecored"))) #CSC.db tag name
#                                     )

##### comment this out for the CSC.db file !!! Does not include GEMAlignment info
process.muonGemAlignment = cms.ESSource("PoolDBESSource", CondDBSetup,
                                     connect = cms.string('sqlite_file:{old_db}'.format(old_db = old_db)),
                                     toGet   = cms.VPSet(cms.PSet(record = cms.string("GEMAlignmentRcd"), tag = cms.string("GEMAlignmentRcd")))
                                     )
#####

#process.es_prefer_muonCscAlignment = cms.ESPrefer("PoolDBESSource","muonCscAlignment")
process.es_prefer_muonGemAlignment = cms.ESPrefer("PoolDBESSource","muonGemAlignment")

#process.globalPosition = cms.ESSource("PoolDBESSource", CondDBSetup,
#                                     connect = cms.string('sqlite_file:Run3v1.db'),
#                                     toGet   = cms.VPSet(cms.PSet(record = cms.string("GlobalPositionRcd"), tag = cms.string("GlobalPositionRcd")))
#                                     )
#process.es_prefer_globalPosition = cms.ESPrefer("PoolDBESSource","globalPosition")
'''

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    CondDBSetup,
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTAlignmentRcd'),
        tag = cms.string('DTAlignmentRcd')
        ),
        cms.PSet(
            record = cms.string('DTAlignmentErrorExtendedRcd'),
            tag = cms.string('DTAlignmentErrorExtendedRcd')
        ),
        cms.PSet(
            record = cms.string('CSCAlignmentRcd'),
            tag = cms.string('CSCAlignmentRcd')
        ),
        cms.PSet(
            record = cms.string('CSCAlignmentErrorExtendedRcd'),
            tag = cms.string('CSCAlignmentErrorExtendedRcd')
        ),
        cms.PSet(
            record = cms.string('GEMAlignmentRcd'),
            tag = cms.string('GEMAlignmentRcd')
        ),
        cms.PSet(
            record = cms.string('GEMAlignmentErrorExtendedRcd'),
            tag = cms.string('GEMAlignmentErrorExtendedRcd')
        ),
        cms.PSet(
            record = cms.string('GlobalPositionRcd'), #the GPR tag doesn't matter here anyway
            tag = cms.string('GlobalPositionRcd')
        )
    ),

    connect = cms.string('sqlite_file:Run2025C_muon0_ZMu_150X_dataRun3_Prompt_v1_backprop_v3.db')
)
process.p1 = cms.Path(process.GEMAlDBWriter)
process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('INFO'),
    default = cms.untracked.PSet(
        limit = cms.untracked.int32(10000000)
    )
)
