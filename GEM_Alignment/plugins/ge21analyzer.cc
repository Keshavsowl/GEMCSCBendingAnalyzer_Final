#include <assert.h>
#include <memory>
#include <cmath>
#include <iostream>
#include <sstream>
#include <boost/foreach.hpp>
#define foreach BOOST_FOREACH

//user include files below
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "RecoMuon/TrackingTools/interface/MuonServiceProxy.h"

#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "MagneticField/Engine/interface/MagneticField.h"

#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/CSCRecHit/interface/CSCRecHit2D.h"
#include "DataFormats/CSCRecHit/interface/CSCSegmentCollection.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigiCollection.h"
#include "DataFormats/CSCDigi/interface/CSCCorrelatedLCTDigi.h"
#include "DataFormats/GEMRecHit/interface/GEMRecHitCollection.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "Geometry/CSCGeometry/interface/CSCGeometry.h"
#include "Geometry/GEMGeometry/interface/GEMGeometry.h"
#include "Geometry/GEMGeometry/interface/GEMEtaPartitionSpecs.h"
#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/CommonTopologies/interface/StripTopology.h"

#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"

#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"

using namespace std;
using namespace edm;


struct MuonData_GE21
{
  void init();
  TTree* book(TTree *t, int prop_type);
  //============ Muon Info ================//
  int muon_charge; float muon_pt; float muon_eta; float muon_momentum;
  unsigned long long evtNum; unsigned long long lumiBlock; int muonIdx;
  int runNum;
  bool has_TightID; bool isPFIsoTightMu;
  //============ Propagation Info =========//
  float prop_GP[3]; float prop_LP[3]; float prop_startingPoint_GP[3];
  float prop_dxdz;  float prop_yroll; float prop_localphi_rad;
  float prop_localphi_deg;            float prop_globalphi_rad;
  bool has_prop;    bool has_fidcut;
  int prop_location[5];
  //============ Track Info ===============//
  float track_chi2; float track_ndof; int n_ME21_segment;
  int which_track;  int hasME21;      int hasME21RecHit;
  int nCSCSeg;      int nDTSeg;       int nME21RecHits;
  float ME21_BunchX;                  int ME21_strip;
  int ME21_location[5];               int inner_or_outer_mom;
  float ME21_Segment_Direction[3];
  float ME21_Segment_slope_dxdz;      float ME21_Segment_slope_dydz;
  int eighthStripDiff;
  //============ Rechit Info =============//
  float rechit_GP[3]; float rechit_LP[3];        bool has_rechit;
  float rechit_yroll; float rechit_localphi_rad; float rechit_localphi_deg;
  int rechit_first_strip;     int rechit_CLS;    int rechit_BunchX;
  float RdPhi;        float RdPhi_Corrected;     int rechit_detId;
  float dPhi;   float dPhi_Corrected;
  float bending_angle;
  int nRecHitsTot;    int nRecHits5;             int nRecHits2;
  int rechit_location[5];
  int nRecHitsRpos1L1; int nRecHitsRpos1L2;
  int nRecHitsRneg1L1; int nRecHitsRneg1L2;
  //=========== Sim info for MC ==========//
  float sim_GP[3];   float sim_LP[3];
  float simDy;       float sim_yroll;            int nSim;
};

void MuonData_GE21::init()
{
  //=========== Muon Info ===============//
  muon_charge = 9999; muon_pt = 99999; muon_eta = 9999; muon_momentum = 9999;
  evtNum = 99999999; lumiBlock = 99999999; muonIdx = 99999999; runNum = 99999999;
  has_TightID = 0;    isPFIsoTightMu = 0;
  //=========== Propagation Info =======//
  for(int i=0; i<3; ++i){
    prop_GP[i] = 99999; prop_LP[i] = 99999; prop_startingPoint_GP[i] = 99999;
  }
  prop_dxdz = 99999; prop_yroll = 99999;
  prop_localphi_rad = 99999; prop_localphi_deg = 99999;
  prop_globalphi_rad = 99999;
  has_prop = false; has_fidcut = false;
  for(int i=0 ; i<5; ++i){
    prop_location[i] = 99999;
  }
  //=========== Track Info =============//
  track_chi2 = 999999; track_ndof = 999999; n_ME21_segment = 999999; which_track = 999999;
  hasME21 = 0; hasME21RecHit = 0;
  nCSCSeg = 999999; nDTSeg = 999999; nME21RecHits = 999999; ME21_BunchX = 999999; ME21_strip = 999999;
  for(int i=0; i<5; ++i){
    ME21_location[i] = 999999;
  }
  inner_or_outer_mom = 99999;
  for (int i=0; i<3; ++i){
    ME21_Segment_Direction[i] = 999999;
  }
  ME21_Segment_slope_dxdz = 999999;    ME21_Segment_slope_dydz = 999999;
  eighthStripDiff = 99999;
  //=========== Rechit Info ===========//
  for (int i=0; i<3; ++i){
    rechit_GP[i] = 999999; rechit_LP[i] = 999999;
  }
  rechit_yroll = 999999; rechit_localphi_rad = 999999; rechit_localphi_deg = 999999;
  has_rechit = false;
  rechit_first_strip = 999999; rechit_CLS = 999999; rechit_BunchX = 999999;
  RdPhi = 999999; RdPhi_Corrected = 999999; rechit_detId = 999999;
  dPhi = 999999; dPhi_Corrected = 999999;
  bending_angle = 999999;
  nRecHitsTot = 999999; nRecHits5 = 999999; nRecHits2 = 999999;
  for (int i=0; i<5; ++i){
    rechit_location[i] = 999999;
  }
  nRecHitsRpos1L1 = 999999; nRecHitsRpos1L2 = 999999;
  nRecHitsRneg1L1 = 999999; nRecHitsRneg1L2 = 999999;
  //Sim info for MC
  for (int i=0; i<3; ++i){
    sim_GP[i] = 9999999; sim_LP[i] = 9999999;
  }
  simDy = 9999999; sim_yroll = 9999999; nSim = 9999999;
}

TTree* MuonData_GE21::book(TTree *t, int prop_type){
  edm::Service< TFileService > fs;
  if(prop_type == 1){
    t = fs->make<TTree>("CSC_Prop", "CSC_Prop");
  }
  else if(prop_type == 2){
    t = fs->make<TTree>("Inner_Prop", "Inner_Prop");
  }
  else if(prop_type == 3){
    t = fs->make<TTree>("ME21Seg_Prop", "ME21Seg_Prop");
  }
  else{
    std::cout << "Bad prop type, failure, doesnt fall under the 3 prop_type listed" << std::endl;
  }
  //=========== Muon Info =============//
  t->Branch("muon_charge", &muon_charge); t->Branch("muon_pt", &muon_pt);
  t->Branch("muon_eta", &muon_eta);       t->Branch("muon_momentum", &muon_momentum);
  t->Branch("evtNum", &evtNum);           t->Branch("lumiBlock", &lumiBlock);
  t->Branch("runNum", &runNum);           t->Branch("muonIdx", &muonIdx);
  t->Branch("has_TightID", &has_TightID); t->Branch("isPFIsoTightMu", &isPFIsoTightMu);
  //========== Propagation Info =======//
  t->Branch("prop_GP", &prop_GP, "prop_GP[3] (x,y,z)/F");
  t->Branch("prop_LP", &prop_LP, "prop_LP[3] (x,y,z)/F");
  t->Branch("prop_dxdz", &prop_dxdz);
  t->Branch("prop_startingPoint_GP", &prop_startingPoint_GP, "prop_startingPoint_GP[3] (x,y,z)/F");
  t->Branch("prop_yroll", &prop_yroll);
  t->Branch("prop_localphi_rad", &prop_localphi_rad);
  t->Branch("prop_localphi_deg", &prop_localphi_deg);
  t->Branch("prop_globalphi_rad", &prop_globalphi_rad);
  t->Branch("has_prop", &has_prop);
  t->Branch("has_fidcut", &has_fidcut);
  t->Branch("prop_location", &prop_location, "prop_location[5] (reg, sta, cha, lay, rol)/I");
  //========== Track Info =============//
  t->Branch("track_chi2", &track_chi2);         t->Branch("track_ndof", &track_ndof);
  t->Branch("n_ME21_segment", &n_ME21_segment); t->Branch("which_track", &which_track);
  t->Branch("hasME21", &hasME21);               t->Branch("hasME21RecHit", &hasME21RecHit);
  t->Branch("eighthStripDiff", &eighthStripDiff);
  t->Branch("nCSCSeg", &nCSCSeg);               t->Branch("nDTSeg", &nDTSeg);
  t->Branch("nME21RecHits", &nME21RecHits);     t->Branch("ME21_BunchX", &ME21_BunchX);
  t->Branch("ME21_strip", &ME21_strip);
  t->Branch("ME21_location", &ME21_location, "ME21_location[5] (end, sta, ring, cha, lay)/I");
  t->Branch("ME21_Segment_Direction", &ME21_Segment_Direction, "ME21_Segment_Direction[3] (x,y,z)/F");
  t->Branch("ME21_Segment_slope_dxdz", &ME21_Segment_slope_dxdz);
  t->Branch("ME21_Segment_slope_dydz", &ME21_Segment_slope_dydz);
  t->Branch("inner_or_outer_mom", &inner_or_outer_mom, "inner_or_outer_mom (0 = inner, 1 = outer)/I");
  //========== Rechit Info ============//
  t->Branch("rechit_GP", &rechit_GP, "rechit_GP[3] (x,y,z)/F");
  t->Branch("rechit_LP", &rechit_LP, "rechit_LP[3] (x,y,z)/F");
  t->Branch("rechit_yroll", &rechit_yroll);
  t->Branch("rechit_localphi_rad", &rechit_localphi_rad);
  t->Branch("rechit_localphi_deg", &rechit_localphi_deg);
  t->Branch("has_rechit", &has_rechit);
  t->Branch("rechit_first_strip", &rechit_first_strip);
  t->Branch("rechit_CLS", &rechit_CLS);
  t->Branch("rechit_BunchX", &rechit_BunchX);
  t->Branch("RdPhi", &RdPhi);
  t->Branch("RdPhi_Corrected", &RdPhi_Corrected);  
  t->Branch("dPhi", &dPhi);
  t->Branch("dPhi_Corrected", &dPhi_Corrected);
  t->Branch("rechit_detId", &rechit_detId);
  t->Branch("bending_angle", &bending_angle);
  t->Branch("nRecHitsTot", &nRecHitsTot);
  t->Branch("nRecHits2", &nRecHits2);
  t->Branch("nRecHits5", &nRecHits5);
  t->Branch("rechit_location", &rechit_location, "rechit_location[5] (reg, sta, cha, lay, rol)/I");
  t->Branch("nRecHitsRpos1L1", &nRecHitsRpos1L1);
  t->Branch("nRecHitsRpos1L2", &nRecHitsRpos1L2);
  t->Branch("nRecHitsRneg1L1", &nRecHitsRneg1L1);
  t->Branch("nRecHitsRneg1L2", &nRecHitsRneg1L2);
  //========== Sim Info ==============//
  t->Branch("sim_GP", &sim_GP, "sim_GP[3] (x,y,z)/F");
  t->Branch("sim_LP", &sim_LP, "sim_LP[3] (x,y,z)/F");
  t->Branch("simDy", &simDy);
  t->Branch("sim_yroll", &sim_yroll);
  t->Branch("nSim", &nSim);
  return t;
}

class ge21analyzer : public edm::one::EDAnalyzer<> {
public:
  explicit ge21analyzer(const edm::ParameterSet&);
  ~ge21analyzer(){};

private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void beginJob() ;
  virtual void endJob() ;

  void propagate(const reco::Muon* mu, int prop_type, const edm::Event& iEvent, int i);
  void CSCSegmentCounter(const reco::Muon* mu, MuonData_GE21& data_);
  void propagate_to_GEM(const reco::Muon* mu, const GEMEtaPartition* ch, int prop_type, bool &tmp_has_prop, GlobalPoint &pos_GP, MuonData_GE21& data_);
  void GEM_rechit_matcher(const GEMEtaPartition* ch, LocalPoint prop_LP, MuonData_GE21& data_);
  void GEM_simhit_matcher(const GEMEtaPartition* ch, GlobalPoint prop_GP, MuonData_GE21& data_);
  float RdPhi_func(float stripAngle, const edm::OwnVector<GEMRecHit, edm::ClonePolicy<GEMRecHit> >::const_iterator rechit, float prop_localx, float prop_localy, const GEMEtaPartition* ch);
  bool fidcutCheck(float local_y, float localphi_deg, const GEMEtaPartition* ch);

  edm::EDGetTokenT<GEMRecHitCollection> gemRecHits_;
  edm::Handle<GEMRecHitCollection> gemRecHits;
  edm::EDGetTokenT<vector<PSimHit> > gemSimHits_;
  edm::Handle<vector<PSimHit> > gemSimHits;
  edm::EDGetTokenT<edm::View<reco::Muon> > muons_;
  edm::EDGetTokenT<reco::VertexCollection> vertexCollection_;
  edm::EDGetTokenT<CSCSegmentCollection> cscSegments_;

  edm::Service<TFileService> fs;
  MuonServiceProxy* theService_;
  
  edm::ESHandle<Propagator> propagator_;
  edm::ESHandle<TransientTrackBuilder> ttrackBuilder_;

  ESHandle<GlobalTrackingGeometry> theTrackingGeometry;
  
  edm::ESHandle<GEMGeometry> GEMGeometry_;
  edm::ESHandle<CSCGeometry> CSCGeometry_;

  bool CSC_prop; bool tracker_prop; bool Segment_prop;
  vector<int> prop_list;
  bool debug;
  bool isCosmic;

  MuonData_GE21 data_;
  TTree* CSC_tree; TTree* Tracker_tree; TTree* Segment_tree;
  TH2D* nME21_col_vs_matches = new TH2D("nME21_test", "nME21_test", 5, 0, 5, 5, 0, 5);

  bool isMC;
  const CSCSegment *ME21_segment;

  const edm::ESGetToken<GEMGeometry, MuonGeometryRecord> gemGeomToken_;
  const edm::ESGetToken<CSCGeometry, MuonGeometryRecord> cscGeomToken_;
  const edm::ESGetToken<TransientTrackBuilder, TransientTrackRecord> ttkToken_;
  const edm::ESGetToken<GlobalTrackingGeometry, GlobalTrackingGeometryRecord> geomToken_;
};


ge21analyzer::ge21analyzer(const edm::ParameterSet& iConfig)
  : gemGeomToken_(esConsumes()),
    cscGeomToken_(esConsumes()),
    ttkToken_(esConsumes(edm::ESInputTag("", "TransientTrackBuilder"))),
    geomToken_(esConsumes())
{
  cout << "Begin ge21analyzer" << endl;
  edm::ParameterSet serviceParameters = iConfig.getParameter<edm::ParameterSet>("ServiceParameters");
  theService_ = new MuonServiceProxy(serviceParameters, consumesCollector());
  muons_ = consumes<View<reco::Muon> >(iConfig.getParameter<InputTag>("muons"));
  vertexCollection_ = consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexCollection")); 
  gemRecHits_ = consumes<GEMRecHitCollection>(iConfig.getParameter<edm::InputTag>("gemRecHits"));
  gemSimHits_ = consumes<vector<PSimHit> >(iConfig.getParameter<edm::InputTag>("gemSimHits"));
  cscSegments_ = consumes<CSCSegmentCollection>(edm::InputTag("cscSegments"));

  tracker_prop = iConfig.getParameter<bool>("tracker_prop");
  CSC_prop = iConfig.getParameter<bool>("CSC_prop");
  Segment_prop = iConfig.getParameter<bool>("Segment_prop");
  debug = iConfig.getParameter<bool>("debug");
  isCosmic = iConfig.getParameter<bool>("isCosmic");
  std::cout << "tracker_prop " << tracker_prop << "\tCSC_prop " << CSC_prop << "\tSegment_prop " << Segment_prop << "\tdebug " << debug << std::endl;

  if(CSC_prop){CSC_tree = data_.book(CSC_tree, 1); prop_list.push_back(1);}
  if(tracker_prop){Tracker_tree = data_.book(Tracker_tree, 2); prop_list.push_back(2);}
  if(Segment_prop){Segment_tree = data_.book(Segment_tree, 3); prop_list.push_back(3);}
}


void
ge21analyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  GEMGeometry_ = &iSetup.getData(gemGeomToken_);
  CSCGeometry_ = &iSetup.getData(cscGeomToken_);
  ttrackBuilder_ = &iSetup.getData(ttkToken_);
  theTrackingGeometry = &iSetup.getData(geomToken_);

  theService_->update(iSetup);
  auto propagator = theService_->propagator("SteppingHelixPropagatorAny");

  isMC = false;
  if (! iEvent.eventAuxiliary().isRealData()) isMC = true;
  iEvent.getByToken(gemRecHits_, gemRecHits);
  if (isMC) {
    iEvent.getByToken(gemSimHits_, gemSimHits);
  }

  edm::Handle<View<reco::Muon> > muons;
  if (! iEvent.getByToken(muons_, muons)) return;
  if (muons->size() == 0) return;

  edm::Handle<CSCSegmentCollection> cscSegments;
  if (! iEvent.getByToken(cscSegments_, cscSegments)){std::cout << "Bad segments" << std::endl;}

  if (debug) cout << "New! EventNumber = " << iEvent.eventAuxiliary().event() << " LumiBlock = " << iEvent.eventAuxiliary().luminosityBlock() << " RunNumber = " << iEvent.run() << endl;

  for (size_t i = 0; i < muons->size(); ++i){
    edm::RefToBase<reco::Muon> muRef = muons->refAt(i);
    const reco::Muon* mu = muRef.get();
    if (not mu->isGlobalMuon()) continue;
    if (debug) cout << "new muon, i = " << i << endl;
    
    if (!(mu->passed(reco::Muon::PFIsoTight))) continue;
    for (auto it = std::begin(prop_list); it != std::end(prop_list); ++it){
      if (debug) std::cout << "\tprop " << *it << "about to start propagate" << std::endl;
      int prop_type = *it;
      propagate(mu, prop_type, iEvent, i);
    }
  }
}

void ge21analyzer::propagate(const reco::Muon* mu, int prop_type, const edm::Event& iEvent, int i){
  const reco::Track* Track;
  reco::TransientTrack ttTrack;
  TTree* tree;
  if (debug) cout << "\tGetting tree, Track, ttTrack " << endl;


  //===============start of vertex edit by TA
  edm::Handle<reco::VertexCollection> vertexCollection;
  iEvent.getByToken(vertexCollection_, vertexCollection);
  reco::Vertex vertexSelection; //choose type of vertex needed
  for (const auto& vertex : *vertexCollection.product()){
    if (vertexCollection.isValid()) {
      vertexSelection = vertex;
      break; //selecting the first valid vertex
    }
  }
  if (prop_type == 1){
    tree = CSC_tree;
    if (!(mu->isGlobalMuon())) {return;}
    if (!(mu->globalTrack().isNonnull())) {return;}
    Track = mu->globalTrack().get();
    ttTrack = ttrackBuilder_->build(Track);
  }
  else if (prop_type == 2){
    tree = Tracker_tree; 
    if (!(mu->isTrackerMuon())) {return;}
    if (!(mu->track().isNonnull())) {return;}
    Track = mu->track().get();
    ttTrack = ttrackBuilder_->build(Track);
  }
  else if (prop_type == 3){
    tree = Segment_tree;

    if (isCosmic){
      if (!(mu->isStandAloneMuon())){return;}
      if (!(mu->outerTrack().isNonnull())){return;}
      Track = mu->outerTrack().get();
      ttTrack = ttrackBuilder_->build(Track);
    }
    else{ 
      if (!(mu->isGlobalMuon())) {return;}
      if (!(mu->globalTrack().isNonnull())) {return;}
      Track = mu->globalTrack().get();
      ttTrack = ttrackBuilder_->build(Track);
    }
  }
  else{
    if (debug) cout << "Bad prop type, failure, not one of the 3" << endl;
    return;
  }

  if (!(ttTrack.isValid())) {cout << "Bad event, no track" << endl;}
  if (debug) cout << "Got track, now initiating data" << endl;
  data_.init();
  //======================Muon Info=======================
  data_.muon_charge = mu->charge(); data_.muon_pt = mu->pt();  data_.muon_eta = mu->eta();
  data_.muon_momentum = mu->momentum().mag2();                 data_.evtNum = iEvent.eventAuxiliary().event();
  data_.lumiBlock = iEvent.eventAuxiliary().luminosityBlock(); data_.muonIdx = data_.evtNum*100 + i;
  data_.runNum = iEvent.run();
  data_.has_TightID = muon::isTightMuon(*mu, vertexSelection);

  //=====================Track Info=======================
  data_.track_chi2 = Track->chi2(); data_.track_ndof = Track->ndof();
  CSCSegmentCounter(mu, data_);
  if (prop_type == 3 and data_.hasME21 != 1) {return;}
  //================Propagation Info===================
  if (debug) cout << "starting chamber loop" << endl;
  for (const auto& ch : GEMGeometry_->etaPartitions()) {
    if (ch->id().station() != 2) continue; //only concerned about GE1/1
    GlobalPoint tmp_prop_GP;        bool tmp_has_prop = 0;
    propagate_to_GEM(mu, ch, prop_type, tmp_has_prop, tmp_prop_GP, data_);
    if (tmp_has_prop){
      LocalPoint tmp_prop_LP = ch->toLocal(tmp_prop_GP);
      //==============RecHit Info======================
      GEM_rechit_matcher(ch, tmp_prop_LP, data_);
      if (isMC){
        GEM_simhit_matcher(ch, tmp_prop_GP, data_);
      }
      if (prop_type==3 and debug) cout << "Filling Tree for prop_type 3" << endl;
      tree->Fill();
    }
  }
}

void ge21analyzer::CSCSegmentCounter(const reco::Muon* mu, MuonData_GE21& data_){
  if (!(mu->isGlobalMuon())) {return;}
  if (!(mu->globalTrack().isNonnull())) {return;}
  const reco::Track* Track = mu->globalTrack().get();
  int tmp_CSC_counter = 0;   int tmp_DT_counter = 0;   int tmp_ME21_counter = 0;
  int tmp_ME21RecHit_counter = 0; float tmp_ME21_BunchX = 99999;
  int tmp_ME21_strip = 99999;
  float tmp_me11_segment_x; float tmp_me11_segment_y; float tmp_me11_segment_z;
  float tmp_me11_segment_slope_dxdz; float tmp_me11_segment_slope_dydz;

  //Below part is for Cosmic Muon Study
  if (isCosmic){
    tmp_DT_counter = mu->numberOfSegments(1,1) + mu->numberOfSegments(2,1) + mu->numberOfSegments(3,1) + mu->numberOfSegments(4,1);
    tmp_CSC_counter = mu->numberOfSegments(1,2) + mu->numberOfSegments(2,2) + mu->numberOfSegments(3,2) + mu->numberOfSegments(4,2);
    auto matches = mu->matches();
    for (auto MCM : matches){
      if (MCM.detector() != 2) continue;
      for (auto MSM : MCM.segmentMatches){
        auto cscSegRef = MSM.cscSegmentRef;
        auto cscDetID = cscSegRef->cscDetId();
        if (cscDetID.station() == 2 and cscDetID.ring() == 1){
          tmp_ME21_counter++;
          if (debug){std::cout << "isCosmic = True! Getting ME21 Segment" <<std::endl;}
          ME21_segment = cscSegRef.get();
          tmp_ME21RecHit_counter = (cscSegRef.get())->nRecHits(); //may need to modify this function in case of multiple segments
          tmp_ME21_BunchX = ME21_segment->time();
          auto cscDetID_FAKE = CSCDetId(cscDetID.endcap(), cscDetID.station(), cscDetID.ring(), cscDetID.chamber(), 3);
          const CSCLayer* tmp_ME21_layer = CSCGeometry_->layer(cscDetID_FAKE);
          const CSCLayerGeometry* tmp_ME21_layer_geo = tmp_ME21_layer->geometry();
          tmp_ME21_strip = tmp_ME21_layer_geo->nearestStrip(ME21_segment->localPosition());
          data_.ME21_location[0] = cscDetID.endcap();
          data_.ME21_location[1] = cscDetID.station();
          data_.ME21_location[2] = cscDetID.ring();
          data_.ME21_location[3] = cscDetID.chamber();
          data_.ME21_location[4] = cscDetID.layer();
        }      
      }
    }
  }
  //End of Cosmics

  else{
    //if (debug) cout << "Track->validFraction() " << Track->validFraction() << "\t Track->recHitsSize(): " << Track->recHitsSize() << endl;
    //if (Track->validFraction() > 0.0) return;
    //if (debug) cout << "checking if Track->validFraction() > 0.0 passes here" << endl;
    if (debug) cout << "Track->recHitsSize(): " << Track->recHitsSize() << endl;
    for (size_t RecHit_iter = 0; RecHit_iter != Track->recHitsSize(); RecHit_iter++){
      const TrackingRecHit* RecHit = (Track->recHit(RecHit_iter)).get();
      DetId RecHitId = RecHit->geographicalId();
      uint16_t RecHitDetId = RecHitId.det();

      if (RecHitDetId == DetId::Muon){
        uint16_t RecHitSubDet = RecHitId.subdetId();
        if (RecHitSubDet == (uint16_t)MuonSubdetId::CSC){
          if (CSCDetId(RecHitId).station() == 2 and CSCDetId(RecHitId).ring() == 1 and RecHit->dimension() == 4){
            tmp_ME21_counter++;
            RecSegment* Rec_segment = (RecSegment*)RecHit;
            ME21_segment = (CSCSegment*)Rec_segment;
            tmp_me11_segment_x = ME21_segment->localDirection().x();
            tmp_me11_segment_y = ME21_segment->localDirection().y();
            tmp_me11_segment_z = ME21_segment->localDirection().z();
            tmp_me11_segment_slope_dxdz = tmp_me11_segment_x / tmp_me11_segment_z;
            tmp_me11_segment_slope_dydz = tmp_me11_segment_y / tmp_me11_segment_z;
            
            tmp_ME21_BunchX = ((CSCRecHit2D*)RecHit)->wgroupsBX();
            auto cscDetID_FAKE = CSCDetId(CSCDetId(RecHitId).endcap(), CSCDetId(RecHitId).station(), CSCDetId(RecHitId).ring(), CSCDetId(RecHitId).chamber(), 3);
            const CSCLayer* tmp_ME21_layer = CSCGeometry_->layer(cscDetID_FAKE);
            const CSCLayerGeometry* tmp_ME21_layer_geo = tmp_ME21_layer->geometry();
            tmp_ME21_strip = tmp_ME21_layer_geo->nearestStrip(ME21_segment->localPosition());
            data_.ME21_Segment_Direction[0] = tmp_me11_segment_x;   data_.ME21_Segment_Direction[1] = tmp_me11_segment_y; data_.ME21_Segment_Direction[2] = tmp_me11_segment_z;
            if (debug) cout << "ME21 segment location endcap:station:ring:chamber:layer " << CSCDetId(RecHitId).endcap() << ":" << CSCDetId(RecHitId).station() << ":" << CSCDetId(RecHitId).ring() << ":" << CSCDetId(RecHitId).chamber() << ":" << CSCDetId(RecHitId).layer() << endl;
            if (debug) cout << "ME21 segment direction x:y:z " << data_.ME21_Segment_Direction[0] << ":" << data_.ME21_Segment_Direction[1] << ":" << data_.ME21_Segment_Direction[2] << endl;
            data_.ME21_Segment_slope_dxdz = tmp_me11_segment_slope_dxdz;  data_.ME21_Segment_slope_dydz= tmp_me11_segment_slope_dydz;
            if (debug) cout << "segment slope dx/dz:dy/dz " << data_.ME21_Segment_slope_dxdz << ":" << data_.ME21_Segment_slope_dydz << endl;
            data_.ME21_location[0] = CSCDetId(RecHitId).endcap();
            data_.ME21_location[1] = CSCDetId(RecHitId).station();
            data_.ME21_location[2] = CSCDetId(RecHitId).ring();
            data_.ME21_location[3] = CSCDetId(RecHitId).chamber();
            data_.ME21_location[4] = CSCDetId(RecHitId).layer();
          }
          if (CSCDetId(RecHitId).station() == 2 and CSCDetId(RecHitId).ring() == 1){tmp_ME21RecHit_counter++;}
          if (RecHit->dimension() == 4) {tmp_CSC_counter++;}
          if (debug) cout << "tmp_CSC_counter: " << tmp_CSC_counter << endl;
        }
        if (RecHitSubDet == (uint16_t)MuonSubdetId::DT){
          if (RecHit->dimension() > 1) {tmp_DT_counter++;}
        }
      }
    }
  }
  data_.nCSCSeg = tmp_CSC_counter; data_.nDTSeg = tmp_DT_counter;
  data_.n_ME21_segment = tmp_ME21_counter;
  data_.nME21RecHits = tmp_ME21RecHit_counter;
  data_.ME21_BunchX = tmp_ME21_BunchX;
  data_.ME21_strip = tmp_ME21_strip;
  if (data_.n_ME21_segment >=1 and data_.n_ME21_segment < 1000) {data_.hasME21 = 1;}
  if (debug) cout << "data_.hasME21: " << data_.hasME21 << "\tdata_.n_ME21_segment: " << data_.n_ME21_segment << endl;
}

void ge21analyzer::propagate_to_GEM(const reco::Muon* mu, const GEMEtaPartition* ch, int prop_type, bool &tmp_has_prop, GlobalPoint &pos_GP, MuonData_GE21& data_){
  const reco::Track* Track;
  reco::TransientTrack ttrack;
  tmp_has_prop = false;
  int tmp_inner_or_outer_mom = 99999;
  const BoundPlane& bps(ch->surface());
  auto propagator = theService_->propagator("SteppingHelixPropagatorAny");
  const auto& etaPart_ch = GEMGeometry_->etaPartition(ch->id());
  TrajectoryStateOnSurface tsos_ch; TrajectoryStateOnSurface tsos_seg;
  GlobalPoint pos_startingPoint_GP;
  float prop_dxdz = 99999;
  if (prop_type==1 or prop_type==2){
    if (prop_type==1){
      if (!(mu->isGlobalMuon())) return;
      Track = mu->globalTrack().get();
      ttrack = ttrackBuilder_->build(Track);
    }
    if (prop_type==2){
      if (!(mu->isTrackerMuon())) return;
      Track = mu->track().get();
      ttrack = ttrackBuilder_->build(Track);
    }
    float inner_delta = abs(ttrack.innermostMeasurementState().globalPosition().z() - GEMGeometry_->etaPartition(ch->id())->toGlobal(etaPart_ch->centreOfStrip(etaPart_ch->nstrips()/2)).z());
    float outer_delta = abs(ttrack.outermostMeasurementState().globalPosition().z() - GEMGeometry_->etaPartition(ch->id())->toGlobal(etaPart_ch->centreOfStrip(etaPart_ch->nstrips()/2)).z());
    float used_delta = 0;
    if (inner_delta < outer_delta){
      tsos_seg = ttrack.innermostMeasurementState();
      tsos_ch = propagator->propagate(tsos_seg, ch->surface());
      used_delta = inner_delta;
      if (prop_type==1){data_.which_track = 1;}
      else{data_.which_track = 0;}
    }
    else{
      tsos_seg = ttrack.outermostMeasurementState();
      tsos_ch = propagator->propagate(tsos_seg, ch->surface());
      used_delta = outer_delta;
      if (prop_type==1){data_.which_track = 0;}
      else{data_.which_track = 1;}
    }
    if (tsos_ch.isValid()){
      const LocalPoint pos_local_ch = ch->toLocal(tsos_ch.globalPosition());
      const LocalPoint pos2D_local_ch(pos_local_ch.x(), pos_local_ch.y(), 0);
      if (!(tsos_ch.globalPosition().z() * tsos_seg.globalPosition().z() < 0) and bps.bounds().inside(pos2D_local_ch) and ch->id().station() == 2 and ch->id().ring() == 1) {
        tmp_has_prop = true;
        if (debug) {cout << "Delta to GEM = " << used_delta << "\tprop " << prop_type << std::endl;}
        pos_GP = tsos_ch.globalPosition();
        pos_startingPoint_GP = tsos_seg.globalPosition();
      }
    }
  }
  if (prop_type == 3){
    LocalVector momentum_at_surface = ME21_segment->localDirection(); //No momentum for segments;

    DetId segDetId = ME21_segment->geographicalId();
    const GeomDet* segDet = theTrackingGeometry->idToDet(segDetId);
    if (mu->isTrackerMuon()) {
      Track = mu->track().get();
      if (Track != 0) {
        tmp_inner_or_outer_mom = 0;
        momentum_at_surface = momentum_at_surface*(Track->outerP()); //If inner track exists, use momentum
        //if (debug) cout << "Got inner momentum = " << momentum_at_surface << endl;
      }
    }
    else if (mu->isGlobalMuon()){
      Track = mu->globalTrack().get();
      if (Track != 0){
        tmp_inner_or_outer_mom = 1;
        momentum_at_surface = momentum_at_surface*(Track->outerP()); //If no inner 
        if (debug) cout << "Got outer momentum = " << momentum_at_surface << endl;
      }
      else{
        if (debug) cout << "No tracks!" << endl;
        return;
      }
    }
    else{
      return;
    }
    //if (debug) cout << "Got momentum" << endl;
    LocalTrajectoryParameters param(ME21_segment->localPosition(), momentum_at_surface, mu->charge());
    AlgebraicSymMatrix mat(5,0);
    mat = ME21_segment->parametersError().similarityT( ME21_segment->projectionMatrix() );
    LocalTrajectoryError error(asSMatrix<5>(mat));
    TrajectoryStateOnSurface tsos_seg(param, error, segDet->surface(), &*theService_->magneticField());
    TrajectoryStateOnSurface tsos_ch = propagator->propagate(tsos_seg, ch->surface());
    if (tsos_ch.isValid()){
      //if (debug) cout << "tsos_ch valid" << endl;
      const LocalPoint pos_local_ch = ch->toLocal(tsos_ch.globalPosition());
      const LocalPoint pos2D_local_ch(pos_local_ch.x(), pos_local_ch.y(), 0);
      const LocalVector direction_local_ch = ch->toLocal(tsos_ch.globalDirection());

      if (!(tsos_ch.globalPosition().z() * tsos_seg.globalPosition().z() < 0) and bps.bounds().inside(pos2D_local_ch) and ch->id().station() == 2 and ch->id().ring() == 1) {
        tmp_has_prop = true;
        //if (debug) cout << "tmp_has_prop is true now" << endl;
        pos_GP = tsos_ch.globalPosition();
        pos_startingPoint_GP = tsos_seg.globalPosition();
        prop_dxdz = direction_local_ch.x()/direction_local_ch.z();
        if (debug){ 
          cout << "calculating R = sqrt(x^2 + y^2) = " << pow( pow(pos_GP.x(), 2) + pow(pos_GP.y(), 2), 0.5) << endl;
        }

      }
    }
  }
  if (tmp_has_prop){
    if (debug) cout << "Valid GEM prop" << endl;
    const auto& etaPart_ch = GEMGeometry_->etaPartition(ch->id());
    const float prop_y_to_center = etaPart_ch->toGlobal(etaPart_ch->centreOfStrip(etaPart_ch->nstrips()/2)).perp(); //y distance to the current eta part
    const float prop_y_to_chamber = (GEMGeometry_->chamber(ch->id()))->toLocal(etaPart_ch->toGlobal(etaPart_ch->centreOfStrip(etaPart_ch->nstrips()/2))).y();
    LocalPoint tmp_prop_LP = ch->toLocal(pos_GP);
    data_.prop_GP[0] = pos_GP.x(); data_.prop_GP[1] = pos_GP.y(); data_.prop_GP[2] = pos_GP.z();
    data_.prop_LP[0] = tmp_prop_LP.x(); data_.prop_LP[1] = tmp_prop_LP.y() + prop_y_to_chamber; data_.prop_LP[2] = tmp_prop_LP.z();
    data_.prop_dxdz = prop_dxdz;
    data_.prop_startingPoint_GP[0] = pos_startingPoint_GP.x(); data_.prop_startingPoint_GP[1] = pos_startingPoint_GP.y(); data_.prop_startingPoint_GP[2] = pos_startingPoint_GP.z();
    data_.prop_yroll = tmp_prop_LP.y();
    LocalPoint local_to_center(tmp_prop_LP.x(), tmp_prop_LP.y() + prop_y_to_center, 0);
    float local_phi = local_to_center.phi();
    data_.prop_localphi_rad = (3.14159265/2.) - local_phi;
    data_.prop_localphi_deg = ((3.14159265/2.) - local_phi)*(180./3.14159265);
    data_.prop_globalphi_rad = pos_GP.phi();
    if (debug) cout << "propagation local x: local y: local phi [rad]" << data_.prop_LP[0] << ":" << data_.prop_LP[1] << ":" << data_.prop_localphi_rad << endl;
    data_.has_prop = tmp_has_prop;
    data_.has_fidcut = fidcutCheck(tmp_prop_LP.y(), ((3.14159265/2.) - local_phi)*(180./3.14159265), ch);
    data_.prop_location[0] = ch->id().region(); data_.prop_location[1] = ch->id().station(); data_.prop_location[2] = ch->id().chamber(); data_.prop_location[3] = ch->id().layer(); data_.prop_location[4] = ch->id().roll();
    if (debug) cout << "prop region:station:chamber:layer:roll " << data_.prop_location[0] << ":" << data_.prop_location[1] << ":"<< data_.prop_location[2] << ":" << data_.prop_location[3] << ":" << data_.prop_location[4] << endl; 
    data_.inner_or_outer_mom = tmp_inner_or_outer_mom;
    if (debug) cout << "prop_localphi_rad:prop_localphi_deg:prop_globalphi_rad: " << data_.prop_localphi_rad << ":" << data_.prop_localphi_deg << ":" << data_.prop_globalphi_rad << endl;
    if (debug) cout << "bunch of data.branches filled" << endl;
  }
}

void ge21analyzer::GEM_rechit_matcher(const GEMEtaPartition* ch, LocalPoint prop_LP, MuonData_GE21& data_){
  float tmp_rechit_GP_x=999999; float tmp_rechit_GP_y=999999; float tmp_rechit_GP_z=999999;
  float tmp_rechit_LP_x=999999; float tmp_rechit_LP_y=999999; float tmp_rechit_LP_z=999999;
  float tmp_rechit_yroll=999999; float tmp_rechit_localphi_rad=999999; float tmp_rechit_localphi_deg=999999;
  bool tmp_has_rechit = false;
  int tmp_rechit_first_strip=999999; int tmp_rechit_CLS=999999; int tmp_rechit_BunchX=999999;
  float tmp_RdPhi = 9999.; float tmp_RdPhi_Corrected=9999; int tmp_rechit_detId=999999;
  float tmp_dPhi = 9999.; float tmp_dPhi_Corrected=9999;
  float tmp_bending_angle = 9999.;
  int tmp_nRecHitsTot = 0; int tmp_nRecHits5 = 0; int tmp_nRecHits2 = 0;
  int tmp_rechit_region = 0; int tmp_rechit_station = 0; int tmp_rechit_chamber = 0; int tmp_rechit_layer = 0; int tmp_rechit_roll = 0;
  int tmp_nRecHitsRpos1L1 = 0; int tmp_nRecHitsRpos1L2 = 0; int tmp_nRecHitsRneg1L1 = 0; int tmp_nRecHitsRneg1L2 = 0;
  for (auto hit = gemRecHits->begin(); hit != gemRecHits->end(); hit++) {
    if ((hit)->geographicalId().det() == DetId::Detector::Muon && (hit)->geographicalId().subdetId() == MuonSubdetId::GEM) {
      GEMDetId gemid((hit)->geographicalId());
      if (gemid.region() == 1) {
        if (gemid.layer() == 1) {tmp_nRecHitsRpos1L1++;}
        if (gemid.layer() == 2) {tmp_nRecHitsRpos1L2++;}
      }
      if (gemid.region() == -1) {
        if (gemid.layer() == 1) {tmp_nRecHitsRneg1L1++;}
        if (gemid.layer() == 2) {tmp_nRecHitsRneg1L2++;}
      }
      if (gemid.station() == ch->id().station() and gemid.chamber() == ch->id().chamber() and gemid.layer() == ch->id().layer() and abs(gemid.roll() - ch->id().roll()) <= 1 and gemid.region() == ch->id().region()) {
        const auto& etaPart = GEMGeometry_->etaPartition(gemid);
        float strip = etaPart->strip(hit->localPosition());
        float stripAngle = etaPart->specificTopology().stripAngle(strip);
        float rechit_y_to_center = etaPart->toGlobal(etaPart->centreOfStrip(etaPart->nstrips()/2)).perp();
        float rechit_y_to_chamber = (GEMGeometry_->chamber(ch->id()))->toLocal(etaPart->toGlobal(etaPart->centreOfStrip(etaPart->nstrips()/2))).y();
        LocalPoint local_to_center((hit)->localPosition().x(), rechit_y_to_center + (hit)->localPosition().y(), 0);
        if (ch->id().station()==2 and ch->id().ring()==1 and fabs((hit)->localPosition().x() - prop_LP.x())<999.0) {
          tmp_nRecHitsTot++;
          if (abs(RdPhi_func(stripAngle, hit, prop_LP.x(), prop_LP.y(), ch)) < 5) {tmp_nRecHits5++;}
          if (abs(RdPhi_func(stripAngle, hit, prop_LP.x(), prop_LP.y(), ch)) < 2) {tmp_nRecHits2++;}
          if (abs(tmp_RdPhi) > abs(RdPhi_func(stripAngle, hit, prop_LP.x(), prop_LP.y(), ch))) {
            tmp_rechit_GP_x = etaPart->toGlobal((hit)->localPosition()).x();
            tmp_rechit_GP_y = etaPart->toGlobal((hit)->localPosition()).y();
            tmp_rechit_GP_z = etaPart->toGlobal((hit)->localPosition()).z();
            tmp_rechit_LP_x = (hit)->localPosition().x();   tmp_rechit_LP_y = rechit_y_to_chamber + (hit)->localPosition().y();    tmp_rechit_LP_z = (hit)->localPosition().z();
            tmp_rechit_yroll = (hit)->localPosition().y();
            float local_phi = local_to_center.phi(); 
            tmp_rechit_localphi_rad = (3.14159265/2.) - local_phi;
            tmp_rechit_localphi_deg = ((3.14159265/2.) - local_phi)*(180./3.14159265);
            tmp_has_rechit = true;
            tmp_rechit_first_strip = (hit)->firstClusterStrip();
            tmp_rechit_CLS = (hit)->clusterSize();
            tmp_rechit_BunchX = (hit)->BunchX();

            if (debug) cout << "cluster size of recHit: " << tmp_rechit_CLS << endl;

            //Calculating the bending angle = CSC segment phi - GEM rechit phi
            if (data_.hasME21) {
              DetId segDetId = ME21_segment->geographicalId();
              const GeomDet* segDet = theTrackingGeometry->idToDet(segDetId);
              float CSC_segment_phi = (segDet->toGlobal(ME21_segment->localPosition())).phi();
              float GEM_hit_phi = (etaPart->toGlobal(hit->localPosition())).phi();
              tmp_bending_angle = CSC_segment_phi - GEM_hit_phi;
              if (debug) cout << "CSC_segment_phi=" << CSC_segment_phi << " GEM_hit_phi=" << GEM_hit_phi << endl;
              if (debug) cout << "Bending Angle = " << tmp_bending_angle << "\tpT = " << data_.muon_pt << endl;
            }
            
            tmp_RdPhi = RdPhi_func(stripAngle, hit, prop_LP.x(), prop_LP.y(), ch);
            tmp_RdPhi_Corrected = tmp_RdPhi;
            tmp_dPhi = tmp_rechit_localphi_rad - data_.prop_localphi_rad; //units of radian
            tmp_dPhi_Corrected = tmp_dPhi;
            if ((gemid.region() == 1 and gemid.chamber()%2 == 1) || (gemid.region() == -1 && gemid.chamber()%2 == 0)) {
              tmp_RdPhi_Corrected = -1.0*tmp_RdPhi_Corrected;
            }
            /*
            if ((gemid.region() == -1 and gemid.chamber()%2 == 1) || (gemid.region() == 1 && gemid.chamber()%2 == 0)) {
              tmp_dPhi_Corrected = -1.0*tmp_dPhi_Corrected;
            }
            comment on sign convention: notice that for the residual calculation in phi we have dphi = rechit_phi - prop_phi.
            Also dphi_corrected is flipped from what rdphi_corrected was. these are because in firmware, the -endcap's phi matches the global phi.
	          */
            if ((gemid.region() == -1 and gemid.chamber()%2 == 0) || (gemid.region() == 1 && gemid.chamber()%2 == 0)) {
              tmp_dPhi_Corrected = -1.0*tmp_dPhi_Corrected;
            }
            /*
            comment on sign convention: according to the Muon Trigger Office (MTO), the -Endcap sign needs to be switched from what was previously done above^.
            slide 6 on this slide points out that the firmware already takes care of some sign convention: https://indico.cern.ch/event/1447286/contributions/6096480/attachments/2914050/5113471/GM@CSC_GEMalignmentOTMB%20-%2021Aug2024.pdf
            so with this new comment the condition above does not need to specify endcap, but keeping it there anyway.
	          */
            tmp_rechit_detId = gemid.region()*(gemid.station()*100 + gemid.chamber());
            tmp_rechit_region = gemid.region();  tmp_rechit_station = gemid.station();
            tmp_rechit_chamber = gemid.chamber();  tmp_rechit_layer = gemid.layer();
            tmp_rechit_roll = gemid.roll();
            if (debug) cout << "rechit_detId:RdPhi:RdPhi_Corrected:dPhi:dPhi_Corrected\t" << tmp_rechit_detId << ":" << tmp_RdPhi << ":" << tmp_RdPhi_Corrected << ":" << tmp_dPhi << ":" << tmp_dPhi_Corrected << endl;
          }
        }
      }
    }
  }
  if (tmp_has_rechit){
    data_.rechit_GP[0] = tmp_rechit_GP_x; data_.rechit_GP[1] = tmp_rechit_GP_y; data_.rechit_GP[2] = tmp_rechit_GP_z;
    data_.rechit_LP[0] = tmp_rechit_LP_x; data_.rechit_LP[1] = tmp_rechit_LP_y; data_.rechit_LP[2] = tmp_rechit_LP_z;
    data_.rechit_yroll = tmp_rechit_yroll;
    data_.rechit_localphi_rad = tmp_rechit_localphi_rad;
    data_.rechit_localphi_deg = tmp_rechit_localphi_deg;
    data_.has_rechit = tmp_has_rechit;
    data_.rechit_first_strip = tmp_rechit_first_strip;
    data_.rechit_CLS = tmp_rechit_CLS;
    data_.rechit_BunchX = tmp_rechit_BunchX;
    data_.RdPhi = tmp_RdPhi;                      data_.dPhi = tmp_dPhi;
    data_.RdPhi_Corrected = tmp_RdPhi_Corrected;  data_.dPhi_Corrected = tmp_dPhi_Corrected;
    data_.rechit_detId = tmp_rechit_detId;
    data_.bending_angle = tmp_bending_angle;
    data_.nRecHitsTot = tmp_nRecHitsTot; data_.nRecHits5 = tmp_nRecHits5; data_.nRecHits2 = tmp_nRecHits2;
    data_.rechit_location[0] = tmp_rechit_region; data_.rechit_location[1] = tmp_rechit_station; data_.rechit_location[2] = tmp_rechit_chamber; data_.rechit_location[3] = tmp_rechit_layer; data_.rechit_location[4] = tmp_rechit_roll;
    data_.nRecHitsRpos1L1 = tmp_nRecHitsRpos1L1; data_.nRecHitsRpos1L2 = tmp_nRecHitsRpos1L2; data_.nRecHitsRneg1L1 = tmp_nRecHitsRneg1L1; data_.nRecHitsRneg1L2 = tmp_nRecHitsRneg1L2;
  }
}

void ge21analyzer::GEM_simhit_matcher(const GEMEtaPartition* ch, GlobalPoint prop_GP, MuonData_GE21& data_){
  float tmpDy = 999.; float tmpDr = 999.; int tmpSimCounter = 0;
  float tmp_sim_GP_x; float tmp_sim_GP_y; float tmp_sim_GP_z;
  float tmp_sim_LP_x; float tmp_sim_LP_y; float tmp_sim_LP_z;
  bool has_tmp = false;
  for (const auto& simHit:*gemSimHits.product()){
    GEMDetId gemid((simHit).detUnitId());
    if (gemid.station() == ch->id().station() and gemid.chamber() == ch->id().chamber() and gemid.layer() == ch->id().layer() and abs(gemid.roll() - ch->id().roll()) <= 1 and gemid.region() == ch->id().region()){
      tmpSimCounter++;
      const auto& etaPart = GEMGeometry_->etaPartition(gemid);
      float dy = prop_GP.y() - etaPart->toGlobal(simHit.localPosition()).y();
      float dx = prop_GP.x() - etaPart->toGlobal(simHit.localPosition()).x();
      if (dy < tmpDy) tmpDy = dy;
      if (pow(pow(dy, 2) + pow(dx, 2), 0.5) < tmpDr){
        tmp_sim_GP_x = etaPart->toGlobal(simHit.localPosition()).x();
        tmp_sim_GP_y = etaPart->toGlobal(simHit.localPosition()).y();
        tmp_sim_GP_z = etaPart->toGlobal(simHit.localPosition()).z();
        tmp_sim_LP_x = simHit.localPosition().x();
        tmp_sim_LP_y = (GEMGeometry_->chamber(ch->id()))->toLocal(etaPart->toGlobal(etaPart->centreOfStrip(etaPart->nstrips()/2))).y() + simHit.localPosition().y();
        tmp_sim_LP_z = simHit.localPosition().z();
	      tmpDr = pow(pow(dy, 2) + pow(dx, 2), 0.5);
        has_tmp = true;
      }
    }
  }
  if (has_tmp){
    data_.sim_GP[0] = tmp_sim_GP_x; data_.sim_GP[1] = tmp_sim_GP_y; data_.sim_GP[2] = tmp_sim_GP_z;
    data_.sim_LP[0] = tmp_sim_LP_x; data_.sim_LP[1] = tmp_sim_LP_y; data_.sim_LP[2] = tmp_sim_LP_z;
    data_.simDy = tmpDy;
    data_.nSim = tmpSimCounter;
  }
}

float ge21analyzer::RdPhi_func(float stripAngle, const edm::OwnVector<GEMRecHit, edm::ClonePolicy<GEMRecHit> >::const_iterator rechit, float prop_localx, float prop_localy, const GEMEtaPartition* ch){
  GEMDetId gemid((rechit)->geographicalId());
  const auto& etaPart = GEMGeometry_->etaPartition(gemid); //eta partition of the reconstructed hit location
  const auto& etaPart_ch = GEMGeometry_->etaPartition(ch->id()); //eta partition of the propagated hit location
  float deltay_roll = etaPart_ch->toGlobal(etaPart_ch->centreOfStrip(etaPart_ch->nstrips()/2)).perp() - etaPart->toGlobal(etaPart->centreOfStrip(etaPart->nstrips()/2)).perp(); //global position of the center of the propagated y and subtract the rechit chamber center eta
  if (debug) cout << "prop_localx:prop_localy " << prop_localx << ":" << prop_localy << "\tstripAngle: " << stripAngle << endl;
  return cos(stripAngle) * (prop_localx - (rechit)->localPosition().x()) - sin(stripAngle) * (prop_localy + deltay_roll);
  /*
  RdPhi clarification: The residual calculation is RdPhi = cos(Angle) * delta_x + sin(Angle) * delta_y.
  Mapping of the angle in GEM is clockwise, whereas this equation considers counterclockwise strip angle to be positive.
  Since cosine is an even function, no sign change is needed for the first part of residual calculation.
  But to the second part, for sine being an odd function, we add the minus sign to account for the CW angles. 
   */
}

bool ge21analyzer::fidcutCheck(float local_y, float localphi_deg, const GEMEtaPartition* ch){
  const float fidcut_angle = 1.0;
  const float cut_chamber = 5.0;
  const float cut_angle = cut_chamber - fidcut_angle;
  auto& parameters(ch->specs()->parameters());
  float height(parameters[2]);
  if ((abs(localphi_deg) < cut_angle) &&
      ((local_y < (height - cut_chamber) && ch->id().roll() == 1) || 
       (local_y > -1.0*(height - cut_chamber) && ch->id().roll() == 16) ||
       (ch->id().roll() != 1 && ch->id().roll() != 16))
     )
    {return 1;}
  else {return 0;}
}

void ge21analyzer::beginJob(){}
void ge21analyzer::endJob(){
  if (debug) nME21_col_vs_matches->Write();
}

DEFINE_FWK_MODULE(ge21analyzer);
