import os

#This file will create a tarball and list of condor jobs separated by runs
###########################################################################
#Variables for making condor jobs                #
#filepath = ""                                   #Pathway to the runlist
#runlist = []                                    #List of runs to go over
#cfg_name = ""                                   #Name of cmsRun cfg file ***Make sure to make it work***
#jobname = ""                                    #Name of local folder to put cfg files in
#useMialign = True                               #Use DB bool
#misalign_db = ""                                #What DB file to use
#useStorage = True                               #Whether to local storage or use eos storage
#storage = "/eos/user/d/daebi/"+jobname+"/"      #Where to xrdcp the output root files to
#n_files_per_script = 10                         #Number of run files per condor job
#joblength = "tomorrow"                          #espresso = 20m, microcentury = 1h, longlunch = 2h, workday = 8h, tomorrow = 1d, testmatch = 3d, nextweek = 1w
#releaseName = "CMSSW_12_3_0"                    #This is the name of the tarball and the CMSSW release ***This will only happen if tarball doesn't exist yet***
###########################################################################

#2022B Collision dataset
filepath = "/eos/cms/tier0/store/data/Run2022B/SingleMuon/ALCARECO/MuAlCalIsolatedMu-PromptReco-v1/000/"
runlist = [355094, 355101, 355103, 355105, 355107, 355109, 355111, 355113, 355118, 355120, 355122, 355124, 355128, 355130, 355134, 355181, 355203, 355205, 355207, 355100, 355102, 355104, 355106, 355108, 355110, 355112, 355117, 355119, 355121, 355123, 355127, 355129, 355133, 355135, 355196, 355204, 355206, 355208]
cfg_name = "run_GE11_condor.py"
jobname = "2022B_AllRuns_100722"
useMisalign = False
misalign_db = ""
useStorage = True
storage = "/eos/user/d/daebi/"+jobname+"/"
n_files_per_script = 10
joblength = "tomorrow"
releaseName = "CMSSW_12_4_0"

"""
#List of CRAFT Express Cosmics runs with 690 or 700 uA
filepath = "/eos/cms/store/express/Commissioning2022/ExpressCosmics/FEVT/Express-v1/000/" #CRAFT
runlist = [348773,348776,348777,348838,348908,348955,349016,349073,349078,349079,349084,349146,349147,349260,349263,349348,349422,349433,349435,349436,349437,349527,349528,349611,349703,349758,349833,349834,349839,349840,349893,349963,350010,350107,350142,350166,350174,350254,350294,350361,350424,350425,350431,350450,350459,350460,350462,350463,350464,350490,350491,350561,350619]
#cfg_name = "run_ME11_GE11_condor.py"
cfg_name = "run_GE11_condor.py"
jobname = "GE11_6dof_GT_noYcap_020722"
useMisalign = True #NEED TO CHANGE THE CFG FILE TOO!!!
misalign_db = "GE11_6dof_GT_noYcap.db"
useStorage = True
storage = "/eos/user/d/daebi/"+jobname+"/"
n_files_per_script = 50
joblength = "tomorrow" #espresso = 20m, microcentury = 1h, longlunch = 2h, workday = 8h, tomorrow = 1d, testmatch = 3d, nextweek = 1w
releaseName = "CMSSW_12_4_0"
"""

"""
#Hyunyong asked to check the CSC tbma analyzer with the ALCARECO dataset -- He said that the statistics were very low
filepath = "/eos/cms/store/data/Commissioning2022/Cosmics/ALCARECO/MuAlGlobalCosmics-PromptReco-v1/000/"
runlist = []
cfg_name = "run_CSC_tbma_condor.py"
jobname = "CSC_tbma_CRAFT_ALCARECO_090622"#"ME11Iter2_GE11Iter1_240522" /eos/cms/store/data/Commissioning2022/Cosmics/ALCARECO/MuAlGlobalCosmics-PromptReco-v1/
useMisalign = False #NEED TO CHANGE THE CFG FILE TOO!!!
misalign_db = ""
useStorage = True
storage = "/eos/user/d/daebi/"+jobname+"/"
n_files_per_script = 10
joblength = "tomorrow" #espresso = 20m, microcentury = 1h, longlunch = 2h, workday = 8h, tomorrow = 1d, testmatch = 3d, nextweek = 1w
releaseName = "CMSSW_12_3_0"
"""


pwd = os.getcwd()+'/'
if useStorage:
  os.system("mkdir -p {storage}".format(storage = storage))
tarBall = releaseName+".tar"
cmsPath = releaseName+"/src"
if not os.path.exists(tarBall):
  print("Creating tarball")
  os.chdir("../../../../../")
  os.system("tar -cf {releaseName}/src/GEMCSCBendingAnalyzer/GEM_Alignment/condor/{tarBall} {releaseName} --exclude={releaseName}/src/GEMCSCBendingAnalyzer/GEM_Alignment/condor --exclude={releaseName}/src/GEMCSCBendingAnalyzer/GEM_Alignment/script --exclude={releaseName}/src/GEMCSCBendingAnalyzer/GEM_Alignment/test --exclude={releaseName}/src/GEMCSCBendingAnalyzer/GEM_Alignment/python".format(releaseName = releaseName, tarBall = tarBall))
  os.chdir("{releaseName}/src/GEMCSCBendingAnalyzer/GEM_Alignment/condor".format(releaseName = releaseName))


#Set up the current folder to be the working space
curr_dir = pwd + jobname + "/"
os.system("mkdir -p {curr_dir}".format(curr_dir = curr_dir))

sub_all_name = "{jobname}/submit_all.sh".format(jobname = jobname)
sub_all = open(sub_all_name, "w")
sub_all.write("#!/bin/bash\n")
sub_all.write("date\n")
sub_all.write("cd "+curr_dir+"\n")
sub_all.write("eval `scramv1 runtime -sh`\n")

ntotal_jobs = 0

#If the runlist is empty, do all runs -- create the runlist ourselves
if len(runlist) == 0:
  for run_p1 in os.listdir(filepath):
    tmp_filepath = filepath+run_p1+"/"
    for run_p2 in os.listdir(tmp_filepath):
      runNumber = int(run_p1 + run_p2)
      runlist.append(runNumber)

print("Runlist = ")
print(runlist)


for run in runlist:
  job_filelist = []
  files_in_script = 0
  runjob_counter = 0

  run_str = str(run)
  run_inputdir = filepath + run_str[:3] + "/" + run_str[3:] + "/"
  run_dir = curr_dir + run_str + "/"
  storage_run_dir = storage + run_str + "/"
  os.system("mkdir -p {run_dir}".format(run_dir = run_dir))
  os.system("mkdir -p {run_dir}/output".format(run_dir = run_dir))
  os.system("mkdir -p {run_dir}/error".format(run_dir = run_dir))
  os.system("mkdir -p {run_dir}/log".format(run_dir = run_dir))
  os.system("mkdir -p {run_dir}/scripts".format(run_dir = run_dir))
  os.system("mkdir -p {run_dir}/rootfiles".format(run_dir = run_dir))
  os.system("mkdir -p {storage_run_dir}".format(storage_run_dir = storage_run_dir))

  for subdir in os.listdir(run_inputdir):
    sub_run_inputdir = run_inputdir + subdir + "/"
    for tmp_filename in os.listdir(sub_run_inputdir):
      if ".root" not in tmp_filename: continue
      filename = sub_run_inputdir + tmp_filename

      if files_in_script == 0:
        runjob_counter += 1
        scriptname = run_dir+"scripts/run"+run_str+"_job{njob}.sh".format(njob = runjob_counter)
        c_script = open(scriptname, "w")

      job_filelist.append(filename)
      files_in_script += 1

      if files_in_script == n_files_per_script or (subdir == os.listdir(run_inputdir)[-1] and tmp_filename == os.listdir(sub_run_inputdir)[-1]):
        #print("Got filelist, writing condor script for {nfiles} files".format(nfiles = files_in_script))
        files_in_script = 0

        """
        if useStorage:
          outname = storage_run_dir+"out_run"+run_str+"_job{njob}.root".format(njob = runjob_counter)
        else:
          outname = run_dir+"rootfiles/out_run"+run_str+"_job{njob}.root".format(njob = runjob_counter)
        """
        outname = "out_run"+run_str+"_job{njob}.root".format(njob = runjob_counter)
        filelist = ""
        for fname in job_filelist:
          filelist += "file:" + fname
          if fname != job_filelist[-1]:
            filelist += ","
        c_script.write("#!/bin/bash\n")
        c_script.write("date\n")
        c_script.write("echo $HOME\n")
        c_script.write("export HOME=`pwd`\n")
        c_script.write("export CAFDIR=`pwd`\n")
        c_script.write("python --version\n")

        c_script.write("cd /afs/cern.ch/work/d/daebi/analyser/CMSSW_12_4_0/src/GEMCSCBendingAnalyzer/GEM_Alignment/condor\n")
        c_script.write("cmsenv\n")
        c_script.write("cd $CAFDIR\n")

        c_script.write("tar xf {tarBall}\n".format(tarBall = tarBall))
        c_script.write("ls\n")
        c_script.write("cd {cmsPath}\n".format(cmsPath = cmsPath))
        c_script.write("pwd\n")
        c_script.write("ls /cvmfs/cms.cern.ch/cmsset_default.sh\n")
        c_script.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
        c_script.write("scram build ProjectRename\n")
        c_script.write("eval `scramv1 runtime -sh`\n")
        c_script.write("cd $CAFDIR\n")
        c_script.write("cmsRun {cfg_name} inputFiles={filelist} outputFile={outname}\n".format(filelist = filelist, cfg_name = cfg_name, outname = outname))
        if useStorage:
          c_script.write("xrdcp {outname} {storage_run_dir}{outname}\n".format(outname = outname, storage_run_dir = storage_run_dir))
          c_script.write("rm {outname}\n".format(outname = outname))
          #c_script.write("rm -rf *\n")
        c_script.write("echo 'done'\n")
        c_script.write("date\n")

        job_filelist = []
        os.system("chmod 755 "+scriptname)

        ntotal_jobs += 1
  print("Run " + run_str + " had {njob} total jobs".format(njob = runjob_counter))

  submit_run_name = "{run_dir}/scripts/submit_run{run_str}.sh".format(run_dir = run_dir, run_str = run_str)
  submit_run = open(submit_run_name, "w")

  transfer_input_files = "../../../{tarBall}, ../../../{cfg_name}".format(tarBall = tarBall, cfg_name = cfg_name)
  if useMisalign: transfer_input_files = transfer_input_files + ", ../../../{misalign_db}".format(misalign_db = misalign_db)
  submit_run.write("executable              = $(filename)\n")
  submit_run.write("output                  = {run_dir}/output/$(filename).out\n".format(run_dir = run_dir))
  submit_run.write("error                   = {run_dir}/error/$(filename).err\n".format(run_dir = run_dir))
  submit_run.write("log                     = {run_dir}/log/$(filename).log\n".format(run_dir = run_dir))
  submit_run.write("request_memory          = 4000M\n")
  #submit_run.write("+JobFlavour             = '{joblength}'\n".format(joblength = joblength))
  #Flavour wasn't working, was only getting 20 minutes with 'tomorrow'
  submit_run.write("+MaxRuntime             = 288000\n")
  submit_run.write("universe                = vanilla\n")
  submit_run.write("+AccountingGroup        = 'group_u_CMS.CAF.ALCA'\n")
  submit_run.write("transfer_input_files    = {transfer_input_files}\n".format(transfer_input_files = transfer_input_files))
  if not useStorage:
    submit_run.write("when_to_transfer_output = ON_EXIT\n")
    submit_run.write("should_transfer_files   = YES\n")
  submit_run.write("queue filename matching files run*.sh")


  os.system("chmod 755 "+submit_run_name)

  sub_all.write("echo run {run_str}\n".format(run_str = run_str))
  sub_all.write("cd {run_dir}/scripts/\n".format(run_dir = run_dir))
  sub_all.write("condor_submit {run_dir}/scripts/submit_run{run_str}.sh\n".format(run_dir = run_dir, run_str = run_str))

print("Total jobs made was ", ntotal_jobs)

sub_all.write("echo 'done'\n")
sub_all.write("cd "+curr_dir+"\n")
sub_all.write("date\n")

os.system("chmod 755 "+sub_all_name)

print("Total number of runs was ", len(runlist))
