import ROOT
import csv
import os

#############################################################
#Script will parse the output files in rootfiles/*.root     #
#to make a list of events that fit a cut defined below.     #
#                                                           #
#You can then run the created cfg file to produce a new     #
#input file only containing those events for easy           #
#event displays.                                            #
#############################################################

make_cfg_file = True          # Make the cfg file to create new reco
make_list_files = False       # Make the individual list.txt files

inputdir = "/eos/cms/store/express/Commissioning2021/ExpressCosmics/FEVT/Express-v1/000/341/343/"

events_full = []

if make_list_files:
  os.system("mkdir -p evt_lists/")
  longlist = open("event_list.txt", "write")
  negL1 = open("RdPhi_0to0p5_R-1_L1.txt", "write")
  negL2 = open("RdPhi_0to0p5_R-1_L2.txt", "write")
  posL1 = open("RdPhi_0to0p5_R1_L1.txt", "write")
  posL2 = open("RdPhi_0to0p5_R1_L2.txt", "write")

pwd = os.getcwd()
filelist = os.listdir(pwd+"/rootfiles")

filelist_new = [x for x in filelist if "out_ana" in x]

print filelist_new
print len(filelist_new)
filecounter = 0

for filename in filelist_new:
  print "File ", filename

  f = ROOT.TFile("rootfiles/"+filename)
  event = f.Get("analyser/MuonData")

  events_only = []
  negativeL1 = []
  negativeL2 = []
  positiveL1 = []
  positiveL2 = []

  for i in event:
    if i.has_prop_CSC == 1 and i.has_rechit_CSC_GE11 and abs(i.RdPhi_CSC_GE11) < 0.5 and i.hasME11:
      if i.prop_region_GE11 == -1:
        if i.prop_layer_GE11 == 1:
          negativeL1.append([i.evtNum, i.lumiBlock])
          events_only.append('341343:{num}'.format(num = i.evtNum))
        if i.prop_layer_GE11 == 2:
          negativeL2.append([i.evtNum, i.lumiBlock])
          events_only.append('341343:{num}'.format(num = i.evtNum))
      if i.prop_region_GE11 == 1:
        if i.prop_layer_GE11 == 1:
          positiveL1.append([i.evtNum, i.lumiBlock])
          events_only.append('341343:{num}'.format(num = i.evtNum))
        if i.prop_layer_GE11 == 2:
          positiveL2.append([i.evtNum, i.lumiBlock])
          events_only.append('341343:{num}'.format(num = i.evtNum))

  print len(negativeL1), " negative L1 events < 0.5 cm"
  print len(negativeL2), " negative L2 events < 0.5 cm"
  print len(positiveL1), " positive L1 events < 0.5 cm"
  print len(positiveL2), " positive L2 events < 0.5 cm"

  if make_list_files:

    if len(negativeL1) != 0:
      with open("evt_lists/{filename}_negative_L1.csv".format(filename = filename[0:-5]), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(negativeL1)
    if len(negativeL2) != 0:
      with open("evt_lists/{filename}_negative_L2.csv".format(filename = filename[0:-5]), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(negativeL2)
    if len(positiveL1) != 0:
      with open("evt_lists/{filename}_positive_L1.csv".format(filename = filename[0:-5]), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(positiveL1)
    if len(positiveL2) != 0:
      with open("evt_lists/{filename}_positive_L2.csv".format(filename = filename[0:-5]), 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(positiveL2)

    if len(negativeL1) != 0 or len(negativeL2) != 0 or len(positiveL1) != 0 or len(positiveL2) != 0:
      filecounter += 1
      longlist.write("File {filecounter}: {filename} \n".format(filecounter = filecounter, filename = filename[8:]))

      longlist.write("Negative L1 : ")
      if len(negativeL1) != 0:
        negL1.write("{filename} \n".format(filename = filename[8:]))
      for item in negativeL1:
        longlist.write("Event: {item}, LumiBlock: {block}; ".format(item = item[0], block = item[1]))
        negL1.write("{item} {block} \n".format(item = item[0], block = item[1]))

      longlist.write("\n")
      longlist.write("\n")

      longlist.write("Negative L2 : ")
      if len(negativeL2) != 0:
        negL2.write("{filename} \n".format(filename = filename[8:]))
      for item in negativeL2:
        longlist.write("Event: {item}, LumiBlock: {block}; ".format(item = item[0], block = item[1]))
        negL2.write("{item} {block} \n".format(item = item[0], block = item[1]))

      longlist.write("\n")
      longlist.write("\n")

      longlist.write("Positive L1 : ")
      if len(positiveL1) != 0:
        posL1.write("{filename} \n".format(filename = filename[8:]))
      for item in positiveL1:
        longlist.write("Event: {item}, LumiBlock: {block}; ".format(item = item[0], block = item[1]))
        posL1.write("{item} {block} \n".format(item = item[0], block = item[1]))

      longlist.write("\n")
      longlist.write("\n")

      longlist.write("Positive L2 : ")
      if len(positiveL2) != 0:
        posL2.write("{filename} \n".format(filename = filename[8:]))
      for item in positiveL2:
        longlist.write("Event: {item}, LumiBlock: {block}; ".format(item = item[0], block = item[1]))
        posL2.write("{item} {block} \n".format(item = item[0], block = item[1]))

  for item in events_only:
    events_full.append(item)
print len(events_full), " total events"

if make_cfg_file:
  disp_cfg = open("display_file.py", "write")
  disp_cfg.write('import os\n')
  disp_cfg.write('import FWCore.ParameterSet.Config as cms\n')
  disp_cfg.write('from FWCore.ParameterSet.VarParsing import VarParsing\n')
  disp_cfg.write('options = VarParsing("analysis")\n')
  disp_cfg.write('options.register ("nEvents",\n')
  disp_cfg.write('                        -1, #Max number of events\n')
  disp_cfg.write('                        VarParsing.multiplicity.singleton,\n')
  disp_cfg.write('                        VarParsing.varType.int,\n')
  disp_cfg.write('                        "Number of events")\n')
  disp_cfg.write('options.parseArguments()\n')
  disp_cfg.write('process = cms.Process("PROCESSNAME")\n')
  disp_cfg.write('process.maxLuminosityBlocks = cms.untracked.PSet(\n')
  disp_cfg.write('               input = cms.untracked.int32(-1)\n')
  disp_cfg.write(')\n')
  disp_cfg.write('process.source = cms.Source("PoolSource",\n')
  disp_cfg.write('                            fileNames = cms.untracked.vstring(options.inputFiles),\n')
  disp_cfg.write('                            eventsToProcess = cms.untracked.VEventRange(*{events_full}),\n'.format(events_full = events_full))
  disp_cfg.write(')\n')
  disp_cfg.write('filelist = os.popen("find {inputdir} -type f |grep root").read().split("\\n")'.format(inputdir = inputdir))
  disp_cfg.write('\n')
  disp_cfg.write('for i in filelist:\n')
  disp_cfg.write('  if "root" not in i: continue\n')
  disp_cfg.write('  process.source.fileNames.append("file:{i}".format(i = i))\n')
  disp_cfg.write('process.out = cms.OutputModule("PoolOutputModule",\n')
  disp_cfg.write('                                outputCommands = cms.untracked.vstring("keep *"),\n')
  disp_cfg.write('                                fileName = cms.untracked.string("output_display.root"),\n')
  disp_cfg.write('                                )\n')
  disp_cfg.write('process.EndPath = cms.EndPath(process.out)')
