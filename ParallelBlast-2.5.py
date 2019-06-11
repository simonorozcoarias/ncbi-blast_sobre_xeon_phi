#!/usr/bin/python

__author__ ='LCF'
import os,sys, getopt
from termcolor import colored

### Global Variable definition ###

sequencesFile=''
dataBaseLoc=''
evalue=''
outputFile=''
typePar=''
machinesFile=''
nMach=''
machines = []
fileByNode = []
threadsByNode=[]
numSeq=''
masterHost=''
user=''
userHome=''
refDb=''
job=''
typeBlast=''
analysisType=''
scheme=''
jobSpace=''
splitter='f'
###################################

########## Printing help #############################


def printHelp():

	print colored("\nParallel Blast script allows to deploy a parallel submission of blast using",'white')
	print colored("different parallelization schemes under a shared file system location\n",'white')
	print colored("================================================================================\n",'blue')
        print colored("		Usage: %s" % sys.argv[0],'green')
        print colored("      			-i <Sequences input file>",'cyan')
	print colored("      			-b BlastType <blastx, blastn, blastp>",'cyan')
	print colored("      			-q AnalysisType <prot, nucl>",'cyan')
        print colored("      			-d <Database to compared with>",'cyan')
        print colored("      			-e <evalue> ",'cyan')
        print colored("      			-o <Output filename>",'cyan')
        print colored("      			-t <Parallelization scheme [TP]>",'cyan')
        print colored("      			-m <Machines file>",'cyan')
        print colored("      			-j <Job Directory>",'cyan')
        print colored("      			-p <Splitter Way [f|l|s|p]>",'cyan')
	print("\n")
	print colored("      	Utilities: \n",'green')
	print colored("      		1. Create Blast-compliant database use:\n",'white')
	print colored("             		%s -c"% sys.argv[0],'cyan')
	print("\n")
	print colored("      		2. Show error table (Useful for debugging):\n",'white')
	print colored("             		%s -w"% sys.argv[0],'cyan')
	print("\n")
	print colored("===================================================================================",'blue')
	print colored("Keynotes from Developer:",'green')
	print colored("===================================================================================\n",'blue')
        print("      		1.Machines file must not include FQDN \n")
	print("      		2.It is recommended to put all arguments in current")
	print("                  execution directory  \n")
        print("      		3.Available Parallelization Schemes:\n")
        print colored("        	  TP = Trivial Parallelization\n",'green')
	print colored("	       	  bSP = by-Sequence Parallelization\n",'green')
        print("      		4.Splitters ways:\n")
        print colored("        	  f = FastaSplitter (recommended when all secuences has the same long)\n",'green')
	print colored("	       	  l = LongerSplitter (recommended when secuences has different long)\n",'green')
	print colored("	       	  s = SorterSplitter (recommended when is needed resulting files with different sizes)\n",'green')
	print colored("	       	  p = PhiSplitter (recommended when using CPUs and MIC devices simultaneously)\n",'green')
	print colored("===================================================================================\n",'blue')
	print("If you require more info about the Parallel Schemes available use \n \n     		")+colored("%s -r" % sys.argv[0],'green')
	print("\nFor support contact:")+colored("Leonardo Camargo Forero, M.Sc @ leonardo.camargo@bios.co\n",'green')
        ##print("\n")

######################################################

########## Printing error table #############################

def showParallelSchemes():
        print colored("                         ParallelBlast utilities",'green')
        print colored("=================================================================================\n",'blue')
        print colored("---------------------------------------------------------------------------------",'blue')
        print colored("                          Parallelization Schemes",'cyan')
        print colored("---------------------------------------------------------------------------------\n",'blue')
        print colored("The following table presents information about available Parallelization Schemes",'green')
        print("=================================================================================")
        print colored("Type ",'red')+colored(" Explanation", "blue")
        print("=================================================================================\n")
        print colored(" TP   ",'red')+colored("Trivial Parallelization",'red')+colored(" consists in splitting the input sequences file into",'blue')
        print colored("      smaller pieces with a number of sequences calculated based on the number of",'blue')
        print colored("      machines included in the  machines file. For example if you  have  100K seq",'blue')
	print colored("      and 5 machines, the input sequences file will be splitted into 5 20k-files.",'blue')
	print colored("      Following, each of the 5 files will  be sent to each of the  5 machines and",'blue')
	print colored("      then the selected blast will be launched at each of the nodes over each  of ",'blue')
	print colored("      the 20k files obtaining this way an aproximated 5x performance\n",'blue')
	print("=================================================================================\n")
	print colored(" bSP  ",'red')+colored("by-Sequence Parallelization",'red')+colored(" consists in splitting the  input sequences file",'blue')
        print colored("      into  smaller pieces  with a number of  sequences  calculated based on  the",'blue')
        print colored("      minimum threads available per machine in the  group of machines included in",'blue')
	print colored("      the machines file. For example if you have put 2 nodes in your machine file",'blue')
	print colored("      we calculate the maximum available parallel threads per machine. So,  let's",'blue')
	print colored("      assume we have in  machine1 max 32 parallel  threads and in machine2 max 80",'blue')
	print colored("      parallel threads. Based on  this information, we will take  the minimum, so",'blue')
	print colored("      32 parallel threads. Now, let's assume we have 32K sequences to be treated.",'blue')	
	print colored("      We are  going to split the input  sequences file  into  32-sequences  files",'blue')
	print colored("      having then a total of 1000 32-sequences  files. Following, this pieces are",'blue')
	print colored("      going to be sent to the nodes in increasing order according to  which  node",'blue')
	print colored("      is available or already finished with a 32-sequences file\n",'blue')
		

######################################################

########## Printing error table #############################

def showErrorTable():
	print colored("=================================================================================\n",'blue')
        print colored("           		ParallelBlast utilities",'green')
        print colored("=================================================================================\n",'blue')
	print colored("---------------------------------------------------------------------------------",'blue')
        print colored("               		     Error table:",'red')
        print colored("---------------------------------------------------------------------------------\n",'blue')
        print colored("The following table presents information about code errors and possible solutions",'green')
	print colored("code errors and possible solutions",'green')
	print colored("Use it carefully ",'green')+colored(":P\n",'red')
	print("=================================================================================")
	print colored("Code No.",'red')+colored(" Solution", "blue")
	print("=================================================================================")
	print colored(" 119     ",'red')+colored("If you want to properly run ParallelBlast you must include all arguments",'blue')
	print colored("         (flags) and its  corresponding input. For  example  for -e <evalue>  you",'blue')
	print colored("         must declare a proper numerical evalue (i.e. 0.00001)",'blue')
	print colored(" 129     ",'red')+colored("Analysis  type can  only be  either  prot or nucl. Replace by the proper",'blue')
	print colored("	 option",'blue')
	print colored(" 165     ",'red')+colored("You should input a machines file where you put each node  name (not FQDN)",'blue')
	print colored("         inside your cluster, each one separated by an enter",'blue')
	print colored(" 175     ",'red')+colored("the Job Directory has to exist, please be sure than the path is correct",'blue')
	print colored(" 215     ",'red')+colored("Analysis type and blast type should match. If your analysis is  blastx or",'blue')
        print colored(" 	 blastp i.e. -b  <blastx,blastp>  you should use  -q prot. If  your analy-",'blue')
	print colored("         sis is  blastn i.e. -b blastb use -a nucl",'blue')
	print colored(" 229     ",'red')+colored("You should ONLY input a blastType included in the options blastx, blastn,",'blue')
        print colored("         blastp",'blue')
	print colored(" 456    ",'red')+colored(" You should  copy your blast database to the same location @ each node in-",'blue')
	print colored("         cluded in your machines database or put it in an NFS exported location",'blue')
	print colored(" 465    ",'red')+colored(" You should put at least one node  in  your machines file",'blue')
	print colored(" 545    ",'red')+colored(" One or some of your nodes in the machine file doesn't exist in /etc/hosts",'blue')
	print colored("	 You need to include an alias for the node in this file. i.e.IP FQDN ALIAS",'blue')
	print colored(" 551    ",'red')+colored(" You do not  have  enough sequences   in your  input  sequences file to be",'blue')
	print colored("         splitted in the machines included in the machines  file i.e. you  have  1",'blue')
	print colored("         1 sequence and 2 machines. Rather use sequential blast",'blue')
	print colored(" 552    ",'red')+colored(" You do not  have  enough sequences  in  your  input  sequences file to be",'blue')
	print colored("         splitted in number of threads,for example if you have 15 sequences and 32",'blue')
	print colored("         threads in your machine, you should use TP rather than bSP",'blue')
	print colored(" 554	",'red')+colored(" Evalue must be a numerical value i.e. 0.01",'blue')
	print colored(" 559    ",'red')+colored(" One or more of your nodes seems to be down. Ask the network administrator",'blue')	
	print colored(" 849     ",'red')+colored("If you want to format a proper  blast-compliant database you  must answer",'blue')
	print colored("         all the questions presented",'blue')
	print("=================================================================================")

######################################################

########## Create BlastDB function #############################

def createDB():
	
        print("==================================================\n")
	print("           ParallelBlast utilities")
	print("==================================================\n")
	print("   Utility for blast-compliant database creation ")
	print("__________________________________________________\n")
	print("Please respond the following questions \n")
	seqFilebBlast=raw_input('Path to SequencesFile: ')
	dirDB=os.path.split(os.path.abspath(seqFilebBlast))[0]+"/"
        dbname=os.path.basename(seqFilebBlast)

	dbType=raw_input('Database type (i.e. prot,nucl): ')	
	title=raw_input('Database title: ')
	out=raw_input('Output files naming: ')
	if (not seqFilebBlast)or(not dbType)or(not title)or(not out):
		print("\nERROR Code No. 849 :")
		print("ALL questions must be responded\n")
                sys.exit()
	
	print("\nCreating Blast Database ...\n")
	exeCode=os.system('makeblastdb -in '+dirDB+dbname+' -input_type fasta -dbtype '+dbType+' -title "'+title+'" -parse_seqids -out '+out)
	if(int(exeCode) != 0):
		print("\n__________________________________________________\n")
		print("           makeblastdb thrown an error ")
		print("           Check makeblastdb -h")
		print("\n__________________________________________________\n")
		sys.exit()
	print("\nDatabase created ... done")
	print("\nUse ParallelBlast -h to know how to perform a launching ...")
	print("\nYou need to copy the created database to the same location you have here in the machines you wish to run ParallelBlasy")	
	print("\n_____________________________\n")

	sys.exit()

######################################################

########## Create Job Readme file function #############################


def createReadmeFile():

        os.system('touch '+jobSpace+'/README ')
        os.system('echo "              ParallelBlast Job Info" >> '+jobSpace+'/README ')
        os.system('echo "-----------------------------------------------------" >> '+jobSpace+'/README ')
        os.system('echo "Job ID: '+str(job)+' ">> '+jobSpace+'/README ')
        os.system('echo "Starting date: `date` " >> '+jobSpace+'/README ')
        os.system('echo "User: '+user[0:-1]+' ">> '+jobSpace+'/README ')
        os.system('echo "Job working space: '+jobSpace+' ">> '+jobSpace+'/README ')
        os.system('echo "Sequences file is : '+sequencesFile+' ">> '+jobSpace+'/README ')
	os.system('echo "Blast type is : '+typeBlast+' ">> '+jobSpace+'/README ')
	os.system('echo "Analysis type is : '+analysisType+' ">> '+jobSpace+'/README ')
        os.system('echo "Blast Database to compare with is: '+dataBaseLoc+' ">> '+jobSpace+'/README ')
        os.system('echo "Selected evalue: '+evalue+' ">> '+jobSpace+'/README ')
        os.system('echo "Output file: '+outputFile+' ">> '+jobSpace+'/README ')
        os.system('echo "Parallelization scheme selected: '+scheme+'" >> '+jobSpace+'/README ')

        machinesCat=''
        cCat=1
        for line in machines:
                if(cCat != len(machines)):
                        machinesCat=machinesCat+line[0:-1]+', '
                else:
                        machinesCat=machinesCat+line[0:-1]
                cCat=cCat+1

        os.system('echo "Selected cluster is composed of: '+machinesCat+' ">> '+jobSpace+'/README ')

######################################################


########## Collecting machines #########################

def collectMachines():
	
	global nMach
	global machines
	tempMach=os.popen("cat "+machinesFile+" | wc -l").read()
	nMach=tempMach[0]
	fMach= open(machinesFile,'r')
	for line in fMach:
		machines.append(line)
	if(len(machines)==0):
		print colored("ERROR Code No. 465 :",'red')
                print colored("Machine file is empty",'red')
                sys.exit()
	

######################################################


########## Query threads by node function ###############################

def queryThreadsByNode():

	global threadsByNode
	for line in machines:
		if(line[0:-1] != masterHost[0:-1]):
			threadsByNode.append(int((os.popen('ssh '+line[0:-1]+ ' "cat /proc/cpuinfo | grep processor | tail -1 | cut -d \\" \\" -f2" ').read())[0:-1])+1)
		else:
			threadsByNode.append(int((os.popen('cat /proc/cpuinfo | grep processor | tail -1 | cut -d " " -f2').read())[0:-1])+1)

######################################################

########## Check Parameters function ###############################

def checkParameters():

	#### Checking number of parameters ###############

	print colored("Checking input parameters ",'green')+colored("...",'blue')
	if (not sequencesFile) or (not dataBaseLoc ) or (not evalue) or (not outputFile) or (not typePar) or (not machinesFile) or (not typeBlast) or (not analysisType) or (not jobSpace):
		print colored("ERROR Code No. 119:",'red')
		print colored("All arguments must be included",'red')
		print colored("Check help (use -h flag) !!!",'red')
		print colored("If you need further assistance, use flag -w for Error Table",'red')
		sys.exit()
	else:
		print colored("Input parameters are complete",'green')+colored(" ... done",'blue')

	#################################################

	#### Checking database existence  ###############

######################################################

########## Check Blast Type function ###############################

def checkTypeBlast():

	if (typeBlast != 'blastx') and (typeBlast != 'blastn') and (typeBlast != 'blastp'):
		print colored("ERROR Code No. 229:",'red')
                print colored("Blast type can be only either blastx, blastn, blastp ",'red')
                print colored("Check help (use -h flag) !!!",'red')
                sys.exit()

######################################################

########## Check Analysis Type function ###############################

def checkAnalysisType():

        if (analysisType != 'prot') and (analysisType != 'nucl'):
                print colored("ERROR Code No. 129:",'red')
                print colored("Analysis type can be only either prot or nucl ",'red')
                print colored("Check help (use -h flag) !!!",'red')
                sys.exit()
	if (typeBlast == 'blastx') or (typeBlast == 'blastp'):
		if (analysisType != 'prot'):
			print colored("ERROR Code No. 215:",'red')
        	        print colored("Analysis type and Blast type are not concordant ",'red')
                	print colored("Check help (use -h flag) !!!",'red')
	                sys.exit()
	elif (typeBlast == 'blastn'): 
		if (analysisType != 'nucl'):
                        print colored("ERROR Code No. 215:",'red')
                        print colored("Analysis type and Blast type are not concordant ",'red')
                        print colored("Check help (use -h flag) !!!",'red')
                        sys.exit()

######################################################



########## Check evalue function ###############################

def checkEvalue():
	print colored("Checking evalue",'green')+colored(" ...",'blue')
	try:
		float(evalue)
	except ValueError:
		print colored("ERROR Code No. 554:",'red')
                print colored("Evalue must be a numerical value",'red')
                sys.exit()
	print colored("evalue is ok",'green')+colored(" ... done",'blue')

######################################################



########## Check DataBase Existence function ###############################

def checkDataBase():

	print colored("Checking database existence ",'green')+colored("...",'blue')
	global dataBaseLoc
	dbDirPath=os.path.split(os.path.abspath(dataBaseLoc))[0]+"/"
	dbName=os.path.basename(dataBaseLoc)
	if(dbName==''):
		dbName=os.path.basename(dataBaseLoc[0:-1])
	global refDb
	db=os.popen('ls '+dbDirPath+ ' | grep -x '+dbName).read()
        if (db[0:-1] == dbName):
		if (typeBlast=='blastx') or (typeBlast=='blastp'):
			refDb=(os.popen('basename '+dbDirPath+dbName+'/'+'*.pal .pal').read())[0:-1]
			print refDb
		elif (typeBlast=='blastn'):
			refDb=(os.popen('basename '+dbDirPath+dbName+'/'+'*.nal .nal').read())[0:-1]
	else:
        	print colored("ERROR Code No. 456:",'red')
        	print colored("Database not found",'red')
                sys.exit()
	print colored("Database was found ",'green')+colored("... done","blue")
	
	#################################################

######################################################

########## Check Sequences File function ###############################

def checkSequencesFile():

	global numSeq
	numSeq=os.popen('cat '+sequencesFile+' | grep ">" | wc -l').read()
	print colored("Checking Sequences File ",'green')+colored('...','blue')
	if(int(numSeq[0:-1])==0):
		print colored("ERROR Code No. 165:",'red')
		print colored("Sequences File is empty ",'red')
		sys.exit()
	print colored("Sequences File is not empty ",'green')+colored('... done','blue')

######################################################


########## Check Sequences For TP function ###############################

def checkJobSpace():
	global jobSpace
	print colored("Checking if Job Directory exists ",'green')+colored('...','blue')
	if (os.path.isdir(jobSpace)):
		print colored("Job Directory exists ",'green')+colored('... done','blue')
	else:
		print colored("ERROR Code No. 175:",'red')
                print colored("Jod Directory doesn't exists",'red')
                sys.exit()
	print colored("Checking if Job Directory is an absolut path",'green')+colored('...','blue')
	jobSpaceAb = os.path.abspath(jobSpace)
	if (jobSpace != jobSpaceAb):
		jobSpace = jobSpaceAb
		print colored("Job Directory wasn't absolut path ",'green')+colored('... new Job Directory: '+jobSpace,'blue')
######################################################

########## Check Sequences For TP function ###############################

def checkSeqForPar():

	if (int(numSeq[0:-1]) < int(nMach)):
		print("ERROR Code No. 551:")
		print("There's not enough sequences to be splitted in number of machines  " +nMach)
		sys.exit()


######################################################

########## Check nodes connectivity ###############################

def checkNodes():

	for line in machines:
        	if(line[0:-1] != masterHost[0:-1]):
                	print colored("Checking Node: ",'green')+colored(line[0:-1],'blue')+colored(" connectivity",'green')
			alive=os.system('ping -c 1 '+line[0:-1]+' 1>&2> /dev/null') 
			if(alive == 256) or (alive == 512):
				if(alive == 256):
                			print colored("Node  "+line[0:-1]+" is not responding to ping",'green')
					print colored("I will check once more ....",'green')
					alive=os.system('ping -c 2 '+line[0:-1]+' 1>&2> /dev/null')
					if(alive == 256):
						print colored(".... Node is not responding",'red')
						print colored("ERROR Code No. 559:",'red')
						print colored("Check error table with ParallelBlast -w !!!",'red')
						print colored("Exiting.",'red')
                				sys.exit()		
				else:
					print colored("ERROR Code No. 545:",'red')
                                        print colored("Node:  "+line[0:-1]+" does not exist in your /etc/hosts",'red')
					print colored("Check error table with ParallelBlast -w !!!",'red')
					sys.exit()
			else:
				print colored("Node  ",'green')+colored(line[0:-1],'blue')+colored(" is alive",'green')
		
	

######################################################

########## Parallelization function ###############################


def ParallelBlast():

	print("Parallelization scheme selected ... "+typePar+"\n")
	global scheme
	global jobSpace
	global splitter
	if (typePar == 'TP'):
		scheme="Trivial Parallelization"
	elif (typePar == 'bSP'):
		scheme="by-Sequence Parallelization"
	print("###############################################################\n")
	print("                "+scheme)
	print("###############################################################\n\n")	

	print("Let's start ... \n")
	print("Checking Number of sequences to be treated ..... ")
	checkSeqForPar()
	print("... done ")

	print("Checking Number of sequences to be treated by node (Quantity of ")
	print("nodes is "+nMach+") ..... ")
	if (typePar == 'TP'):
		countFiles=nMach
		numSeqByNode=(int(numSeq[0:-1]))/(int(nMach))
	elif (typePar == 'bSP'):
		threads=threadsByNode
        	threads.sort()
	        numSeqByNode=threads[0]
		countFiles=(int(numSeq[0:-1]))/(int(numSeqByNode))
	print("... done ")

	if(splitter == 'f'):
		if(int(numSeq[0:-1])<int(numSeqByNode)):
			print colored("ERROR Code No. 552 :",'red')
                        print colored("The number of secuences in file ("+str(int(numSeq[0:-1]))+") is less than the number of threads ("+str(numSeqByNode)+"), please use other Parallelization scheme",'red')
                        print colored("Check error table with ParallelBlast -w !!!",'red')
                        sys.exit()
		print("Using utility BIOS-FastaSplitter to split sequences file by num")
		print("ber of machines ......")
		os.popen('python BIOS-FastaSplitter-1.1.py '+str(sequencesFile)+' '+str(numSeqByNode)).read()
		print("... done")
	elif(splitter == 'l'):
		print("Using utility LongerSplitter to split sequences file by long generating "+str(countFiles)+" files")
		os.popen('./LongSplitter.sh -f '+str(sequencesFile)+' -q '+str(sequencesFile)+' -n '+str(countFiles)).read()
		print("... done")
	elif(splitter == 's'):
                print("Using utility SorterSplitter to split sequences file by sorting long generating "+str(countFiles)+" files")
                os.popen('./SorterSplitter.sh -f '+str(sequencesFile)+' -q '+str(sequencesFile)+' -n '+str(countFiles)).read()
                print("... done")
        elif(splitter == 'p'):
                print("Using utility PhiSplitter to split sequences file especially for mics, generating "+str(countFiles)+" files")
                os.popen('./PhiSplitter.sh -f '+str(sequencesFile)+' -q '+str(sequencesFile)+' -m '+machinesFile)
                print("... done")

	print("\n")
	print("Number of sequences to be treated is "+numSeq[0:-1])
	if (typePar == 'TP'):
	
		## General information printed for TP scheme (i.e. files to be splitted and to which node)
		
		print("Number of sequences to be treated by node is "+str(numSeqByNode))
		seqFileLoc=os.path.split(os.path.abspath(sequencesFile))[0]+"/"
		#print ('comando ls '+seqFileLoc+' | grep '+os.path.basename(sequencesFile)+'. > '+seqFileLoc+'splitfile')
        	os.system('ls '+seqFileLoc+' | grep '+os.path.basename(sequencesFile)+'. > '+seqFileLoc+'splitfile')
        	splittedFiles= open(seqFileLoc+'splitfile','r')
        	global fileByNode
        	con=0
        	print("Files to be splitted into machines are: ")
        	for line in splittedFiles:
                	fileByNode.append(line[0:-1])
                	print("  "+line[0:-1])
                	con=con+1

        	print("\n==========================================================")
        	print("Node             File to Send            Number of Threads")
        	print("==========================================================")
		print con
        	for x in range(0,con):
                	if (machines[x][0:-1]!='titan'):
                        	print (machines[x][0:-1]+'      '+fileByNode[x]+'               '+str(threadsByNode[x]))
                	else:
                        	print (machines[x][0:-1]+'              '+fileByNode[x]+'       '+str(threadsByNode[x]))
	
		###########################################################################################
	
	elif (typePar == 'bSP'):
		
		## General information printed for bSP scheme
	
		threads=threadsByNode
	        threads.sort()
        	minThreads=threads[0]
		print sequencesFile
		print("Number of sequences to be treated by cycle (In each node) is "+str(minThreads))
		print("Calculating number of cycles to be performed  ..... ")
		seqFileLoc=os.path.split(os.path.abspath(sequencesFile))[0]+"/"
		print "ls "+seqFileLoc+" | grep "+os.path.basename(sequencesFile)+". | awk -F. {'print $NF'} | sort -g | tail -1"
        	#numCycles=int((os.popen("ls | grep "+os.path.basename(sequencesFile)+". | awk -F. {'print $NF'} | sort -g | tail -1").read())[0:-1])
        	numCycles=int((os.popen("ls "+seqFileLoc+" | grep "+os.path.basename(sequencesFile)+". | awk -F. {'print $NF'} | sort -g | tail -1").read())[0:-1])
        	print("Number of cycles is  "+str(numCycles))
	
		###########################################################################################


	## Getting user informationnumCycles=int((os.popen("ls | grep "+sequencesFile+". | awk -F. {'print $NF'} | sort -g | tail -1").read())[0:-1])
	
	global user
	global userHome
	user=os.popen('whoami').read()
	userHome= (os.popen('env | grep HOME | grep '+user[0:-1]+' | cut -d \"=\" -f2').read())[0:-1]

	print("\n==========================================================")
	print("Starting "+scheme+" for user "+user[0:-1]+" ...")
	print("==========================================================")


	## Checking Job number and creating Job Space and related info "
	print("Checking Job number ... ")
        
	global job
	# currJob=(os.popen('ls '+userHome+'/Jobs/ParallelBlast | grep Job | cut -d \".\" -f2 | sort -g | tail -1').read())[0:-1]
	currJob=(os.popen('ls '+jobSpace+' | grep Job | cut -d \".\" -f2 | sort -g | tail -1').read())[0:-1]
	if (currJob != ''):
       		job=int(currJob)+1
        else:
       		job="1"
	
	jobSpace=jobSpace+'/Job.'+str(job)
        os.system('mkdir '+jobSpace)

	createReadmeFile() ## Readme file Creation
	print("Job space .. created  ")
	print("Job id is "+str(job))
	print("Job space is "+jobSpace)
	print("For Job info, please check the README file found in the Job space")
        print(".... Done")

	###############################################

	## Copying data to job space in machines file

        print("Copying sequences files to Job Space ....") 
        os.system('mv '+os.path.abspath(sequencesFile)+'.* '+jobSpace+'/')
        print(".... Done")
	

        #################################################



	## Executing Blast under selected Parallel Scheme

        print("Launching Blast under machines .... ")
	## TP 
	
	if (typePar == 'TP'):
                load=''
		con=0
		for line in machines:
			if(line[0:-1].find('mic') == -1 ):
                        	load='module load software/bioinformatics/ncbi-blast;'  
                	else:
                        	load='export LD_LIBRARY_PATH=/BIOS-Share/home/sorozcoa/blast-for-mic/blast-for-phi/ncbi-blast-2.2.30+-src/librerias; export PATH=$PATH:/BIOS-Share/home/sorozcoa/blast-for-mic/blast-for-phi/ncbi-blast-2.2.30+-src/mic/ReleaseMIC/bin;'
                	if(line[0:-1] != masterHost[0:-1]):
                        	os.system('ssh '+line[0:-1]+' "'+load+' '+typeBlast+' -query '+jobSpace+'/'+fileByNode[con]+' -db '+os.path.abspath(dataBaseLoc)+'/'+refDb+' -evalue '+evalue+' -out '+jobSpace+'/'+os.path.basename(outputFile)+'.'+line[0:-1]+' -outfmt 5 -gapopen 11 -gapextend 1 -max_target_seqs 3 -word_size 3 -matrix BLOSUM62 -num_threads '+str(threadsByNode[con])+'" &')
			else:
				os.system(load+' '+typeBlast+' -query '+jobSpace+'/'+fileByNode[con]+' -db '+os.path.abspath(dataBaseLoc)+'/'+refDb+' -evalue '+evalue+' -out '+jobSpace+'/'+os.path.basename(outputFile)+'.'+line[0:-1]+' -outfmt 5 -gapopen 11 -gapextend 1 -max_target_seqs 3 -word_size 3 -matrix BLOSUM62 -num_threads '+str(threadsByNode[con])+' &')
			con=con+1
		print(".... Done")
		#os.system('ControlProcess -p '+typeBlast+' -m '+machinesFile+' -o monitor -d "GatherResults -i '+jobSpace+'/'+os.path.basename(outputFile)+' -m '+machinesFile+' -o '+jobSpace+'/gatoutput -f tab " > '+jobSpace+'/monout ')
		os.system('./ControlProcess -p '+typeBlast+' -m '+machinesFile+' -o monitor -d "sleep 30; cat '+jobSpace+'/'+os.path.basename(outputFile)+'.* >> '+jobSpace+'/JOB.'+str(job)+'.out " ')

	#############################

	## bSP 
	elif (typePar == 'bSP'):
		cycleCount=0
		con=0
		load=''
		## bSP cycle
		while(cycleCount <= numCycles):
			con=0 ## Con is used for discriminating machines within threadsByNode
			## Monitor and launch cycle step
			for line in machines:  
				if(line[0:-1].find('mic') == -1 ):
                                	load='module load software/bioinformatics/ncbi-blast;'
                        	else:
                                	load='export LD_LIBRARY_PATH=/BIOS-Share/home/sorozcoa/blast-for-mic/blast-for-phi/ncbi-blast-2.2.30+-src/librerias; export PATH=$PATH:/BIOS-Share/home/sorozcoa/blast-for-mic/blast-for-phi/ncbi-blast-2.2.30+-src/mic/ReleaseMIC/bin;'
                        	exists=os.system('ls '+jobSpace+'/'+line[0:-1])
				print 'Cycle number: {0} of {1} exists {2}'.format(cycleCount, numCycles, exists)
				## Doesn't the lock exist? 
				if(exists!=0):
					## Create lock 
					os.system('touch '+jobSpace+'/'+line[0:-1])
                        		os.system('echo '+line[0:-1]+" > "+jobSpace+'/'+line[0:-1])
					#########################
					if(line[0:-1] != masterHost[0:-1]):
						#print typeBlast+' -query '+jobSpace+'/'+os.path.basename(sequencesFile)+'.'+str(cycleCount)+' -db '+os.path.abspath(dataBaseLoc)+'/'+refDb+' -evalue '+evalue+' -best_hit_overhang 0.1 -best_hit_score_edge 0.1 -max_target_seqs 3 -out '+jobSpace+'/'+os.path.basename(outputFile)+'.'+str(cycleCount)+' -outfmt 5 -show_gis -num_threads '+str(threadsByNode[con])+'" &'
                                		os.system('ssh '+line[0:-1]+' "'+load+' '+typeBlast+' -query '+jobSpace+'/'+os.path.basename(sequencesFile)+'.'+str(cycleCount)+' -db '+os.path.abspath(dataBaseLoc)+'/'+refDb+' -evalue '+evalue+' -best_hit_overhang 0.1 -best_hit_score_edge 0.1 -max_target_seqs 3 -out '+jobSpace+'/'+os.path.basename(outputFile)+'.'+str(cycleCount)+' -outfmt 5 -show_gis -num_threads '+str(threadsByNode[con])+'" &')
					else:
		                                os.system(load+' '+typeBlast+' -query '+jobSpace+'/'+os.path.basename(sequencesFile)+'.'+str(cycleCount)+' -db '+os.path.abspath(dataBaseLoc)+'/'+refDb+' -evalue '+evalue+' -best_hit_overhang 0.1 -best_hit_score_edge 0.1 -max_target_seqs 3 -out '+jobSpace+'/'+os.path.basename(outputFile)+'.'+str(cycleCount)+' -outfmt 5 -show_gis -num_threads '+str(threadsByNode[con])+' &')
					os.system('./ControlProcess -p '+typeBlast+' -m '+jobSpace+'/'+line[0:-1]+' -o monitor -d " rm -drf '+jobSpace+'/'+line[0:-1]+' " &')
					cycleCount=cycleCount+1
				con=con+1
			 #############################
		#############################

		print("Gathering results from Job "+str(job)+' into File JOB'+str(job)+'.out at location: '+jobSpace+' ...')
		os.system('sleep 30')
		os.system('cat '+jobSpace+'/'+os.path.basename(outputFile)+'.* >> '+jobSpace+'/JOB.'+str(job)+'.out')
		os.system('rm -drf '+jobSpace+'/'+os.path.basename(outputFile)+'.*')
	print('Finishing .... ')
	print('ParallelBlast is done :D')


	############################



	#################################################
	
	


######################################################



########## Main Function  ############################

def main():
	try:
		flags, params = getopt.getopt(sys.argv[1:],"whcri:d:e:o:t:m:b:q:j:p:")
	except getopt.GetoptError as error:
		print (str(error))
		print("Usage: %s -i <Sequences input file> -b TypeBlast <blastx, blastn, blastp> -q AnalysisType <prot,nucl> -d <Database to compared with> -e <evalue> -o <Output filename> -t <Parallelization type [TP]> -m <Machines file>" % sys.argv[0])
		sys.exit(2)
	global sequencesFile
	global dataBaseLoc
	global evalue
	global outputFile
	global typePar
	global machinesFile
	global typeBlast
	global analysisType
	global jobSpace
	global splitter 

	for o, a in flags:
		if o == '-h':
			printHelp()
			sys.exit()
		elif o == '-i':
			sequencesFile=a
		elif o == '-b':
			typeBlast=a
		elif o == '-q':
			analysisType=a
		elif o == '-d':
			dataBaseLoc=a
		elif o == '-e':
			evalue=a
		elif o == '-o':
			outputFile=a
		elif o == '-t':
                        typePar=a
		elif o == '-m':
                        machinesFile=a
		elif o == '-c':
			createDB()
		elif o == '-j':
                        jobSpace=a
		elif o == '-p':
                        splitter=a
		elif o == '-w':
			showErrorTable()
			sys.exit()
		elif o == '-r':
			showParallelSchemes()
			sys.exit()

	global masterHost
	masterHost=os.popen('hostname -a').read()

	print colored("\nChecking if we can procede with Blast launching from "+masterHost[0:-1]+" ....",'green')
	print colored("_________________________________________________________________________________\n",'blue')
	checkParameters()
	checkTypeBlast()
	checkAnalysisType()
	checkEvalue()
	collectMachines()
	checkNodes()
	checkDataBase()	
	checkSequencesFile()
	checkJobSpace()
	
	print colored("\nWe are good to go with Blast launching ",'green')+colored(" ... :D",'blue')
	print colored("_________________________________________________________________________________\n",'blue')
	queryThreadsByNode()
	ParallelBlast()
	


######################################################


if __name__ == "__main__":
	#print("\n")
	print colored("#################################################################################",'blue')
	print colored("#################################################################################\n",'blue')
	print colored("                     	   ParallelBlast V.2.5                   ",'green')
	print colored("                      	     Developed",'blue')+colored(' @BIOS','green')
	print colored("                        by ",'blue')+colored('Leonardo Camargo Forero','green')
	print colored("                         leonardo.camargo@bios.co",'blue')
	print colored("                                  2014                    \n",'green')
	print colored("                      	     Modified",'blue')+colored(' @BIOS','green')
	print colored("                        by ",'blue')+colored('Simon Orozco Arias','green')
	print colored("                         simon.orozco@bios.co",'blue')
	print colored("                                  2016                    \n",'green')
	print colored("#################################################################################",'blue')
	main()

