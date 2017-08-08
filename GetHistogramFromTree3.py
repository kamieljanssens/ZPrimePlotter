import argparse	
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath, gROOT, TPDF, TGraph, TFile
import ratios
from setTDRStyle import setTDRStyle
gROOT.SetBatch(True)
from helpersFromTree import *
from defsFromTree import getPlot, Backgrounds, Signals, DYsignals
import math
import os
from array import array



def plotDataMC(args,plot):
	

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	if args.ratio:
		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
		setTDRStyle()		
		plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		plotPad.Draw()	
		ratioPad.Draw()	
		plotPad.cd()
	else:
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()	
		
	colors = createMyColors()	


	
	
	eventCounts = totalNumberOfGeneratedEvents("/afs/cern.ch/work/j/jschulte/public/filesM300New/mc/")	
	mcTrees = readTrees("/afs/cern.ch/work/j/jschulte/public/filesM300New/mc/")
	eventCountsDY=totalNumberOfGeneratedEvents("/afs/cern.ch/work/j/jschulte/public/filesM300New/mc/")
	SignDYTrees = readTrees("/afs/cern.ch/work/j/jschulte/public/filesM300New/mc/")
	dataTrees = readTrees("/afs/cern.ch/work/j/jschulte/public/filesM300New/")

	#print eventCounts
	
	
	processes = []
	for background	 in args.backgrounds:
		processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
	
	signals = []
	for signal in args.signals:
		signals.append(Process(getattr(Signals,signal),eventCounts))

	DYSignals=[]
	for DYsignal in args.DYSignals:
		DYSignals.append(Process(getattr(DYsignals,DYsignal),eventCountsDY))
		
	legend = TLegend(0.475, 0.65, 0.925, 0.925)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	legend.SetTextFont(42)
	#~ legend.SetNColumns(2)

	#legendEta = TLegend(0.15, 0.75, 0.7, 0.9)
	#legendEta.SetFillStyle(0)
	#legendEta.SetBorderSize(0)
	#legendEta.SetTextFont(42)

	

	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.06)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.045)
	latexCMSExtra.SetNDC(True)	
	legendHists = []
	


	legendHistData = ROOT.TH1F()
	if args.data:	
		legend.AddEntry(legendHistData,"Data","pe")	
		#legendEta.AddEntry(legendHistData,"Data","pe")	


	for process in reversed(processes):
		temphist = ROOT.TH1F()
		temphist.SetFillColor(process.theColor)
		temphist.SetFillStyle(process.theStyle)
		temphist.SetLineColor(process.theLineColor)
		legendHists.append(temphist.Clone)
		legend.AddEntry(temphist,process.label,"f")
		#legendEta.AddEntry(temphist,process.label,"f")



	
	if args.signals !=0:
		processesWithSignal = []
		for process in processes:
			processesWithSignal.append(process)
		for Signal in signals:
			processesWithSignal.append(Signal)
			temphist = ROOT.TH1F()
			temphist.SetFillColor(Signal.theColor)
			temphist.SetFillStyle(process.theStyle)
			temphist.SetLineColor(Signal.theLineColor)
			legendHists.append(temphist.Clone)		
			legend.AddEntry(temphist,Signal.label,"l")
			#legendEta.AddEntry(temphist,Signal.label,"l")
	
	


	nEvents=-1

	
	ROOT.gStyle.SetOptStat(0)
	
	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.045)
	intlumi.SetNDC(True)
	intlumi2 = ROOT.TLatex()
	intlumi2.SetTextAlign(12)
	intlumi2.SetTextSize(0.07)
	intlumi2.SetNDC(True)
	scalelabel = ROOT.TLatex()
	scalelabel.SetTextAlign(12)
	scalelabel.SetTextSize(0.03)
	scalelabel.SetNDC(True)
	metDiffLabel = ROOT.TLatex()
	metDiffLabel.SetTextAlign(12)
	metDiffLabel.SetTextSize(0.03)
	metDiffLabel.SetNDC(True)
	chi2Label = ROOT.TLatex()
	chi2Label.SetTextAlign(12)
	chi2Label.SetTextSize(0.03)
	chi2Label.SetNDC(True)
	hCanvas.SetLogy()




	
	plotPad.cd()
	plotPad.SetLogy(0)
	logScale = plot.log
	
	if logScale == True:
		plotPad.SetLogy()

	datahist = getDataHist(plot,dataTrees,fromTree=True)	
	#print datahist.GetEntries()
	lumi = 36400
	#print "-----"
	stack = TheStack(processes,lumi,plot,mcTrees,fromTree=True)

	if args.data:
		yMax = datahist.GetBinContent(stack.theHistogram.GetMaximumBin())
		yMin = 0.1
		xMax = datahist.GetXaxis().GetXmax()
		xMin = datahist.GetXaxis().GetXmin()
	else:	
		yMax = stack.theHistogram.GetBinContent(stack.theHistogram.GetMaximumBin())
		yMin = 0.1
		xMax = stack.theHistogram.GetXaxis().GetXmax()
		xMin = stack.theHistogram.GetXaxis().GetXmin()	
	#print yMax, yMin, xMax, xMin
	if plot.yMax == None:
		if logScale:
			yMax = yMax*1000
		else:
			yMax = yMax*1.5
	
	else: yMax = plot.yMax
	#print plot.xMin, plot.xMax
	if not plot.yMin == None:
		yMin = plot.yMin
	if not plot.xMin == None:
		xMin = plot.xMin
	if not plot.xMax == None:
		xMax = plot.xMax
	#print yMax, yMin, xMax, xMin
	plotPad.DrawFrame(xMin,yMin,xMax,yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
	
	

 
	drawStack = stack
	drawStack.theStack.Draw("samehist")	

	testB=stack.theHistogram
	testtt= testB.Integral(0,testB.GetSize())
	print testtt

	if len(args.signals) != 0:
		signalhists = []
		SignalName = []
		for Signal in signals:
			
			signalhist = Signal.loadHistogramFromTree(lumi,mcTrees,plot)
			signalhist.SetLineWidth(2)
	#		signalhist.Add(stack.theHistogram)
			signalhist.SetMinimum(0.1)
			signalhist.Draw("samehist")
			signalhists.append(signalhist)	
			print Signal.samples, signalhist.Integral(0,signalhist.GetSize())


	if len(args.DYSignals) != 0:
		DYSignalhists = []
		DYSignalName = []
		for DYSignal in DYSignals:
			
			DYSignalhist = DYSignal.loadHistogramFromTree(lumi,mcTrees,plot)
			DYSignalhist.SetLineWidth(2)
	#		DYSignalhist.Add(stack.theHistogram)
			DYSignalhist.SetMinimum(0.1)
			DYSignalhist.Draw("samehist")
			DYSignalhists.append(DYSignalhist)	

	 
	

						


	
	

	datahist.SetMinimum(0.1)
	if args.data:
		datahist.Draw("samep")	


	legend.Draw()


	
	latex.DrawLatex(0.95, 0.96, "%.2f fb^{-1} (13 TeV)"%(lumi/1000,))
	yLabelPos = 0.85
	cmsExtra = "Private Work"
	if not args.data:
		cmsExtra = "#splitline{Private Work}{Simulation}"
		yLabelPos = 0.82	
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	
	if args.ratio:
		try:
			ratioPad.cd()
		except AttributeError:
			print "Plot fails. Look up in errs/failedPlots.txt"
			outFile =open("errs/failedPlots.txt","a")
			outFile.write('%s\n'%plot.filename%("_"+run.label+"_"+dilepton))
			outFile.close()
			plot.cuts=baseCut
			return 1
		ratioGraphs =  ratios.RatioGraph(datahist,drawStack.theHistogram, xMin=xMin, xMax=xMax,title="Data / MC",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=0.25)
		ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
					

	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	if args.ratio:

		ratioPad.RedrawAxis()
	if not os.path.exists("NPlotsCI"):
		os.makedirs("NPlotsCI")	
	#print plot.fileName
	hCanvas.Print("NPlotsCI/"+plot.fileName+"_fromTree.png")



	##
	## Get the histograms
	##

	## Background processes:

	HistoB=stack.theHistogram
	
	##DY to subract from signal
	
	

	for index, DYSignal in enumerate(DYSignals):
	
		if index is 0:
			HistoSDY=DYSignalhists[index]
		else:
			HistoSDY.Add(DYSignalhists[index]) #loadHistoFromFile("/afs/cern.ch/work/j/jschulte/public/filesM300/ana_datamc_DYTo2Mu_M300.root",plot.histName,plot.rebin)

	##Signals

	binningD={"binningMass": [300,500,700,1100,1900,3500], "binningCosThetaStar": [-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1], "binningChi": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]}
	binningDD={"binningMass": [HistoB.GetXaxis().FindBin(300),HistoB.GetXaxis().FindBin(500),HistoB.GetXaxis().FindBin(700),HistoB.GetXaxis().FindBin(1100),HistoB.GetXaxis().FindBin(1900),HistoB.GetXaxis().FindBin(3500)], "binningCosThetaStar": [HistoB.GetXaxis().FindBin(-1),HistoB.GetXaxis().FindBin(-0.8+0.001),HistoB.GetXaxis().FindBin(-0.6),HistoB.GetXaxis().FindBin(-0.4),HistoB.GetXaxis().FindBin(-0.2),HistoB.GetXaxis().FindBin(0),HistoB.GetXaxis().FindBin(0.2),HistoB.GetXaxis().FindBin(0.4),HistoB.GetXaxis().FindBin(0.6),HistoB.GetXaxis().FindBin(0.8),HistoB.GetXaxis().FindBin(1)], "binningChi": [HistoB.GetXaxis().FindBin(0),HistoB.GetXaxis().FindBin(1),HistoB.GetXaxis().FindBin(2),HistoB.GetXaxis().FindBin(3),HistoB.GetXaxis().FindBin(4),HistoB.GetXaxis().FindBin(5),HistoB.GetXaxis().FindBin(6),HistoB.GetXaxis().FindBin(7),HistoB.GetXaxis().FindBin(8),HistoB.GetXaxis().FindBin(9),HistoB.GetXaxis().FindBin(10),HistoB.GetXaxis().FindBin(11),HistoB.GetXaxis().FindBin(12),HistoB.GetXaxis().FindBin(13),HistoB.GetXaxis().FindBin(14),HistoB.GetXaxis().FindBin(15),HistoB.GetXaxis().FindBin(16),HistoB.GetXaxis().FindBin(17),HistoB.GetXaxis().FindBin(18),HistoB.GetXaxis().FindBin(19),HistoB.GetXaxis().FindBin(20),HistoB.GetXaxis().FindBin(21),HistoB.GetXaxis().FindBin(22),HistoB.GetXaxis().FindBin(23),HistoB.GetXaxis().FindBin(24),HistoB.GetXaxis().FindBin(25),HistoB.GetXaxis().FindBin(26),HistoB.GetXaxis().FindBin(27),HistoB.GetXaxis().FindBin(28),HistoB.GetXaxis().FindBin(29),HistoB.GetXaxis().FindBin(30)]}
	print binningDD

	for index, signal in enumerate(signals):
		if not os.path.exists("rootfiles"):
			os.makedirs("rootfiles")
		OutputFile=TFile("rootfiles/"+"%s"%(signal.label)+"_"+"%s"%(plot.histName)+".root","RECREATE")
     		HistoS = signalhists[index]
		SignalName.append(signal.label)


		if "Mass" in plot.histName:
			binning=binningDD["binningMass"]


		if "CosThetaStar" in plot.histName:
			binning=binningDD["binningCosThetaStar"]

		if "Chi" in plot.histName:
			binning=binningDD["binningChi"]

		
		print binning




		newHistoB = TH1F("bkgHist","bkgHist",len(binning)-1,array("f",binning))	
		for index, binBoundary in enumerate(binning):
    			if index < len(binning)-1:
     				newHistoB.SetBinContent(index+1,HistoB.Integral(binBoundary,binning[index+1]-1))


		newHistoS = TH1F("sigHist","sigHist",len(binning)-1,array("f",binning))
		for index, binBoundary in enumerate(binning):
    			if index < len(binning)-1:
     				newHistoS.SetBinContent(index+1,HistoS.Integral(binBoundary,binning[index+1]-1)-HistoSDY.Integral(binBoundary,binning[index+1]-1))

		newHistoD = TH1F("dataHist","dataHist",len(binning)-1,array("f",binning))
		for index, binBoundary in enumerate(binning):
    			if index < len(binning)-1:
     				newHistoD.SetBinContent(index+1,HistoB.Integral(binBoundary,binning[index+1]-1)+HistoS.Integral(binBoundary,binning[index+1]-1)-HistoSDY.Integral(binBoundary,binning[index+1]-1))

		print newHistoB.Integral(0,newHistoB.GetSize()),newHistoS.Integral(0,newHistoS.GetSize()),HistoSDY.Integral(0,newHistoD.GetSize())

		OutputFile.Write()
		OutputFile.Close()

					
if __name__ == "__main__":
	
	
	parser = argparse.ArgumentParser(description='Process some integers.')
	
	parser.add_argument("-d", "--data", action="store_true", dest="data", default=False,
						  help="plot data points.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="plot mc backgrounds.")
	parser.add_argument("-p", "--plot", dest="plot", nargs=1, default="",
						  help="plot to plot.")
	parser.add_argument("-n", "--norm", action="store_true", dest="norm", default=False,
						  help="normalize to data.")
	parser.add_argument("-r", "--ratio", action="store_true", dest="ratio", default=False,
						  help="plot ratio plot")
	parser.add_argument("-l", "--log", action="store_true", dest="log", default=False,
						  help="plot with log scale for y axis")
	parser.add_argument("-s", "--signal", dest="signals", action="append", default=[],
						  help="signals to plot.")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-dy", "--drellyansign", dest="DYSignals", action="append", default=[],
						  help="DYSignals to plot.")


	args = parser.parse_args()
	if len(args.backgrounds) == 0:
		args.backgrounds = ["DrellYan"]

	if len(args.DYSignals) == 0:
		args.DYSignals = ["DYTo2Mu_M300"]

	#if len(args.signals) == 0:
	#	args.signals = ["SimplifiedModel_mB_225_mn2_150_mn1_80","CITo2Mu_Lam22TeVConLL"]

	#if len(args.signals) != 0:
	#	args.plotSignal = True

	if args.plot == "":
	        ## Normal plots
 	        #args.plot = ["massPlot","massPlot2","massPlot3"]
		
		## CI plots
		args.plot = ["massPlot","CosThetaStarPlot","ChiPlot"]#"massPlot","massCSPosPlot","massCSNegPlot","massPlotBB","massCSPosPlotBB","massCSNegPlotBB","massPlotBE","massCSPosPlotBE","massCSNegPlotBE","CosThetaStarPlot"]
		
	for plot in args.plot:
		plotObject = getPlot(plot)
		plotDataMC(args,plotObject)
	
