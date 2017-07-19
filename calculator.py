import argparse	
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath, gROOT, TPDF
import ratios
from setTDRStyle import setTDRStyle
gROOT.SetBatch(True)
from helpers import *
from defs import getPlot, Backgrounds, Signals
import math
import os



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

	file = open("Test.tex","w")
	file.write("\\documentclass[12pt,a4paper]{report}\n")
	file.write("\\usepackage[margin=1.1 cm]{geometry} \n")
	file.write("\\begin{document}\n")
	file.write("\\begin{center} \n")
	file.write("\\LARGE CMS\\\\ \n")
	file.write("\\Large Private Work \\\\ \n")
	file.write("\\normalsize \n")
	file.write("Lumi=36.5 $fb^{-1}$\\\\ \n")	
	file.write("$\\sqrt{s}=13$ TeV\\\\ \n")
	file.write("\\end{center} \n")
	file.write("\\vspace{1.5mm}  \n")
	file.write("Values: \\\\ \n")
	file.write("\\begin{table}[H] \n")
	file.write("\\centering \n")
	file.write("\\begin{tabular}{|l|l|l|l|l|} \n")
	file.write("\\hline \n")
	file.write(" LL & UL & Variable & Sample & Events \\\\ \n")
	file.write(" \\hline \\hline \n")
	
	
	eventCounts = totalNumberOfGeneratedEvents("/afs/cern.ch/work/j/jschulte/public/filesM300/mc/")	
	mcFiles = getFilePathsAndSampleNames("/afs/cern.ch/work/j/jschulte/public/filesM300/mc/")
	dataFile = getFilePathsAndSampleNames("/afs/cern.ch/work/j/jschulte/public/filesM300/")
	
	##
	## Calculation of integrals en ratios
	##

	scaleB1=0
	scaleS1=0
	scaleB2=0
	scaleS2=0
	
	## Background processes:

	Back=loadHistoFromFile(mcfiles+"ana_datamc_dy50to120.root",plot.histName,plot.rebin)
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy120to200.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy200to400.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy400to800.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy800to1400.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy1400to2300.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy2300to3500.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy3500to4500.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_dy4500to6000.root",plot.histName,plot.rebin))

	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_ttbar_lep50to500.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_ttbar_lep_500to800.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_ttbar_lep_800to1200.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_ttbar_lep_1200to1800.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_ttbar_lep1800toInf.root",plot.histName,plot.rebin))

	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_tW.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_Wantitop.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_WZ_ext.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_ZZ_ext.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_WWinclusive.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_WW200to600.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_WW600to1200.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_WW1200to2500.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_WW2500.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_Wjets.root",plot.histName,plot.rebin))

	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd80to120.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd120to170.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd170to300.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd300to470.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd470to600.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd600to800.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd800to1000.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd1000to1400.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd1400to1800.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd1800to2400.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd2400to3200.root",plot.histName,plot.rebin))
	Back.Add(loadHistoFromFile(mcfiles+"ana_datamc_qcd3200.root",plot.histName,plot.rebin))
	
	##Signals

	Sign=loadHistoFromFile(mcfiles+"ana_datamc_CITo2Mu_Lam22TeVConLL",plot.histName,plot.rebin)
	Sign.Add(loadHistoFromFile(mcfiles+"ana_datamc_CITo2Mu_Lam22TeVConLR",plot.histName,plot.rebin))
	Sign.Add(loadHistoFromFile(mcfiles+"ana_datamc_CITo2Mu_Lam22TeVConRR",plot.histName,plot.rebin))
	Sign.Add(loadHistoFromFile(mcfiles+"ana_datamc_CITo2Mu_Lam22TeVDesLL",plot.histName,plot.rebin))
	Sign.Add(loadHistoFromFile(mcfiles+"ana_datamc_CITo2Mu_Lam22TeVDesLR",plot.histName,plot.rebin))
	Sign.Add(loadHistoFromFile(mcfiles+"ana_datamc_CITo2Mu_Lam22TeVDesRR",plot.histName,plot.rebin))

	##DY to subract from signal

	SignDY=loadHistoFromFile(DataFile+"ana_datamc_DYTo2Mu_M300",plot.histName,plot.rebin)

	## Integrating

	a = 0;
	b = Back.GetSize()	
	da = Back.GetXaxis().GetBinWidth(a)
	db = Back.GetXaxis().GetBinWidth(b)
	offset= Back.GetXaxis().GetXmin()	

	for x in range (0,b-1):
		a1=a
		b1=b-x
		a2=a+x
		b2=b

		A1= a1*da+offset
		B1= b1*db+offset
		A2= a2*da+offset
		B2= b2*db+offset				


		scaleB1 = Back.Integral(a1, b1)
		scaleB2 = Back.Integral(a2, b2)
				
		scaleS1 = Sign.Integral(a1, b1)
		scaleS2 = Sign.Integral(a2, b2)
		scaleDY1=SignDY.Integral(a1, b1)
		scaleDY2=SignDY.Integral(a2, b2)
		scaleS1=scaleS1-scaleDY1
		scaleS2=scaleS2-scaleDY2

			
		if scaleB1 is not 0:		
			texfile.write(" %d & %d & %s & %s & %f \\\\ \\hline	\n" %(A1,B1,plot.histName,"Background",scaleB1))
		if scaleB2 is not 0:			
			texfile.write(" %d & %d & %s & %s & %f \\\\ \\hline	\n" %(A2,B2,plot.histName,"Background",scaleB2))
		if scaleS1 is not 0:	
			texfile.write(" %d & %d & %s & %s & %f \\\\ \\hline	\n" %(A1,B1,plot.histName,tempSample,scaleS1))
		if scaleS2 is not 0:	
			texfile.write(" %d & %d & %s & %s & %f \\\\ \\hline	\n" %(A2,B2,plot.histName,tempSample,scaleS2))
						
	
	print eventCounts
	
	
	processes = []
	for background	 in args.backgrounds:
		processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
	
	signals = []
	for signal in args.signals:
		signals.append(Process(getattr(Signals,signal),eventCounts))
		
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

	datahist = getDataHist(plot,dataFile)	
	print datahist.GetEntries()
	lumi = 36400
	print "-----"
	stack = TheStack(processes,lumi,plot,mcFiles,file)

	if args.data:
		yMax = datahist.GetBinContent(datahist.GetMaximumBin())
		yMin = 0.1
		xMax = datahist.GetXaxis().GetXmax()
		xMin = datahist.GetXaxis().GetXmin()
	else:	
		yMax = stack.theHistogram.GetBinContent(datahist.GetMaximumBin())
		yMin = 0.1
		xMax = stack.theHistogram.GetXaxis().GetXmax()
		xMin = stack.theHistogram.GetXaxis().GetXmin()	
	print yMax, yMin, xMax, xMin
	if plot.yMax == None:
		if logScale:
			yMax = yMax*1000
		else:
			yMax = yMax*1.5
	
	else: yMax = plot.yMax
	print plot.xMin, plot.xMax
	if not plot.yMin == None:
		yMin = plot.yMin
	if not plot.xMin == None:
		xMin = plot.xMin
	if not plot.xMax == None:
		xMax = plot.xMax
	print yMax, yMin, xMax, xMin
	plotPad.DrawFrame(xMin,yMin,xMax,yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
	
	

 
	drawStack = stack

	if len(args.signals) != 0:
		signalhists = []
		for Signal in signals:
			
			signalhist = Signal.loadHistogram(lumi,mcFiles,plot,file)
			signalhist.SetLineWidth(2)
	#		signalhist.Add(stack.theHistogram)
			signalhist.SetMinimum(0.1)
			signalhist.Draw("samehist")
			signalhists.append(signalhist)	

	 
	

	drawStack.theStack.Draw("samehist")							


	
	

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
	if not os.path.exists("NplotsCI"):
		os.makedirs("NplotsCI")	
	print plot.fileName
	hCanvas.Print("NplotsCI/"+plot.fileName+".png")

	file.write("\\end{tabular} \n")
	file.write("\\caption{The integrated number of events between LL(lower limit) and UL (upper limit).} \n")
	file.write("\\label{tab:data} \n")
	file.write("\\end{table}  \n")

	file.write("\end{document}\n")
	file.close()	

					
if __name__ == "__main__":
	
	
	parser = argparse.ArgumentParser(description='Process some integers.')
	
	parser.Add_argument("-d", "--data", action="store_true", dest="data", default=False,
						  help="plot data points.")
	parser.Add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="plot mc backgrounds.")
	parser.Add_argument("-p", "--plot", dest="plot", nargs=1, default="",
						  help="plot to plot.")
	parser.Add_argument("-n", "--norm", action="store_true", dest="norm", default=False,
						  help="normalize to data.")
	parser.Add_argument("-r", "--ratio", action="store_true", dest="ratio", default=False,
						  help="plot ratio plot")
	parser.Add_argument("-l", "--log", action="store_true", dest="log", default=False,
						  help="plot with log scale for y axis")
	parser.Add_argument("-s", "--signal", dest="signals", action="append", default=[],
						  help="signals to plot.")
	parser.Add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")


	args = parser.parse_args()
	if len(args.backgrounds) == 0:
		args.backgrounds = ["DrellYan","OtherPrompt","NonPrompt"]

	#if len(args.signals) == 0:
	#	args.signals = ["SimplifiedModel_mB_225_mn2_150_mn1_80","CITo2Mu_Lam22TeVConLL"]

	#if len(args.signals) != 0:
	#	args.plotSignal = True

	if args.plot == "":
	        ## Normal plots
 	        #args.plot = ["massPlot","massPlot2","massPlot3"]
		
		## CI plots
		args.plot = ['massPlot']#["dietaPlot","massPlot","massCSPosPlot","massCSNegPlot","etaPlot"]
		
	for plot in args.plot:
		plotObject = getPlot(plot)
		plotDataMC(args,plotObject)
	
