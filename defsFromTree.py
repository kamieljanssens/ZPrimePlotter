from math import sqrt
import ROOT
from ROOT import TMath
import sys
import copy

#~ from helpersFromTree import Plot

		


				

	
	
'''
List of cross sections in pb
'''	

crossSections = {
"dyInclusive50":5765.4,
"dy50to120":1975,
"dy120to200":19.32,
"dy200to400":2.731,
"dy400to800": 0.241,
"dy800to1400":0.01678,
"dy1400to2300":0.00139,
"dy2300to3500":0.00008948,
"dy3500to4500":0.0000041,
"dy4500to6000":4.56E-7,

"tW":35.6,
"Wantitop":35.6,
"Wjets":61526.7,
"WW200to600":1.385,
"WW600to1200":0.0566,
"WW1200to2500":0.003557,
"WW2500": 0.00005395,
"WWinclusive":12.178,

"WZ":47.13,
"WZ_ext":47.13,
"ZZ_ext":16.523,
"ZZ":16.523,

"ttbar_lep":87.31,
"ttbar_lep50to500":87.31,
"ttbar_lep_500to800":0.32611,
"ttbar_lep_800to1200":0.03265,
"ttbar_lep_1200to1800":0.00305,
"ttbar_lep1800toInf":0.00017,

"qcd50to80":0,
"qcd80to120":2762530,
"qcd120to170":471100,
"qcd170to300":117276,
"qcd300to470":7823,
"qcd470to600":648.2,
"qcd600to800":186.9,
"qcd800to1000":32.293,
"qcd1000to1400":9.4183,
"qcd1400to1800":0.84265,
"qcd1800to2400":0.114943,
"qcd2400to3200":0.00682981,
"qcd3200":0.000165445,

#multiplied by 1.3 (k-factor) since the rest is NNLO and this ones LO.

"CITo2Mu_Lam10TeVConLL":1.3*0.63935,
"CITo2Mu_Lam10TeVConLR":1.3*0.684785,
"CITo2Mu_Lam10TeVConRR":1.3*0.640769,
"CITo2Mu_Lam10TeVDesLL":1.3*0.557603,
"CITo2Mu_Lam10TeVDesLR":1.3*0.576513,
"CITo2Mu_Lam10TeVDesRR":1.3*0.547086,

"CITo2Mu_Lam16TeVConLL":1.3*0.3718,
"CITo2Mu_Lam16TeVConLR":1.3*0.7341,
"CITo2Mu_Lam16TeVConRR":1.3*0.3725,
"CITo2Mu_Lam16TeVDesLL":1.3*0.3739,
"CITo2Mu_Lam16TeVDesLR":1.3*0.7342,
"CITo2Mu_Lam16TeVDesRR":1.3*0.3333,  #### ????

"CITo2Mu_Lam22TeVConLL":1.3*0.3637,
"CITo2Mu_Lam22TeVConLR":1.3*0.7486,
"CITo2Mu_Lam22TeVConRR":1.3*0.3737,
"CITo2Mu_Lam22TeVDesLL":1.3*0.3551,
"CITo2Mu_Lam22TeVDesLR":1.3*0.7283,
"CITo2Mu_Lam22TeVDesRR":1.3*0.3629,

"CITo2Mu_Lam28TeVConLL":1.3*0.3333,  #### ????
"CITo2Mu_Lam28TeVConLR":1.3*0.7333,  #### ????
"CITo2Mu_Lam28TeVConRR":1.3*0.3333,  #### ????
"CITo2Mu_Lam28TeVDesLL":1.3*0.3333,  #### ????
"CITo2Mu_Lam28TeVDesLR":1.3*0.7333,  #### ????
"CITo2Mu_Lam28TeVDesRR":1.3*0.3333,  #### ????

"CITo2Mu_Lam34TeVConLL":1.3*0.3333,  #### ????
"CITo2Mu_Lam34TeVConLR":1.3*0.7333,  #### ????
"CITo2Mu_Lam34TeVConRR":1.3*0.3333,  #### ????
"CITo2Mu_Lam34TeVDesLL":1.3*0.7333,  #### ????
"CITo2Mu_Lam34TeVDesLR":1.3*0.7333,  #### ????
"CITo2Mu_Lam34TeVDesRR":1.3*0.3333,  #### ????

"DYTo2Mu_M300":1.3*0.562538,
}

	
	
	
class Signals:
	
	#class SimplifiedModel_mB_225_mn2_150_mn1_80:
	#	subprocesses = ["SUSY_Simplified_Model_Madgraph_FastSim_T6bblledge_225_150_80_8TeV"]
	#	label 		 = "m_{#tilde{b}} = 225 GeV m_{#tilde{#chi_{0}^{2}}} = 150 GeV"
	#	fillcolor    = ROOT.kWhite
	#	fillstyle = 3315
	#	linecolor    = ROOT.kRed-7
	#	uncertainty	 = 0.
	#	scaleFac     = 1.
	#	additionalSelection = None 	
	class CITo2Mu_Lam10TeVConLL:
		subprocesses = ["CITo2Mu_Lam10TeVConLL"]
		label = "CITo2Mu_Lam10TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kAzure+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVConLR:
		subprocesses = ["CITo2Mu_Lam10TeVConLR"]
		label = "CITo2Mu_Lam10TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVConRR:
		subprocesses = ["CITo2Mu_Lam10TeVConRR"]
		label = "CITo2Mu_Lam10TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVDesLL:
		subprocesses = ["CITo2Mu_Lam10TeVDesLL"]
		label = "CITo2Mu_Lam10TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVDesLR:
		subprocesses = ["CITo2Mu_Lam10TeVDesLR"]
		label = "CITo2Mu_Lam10TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam10TeVDesRR:
		subprocesses = ["CITo2Mu_Lam10TeVDesRR"]
		label = "CITo2Mu_Lam10TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None

	class CITo2Mu_Lam16TeVConLL:
		subprocesses = ["CITo2Mu_Lam16TeVConLL"]
		label = "CITo2Mu_Lam16TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kAzure+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVConLR:
		subprocesses = ["CITo2Mu_Lam16TeVConLR"]
		label = "CITo2Mu_Lam16TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVConRR:
		subprocesses = ["CITo2Mu_Lam16TeVConRR"]
		label = "CITo2Mu_Lam16TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVDesLL:
		subprocesses = ["CITo2Mu_Lam16TeVDesLL"]
		label = "CITo2Mu_Lam16TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVDesLR:
		subprocesses = ["CITo2Mu_Lam16TeVDesLR"]
		label = "CITo2Mu_Lam16TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam16TeVDesRR:
		subprocesses = ["CITo2Mu_Lam16TeVDesRR"]
		label = "CITo2Mu_Lam16TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None

	class CITo2Mu_Lam22TeVConLL:
		subprocesses = ["CITo2Mu_Lam22TeVConLL"]
		label = "CITo2Mu_Lam22TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kAzure+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVConLR:
		subprocesses = ["CITo2Mu_Lam22TeVConLR"]
		label = "CITo2Mu_Lam22TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVConRR:
		subprocesses = ["CITo2Mu_Lam22TeVConRR"]
		label = "CITo2Mu_Lam22TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVDesLL:
		subprocesses = ["CITo2Mu_Lam22TeVDesLL"]
		label = "CITo2Mu_Lam22TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVDesLR:
		subprocesses = ["CITo2Mu_Lam22TeVDesLR"]
		label = "CITo2Mu_Lam22TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam22TeVDesRR:
		subprocesses = ["CITo2Mu_Lam22TeVDesRR"]
		label = "CITo2Mu_Lam22TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None


	class CITo2Mu_Lam28TeVConLL:
		subprocesses = ["CITo2Mu_Lam28TeVConLL"]
		label = "CITo2Mu_Lam28TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kAzure+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVConLR:
		subprocesses = ["CITo2Mu_Lam28TeVConLR"]
		label = "CITo2Mu_Lam28TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVConRR:
		subprocesses = ["CITo2Mu_Lam28TeVConRR"]
		label = "CITo2Mu_Lam28TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVDesLL:
		subprocesses = ["CITo2Mu_Lam28TeVDesLL"]
		label = "CITo2Mu_Lam28TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVDesLR:
		subprocesses = ["CITo2Mu_Lam28TeVDesLR"]
		label = "CITo2Mu_Lam28TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam28TeVDesRR:
		subprocesses = ["CITo2Mu_Lam28TeVDesRR"]
		label = "CITo2Mu_Lam28TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None


	class CITo2Mu_Lam34TeVConLL:
		subprocesses = ["CITo2Mu_Lam34TeVConLL"]
		label = "CITo2Mu_Lam34TeVConLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kAzure+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVConLR:
		subprocesses = ["CITo2Mu_Lam34TeVConLR"]
		label = "CITo2Mu_Lam34TeVConLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kRed-4
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVConRR:
		subprocesses = ["CITo2Mu_Lam34TeVConRR"]
		label = "CITo2Mu_Lam34TeVConRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Con RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kYellow
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVDesLL:
		subprocesses = ["CITo2Mu_Lam34TeVDesLL"]
		label = "CITo2Mu_Lam34TeVDesLL"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LL"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kBlue+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVDesLR:
		subprocesses = ["CITo2Mu_Lam34TeVDesLR"]
		label = "CITo2Mu_Lam34TeVDesLR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des LR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kGreen+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
	class CITo2Mu_Lam34TeVDesRR:
		subprocesses = ["CITo2Mu_Lam34TeVDesRR"]
		label = "CITo2Mu_Lam34TeVDesRR"		#"CI #rightarrow #mu^{+}#mu^{-} #Lambda 10 TeV - Des RR"
		fillcolor = ROOT.kWhite
		fillstyle = 0
		linecolor = ROOT.kMagenta+1
		uncertainty = 0.0
		scaleFac     = 1.	
		additionalSelection = None
		
class DYsignals:

	class DYTo2Mu_M300:
		subprocesses = ["DYTo2Mu_M300"]
		label = "DYTo2Mu_M300"
		fillcolor = ROOT.kAzure+1
		fillstyle = 1001#3315
		linecolor = ROOT.kAzure+1 #ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
		
		
class Backgrounds:
	
        
	class DrellYan:
		subprocesses = ["dy50to120","dy120to200","dy200to400","dy400to800","dy800to1400","dy1400to2300","dy2300to3500","dy3500to4500","dy4500to6000"]
		label = "#gamma/Z #rightarrow #mu^{+}#mu^{-}"
		fillcolor = ROOT.kAzure+1
		fillstyle = 1001#3315
		linecolor = ROOT.kAzure+1 #ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class OtherPrompt:
		subprocesses = ["ttbar_lep50to500","ttbar_lep_500to800","ttbar_lep_800to1200","ttbar_lep_1200to1800","ttbar_lep1800toInf","tW","Wantitop","WZ_ext","ZZ_ext","WWinclusive","WW200to600","WW600to1200","WW1200to2500","WW2500"]
		label = "t#bar{t} + other prompt leptons"
		fillcolor = ROOT.kRed-4
		fillstyle = 1001#3345
		linecolor = ROOT.kRed-4 #ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class NonPrompt:
		subprocesses = ["Wjets","qcd80to120","qcd120to170","qcd170to300","qcd300to470","qcd470to600","qcd600to800","qcd800to1000","qcd1000to1400","qcd1400to1800","qcd1800to2400","qcd2400to3200","qcd2400to3200","qcd3200"]
		label = "non-prompt leptons"
		fillcolor = ROOT.kYellow
		fillstyle = 1001#3385
		linecolor = ROOT.kYellow #ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None

	class DYTo2Mu_M300:
		subprocesses = ["DYTo2Mu_M300"]
		label = "DYTo2Mu_M300"
		fillcolor = ROOT.kAzure+1
		fillstyle = 1001#3315
		linecolor = ROOT.kAzure+1 #ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None


	

# Color definition
#==================
defineMyColors = {
        'Black' : (0, 0, 0),
        'White' : (255, 255, 255),
        'Red' : (255, 0, 0),
        'DarkRed' : (128, 0, 0),
        'Green' : (0, 255, 0),
        'Blue' : (0, 0, 255),
        'Yellow' : (255, 255, 0),
        'Orange' : (255, 128, 0),
        'DarkOrange' : (255, 64, 0),
        'Magenta' : (255, 0, 255),
        'KDEBlue' : (64, 137, 210),
        'Grey' : (128, 128, 128),
        'DarkGreen' : (0, 128, 0),
        'DarkSlateBlue' : (72, 61, 139),
        'Brown' : (70, 35, 10),

        'MyBlue' : (36, 72, 206),
        'MyDarkBlue' : (18, 36, 103),
        'MyGreen' : (70, 164, 60),
        'AnnBlueTitle' : (29, 47, 126),
        'AnnBlue' : (55, 100, 255),
#        'W11AnnBlue' : (0, 68, 204),
#        'W11AnnBlue' : (63, 122, 240),
    }


myColors = {
            'W11ttbar':  855,
            'W11singlet':  854,
            'W11ZLightJets':  401,
            'W11ZbJets':  400,
            'W11WJets':  842,
            'W11Diboson':  920,
            'W11AnnBlue': 856,
            'W11Rare':  630,
            }


def getPlot(name):
	from defsFromTree import plots
	if not name in dir(plots):
		print "unknown plot '%s, exiting'"%name
		sys.exit()
	else:
		return copy.copy(getattr(plots, name))
	
		
class Plot:
	
	histName = "none"
	plotName = "none"
	xaxis   = "none"
	yaxis	= "none"
	cut	= ""
	variable = ""
	xMin = 0
	xMax = 0
	nBins = 0
	binning = []
	yMin 	= 0
	yMax	= 0 
	rebin = 1
	fileName = "none.pdf"
	log = False
	
	def __init__(self,histName,plotName, yRange = None, xRange = None, nBins = 0, xLabel = "", yLabel = "",log=False,rebin = None, binning = [], cuts = "", variable = "", scale = 1.0):
		self.histName=histName
		self.xaxis=xLabel
		self.yaxis=yLabel
		self.nBins = nBins
		self.binning = binning
		self.xMin= None
		self.xMax= None
		self.yMin= None
		self.yMax= None
		self.plotName = plotName
		self.fileName= plotName
		self.cut = cuts
		self.variable = variable
		self.scale = scale
		if rebin != None:
			self.rebin = rebin
		if log:
			self.fileName+"_log" 
		self.log = log

		if yRange != None:
			self.yMin = yRange[0]
			self.yMax = yRange[1]
		if xRange != None:
			self.xMin = xRange[0]
			self.xMax = xRange[1]


class plots:
	

## CI plots
	
	masscut = 300
	scaletemp=1.00

	##mass plots general
	massPlot = Plot("DimuonMassVertexConstrained","CIDiMuonMass_%s"%masscut,xLabel="dimuon mass [GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=50,yLabel="Events/10 GeV", cuts = "scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	massCSPosPlot = Plot("DimuonMassVertexConstrained_CSPos","CIDiMuonMassCSPos_%s"%masscut,xLabel="dimuon mass Pos cos theta*[GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=10,yLabel="Events/10 GeV", cuts = "cos_cs > 0 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	massCSNegPlot = Plot("DimuonMassVertexConstrained_CSNeg","CIDiMuonMassCSNeg_%s"%masscut,xLabel="dimuon mass Neg cos theta*[GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=10,yLabel="Events/10 GeV", cuts = "cos_cs < 0 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
              
	##mass plot bb
	massPlotBB = Plot("DimuonMassVertexConstrained_bb","CIDiMuonMass_bb_%s"%masscut,xLabel="dimuon mass [GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=50,yLabel="Events/50 GeV", cuts = "abs(lep_eta[0]) < 1.2 && abs(lep_eta[1]) < 1.2 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	massCSPosPlotBB = Plot("DimuonMassVertexConstrained_bb_CSPos","CIDiMuonMassCSPos_bb_%s"%masscut,xLabel="dimuon mass Pos cos theta*[GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=10,yLabel="Events/10 GeV", cuts = "abs(lep_eta[0]) < 1.2 && abs(lep_eta[1]) < 1.2 && cos_cs > 0 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	massCSNegPlotBB = Plot("DimuonMassVertexConstrained_bb_CSNeg","CIDiMuonMassCSNeg_bb_%s"%masscut,xLabel="dimuon mass Neg cos theta*[GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=10,yLabel="Events/10 GeV", cuts = "abs(lep_eta[0]) < 1.2 && abs(lep_eta[1]) < 1.2 && cos_cs < 0 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
              
	##mass plot be	
	massPlotBE = Plot("DimuonMassVertexConstrained_be","CIDiMuonMass_be_%s"%masscut,xLabel="dimuon mass [GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=50,yLabel="Events/50 GeV", cuts = "!(abs(lep_eta[0])<1.2 && abs(lep_eta[1])<1.2) && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	massCSPosPlotBE = Plot("DimuonMassVertexConstrained_be_CSPos","CIDiMuonMassCSPos_be_%s"%masscut,xLabel="dimuon mass Pos cos theta*[GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=10,yLabel="Events/10 GeV", cuts = "!(abs(lep_eta[0])<1.2 && abs(lep_eta[1])<1.2) && cos_cs > 0 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	massCSNegPlotBE = Plot("DimuonMassVertexConstrained_be_CSNeg","CIDiMuonMassCSNeg_be_%s"%masscut,xLabel="dimuon mass Neg cos theta*[GeV]",log=True,xRange=[0,3000],nBins = 100,rebin=10,yLabel="Events/10 GeV", cuts = "!(abs(lep_eta[0])<1.2 && abs(lep_eta[1])<1.2) && cos_cs < 0 && scaletemp*dil_mass > %d"%masscut, variable = "dil_mass",scale=scaletemp)
	


	##CosTheta* plot
	CosThetaStarPlot=Plot("CosThetaStarDilepton","CosThetaStarDilepton_%s"%masscut,xLabel="dilepton cos(theta*)[]",log=False,xRange=[-1,1],nBins = 10,rebin=10,yLabel="Events/10", cuts = "scaletemp*dil_mass > %d"%masscut, variable = "cos_cs",scale=scaletemp)

	##Chi plot
	ChiPlot=Plot("ChiDilepton","ChiDilepton_%s"%masscut,xLabel="dilepton chi[]",log=False,xRange=[0,30],nBins = 30,rebin=1,yLabel="Events", cuts = "scaletemp*dil_mass > %d"%masscut, variable = "chi_dilepton",scale=scaletemp)
