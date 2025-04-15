# -*- coding: utf-8 -*-
""" Class DataSet manage the datas of the spring """
__author__      = "Yves Guillou"
__licence__     = "GPL"
import os
import sys
import time
import shutil
import FreeCAD    as App
import FreeCADGui as Gui
import subprocess as sp
from   PySide       import QtGui, QtCore
from   PySide.QtGui import QInputDialog, QWidget, QAbstractButton
from   Spring.SpringDialogsModule import dialogCalcExecutableNotFound, dialogCalcNotFound, dialogCopyNew
from   Spring.SpringDialogsModule import dialogInitialSaveAlert      , dialogMissingCsv  , dialogMissingCsvOds
                                         
                                         					 

class DataSet():
	def __init__(self):
		###################
		self.existOds = False
		self.existCsv = False
		###################
		self.missingCsv = False
		self.diameterCoeff =  0.999
		####################################################################
		# self.diameterCoeff reducing the wire diameter to avoid geometrical
		# issues for dead turns and when the spring is at its minimal height
		####################################################################
		self.findLibreOfficeCalcPath()
		if self.locPathFound == True:
			self.newFile  = False
			self.filePath = self.filePath()
			if self.filePath != "" or not self.locPathFound:
				self.pathsSetting()
				if not self.missingCsv :
					if ((self.existCsv or self.existOds) and self.findSpring()) or self.newFile :
						self.initReading()
						self.readDatas()
						self.datasFormatting()
				
	def findLibreOfficeCalcPath(self):
		my_os = sys.platform
		self.osType = ''
		self.macroPath , self.macrofilename = os.path.split(__file__)
		self.locFile= self.macroPath+'/pathConfig.csv'
		myFile =open (self.locFile, 'r')
		while self.osType != my_os:
			self.osType, self.osName, self.locPath , null= myFile.readline().split(",") 
		myFile.close()
		self.locPathFound = os.path.exists(self.locPath)
		if self.locPathFound == False:
			dialogCalcExecutableNotFound(self.osType, self.osName)
			
	def findSpring(self):
		try: 
			piece   = App.ActiveDocument.getObject('Spring')
			version = piece.version
			representation = piece.representation
			return True
		except:
			return False 		
	
	def datasFormatting(self):
		if self.leftHanded == 1:
			self.leftHanded = False
		else:
			self.leftHanded = True
		if self.deadTurnsQty <= 0.0001:
			self.deadTurnsQty = 0.00025 * self.wireDiameter
		self.adjustedWireDiameter = self.wireDiameter*self.diameterCoeff
		if self.grinded == 0:
			self.minActiveTurnsHight -= self.wireDiameter
			self.maxActiveTurnsHight -= self.wireDiameter
			self.offsetY = self.adjustedWireDiameter*self.diameterCoeff/2
		else:
			self.offsetY  = 0
		self.activeTurnsHight = self.onLoadHight  - 2 * self.offsetY - 2 * self.deadTurnsHight
		self.deadTurnsPitch   = self.wireDiameter
		self.externalDiameter = self.meanDiameter + self.wireDiameter
		self.deadTurnsHight   = self.deadTurnsQty * self.deadTurnsPitch

	def openLibreOfficeCalc (self): 
		if os.path.exists(self.projetOdsFile):
			sp.Popen(args=[self.locPath,self.projetOdsFile])
		else:
			dialogCalcNotFound()
		
	def readDatas(self):
		try:
			while True:
				parameter, value = self.dataFile.readline().split(';')
				parameter = "self."+parameter.replace ("'","")
				try:
					value = float(value.replace(',','.'))
				except:
					pass
				exec (parameter+" = "+ str(value))
		except:
			self.dataFile.close()
				
	
	def copyNew(self):
		shutil.copyfile(self.macroOdsFile , self.projetOdsFile)
		shutil.copyfile(self.macroCsvFile , self.projetCsvFile)
		shutil.copyfile(self.macroFcsFile , self.projetFcsFile)
		App.ActiveDocument.restore()
		self.dataFile = open(self.datasFile, "r")
		dialogCopyNew()
		self.openLibreOfficeCalc()
		
	def initReading(self):
		try:
			self.dataFile = open(self.datasFile, "r") 
		except:
			self.newFile = True
			for file in (self.projetOdsFile,  self.projetCsvFile,  self.projetFcsFile):
				if os.path.isfile(file):
					os.remove(file)
			self.copyNew()
				
	def getTimeStamp(self, file):
		if file == "CSV":
			timeStampNum = os.path.getmtime(self.projetCsvFile)
		else:
			timeStampNum = os.path.getmtime(self.filePath)
		timeStamp = time.ctime(timeStampNum)
		return timeStampNum 
		
	def pathsSetting(self):
		self.springPath,  self.springName    = os.path.split(self.filePath)
		self.macroOdsFile  = self.macroPath  + '/Spring.ods'
		self.macroCsvFile  = self.macroPath  + '/Spring.csv'
		self.macroFcsFile  = self.macroPath  + '/Spring.FCStd'
		self.materialColor = self.macroPath  + '/SpringMaterialColor.csv'
		self.locFile       = self.macroPath  + '/pathConfig.csv'
		self.projetOdsFile = self.springPath + '/' + self.springName.replace('.FCStd','.ods')
		self.projetCsvFile = self.springPath + '/' + self.springName.replace('.FCStd','.csv')
		self.projetFcsFile = self.springPath + '/' + self.springName
		self.model         = App.ActiveDocument.FileName
		self.datasFile     = self.model.replace ('FCStd','csv')
		#####################################################
		self.existCsv      = os.path.exists(self.projetCsvFile)
		self.existOds      = os.path.exists(self.projetOdsFile)
		self.existsFcs     = os.path.exists(self.projetFcsFile)
		self.missingCsv    = self.existOds and not self.existCsv
	
	def filePath(self):
		name = "Spring"
		try:
			chemin= App.ActiveDocument.FileName
			self.newFile = False
		except:
			name= "Spring"
			self.newFile = True
			App.newDocument(name)
			App.setActiveDocument(name)
			Gui.ActiveDocument = Gui.getDocument(name)
			Gui.activeDocument().activeView().viewDefaultOrientation()
			msgBox=Gui.SendMsgToActiveView("SaveAs")
		if App.ActiveDocument.FileName == "":	
			dialogInitialSaveAlert()
			Gui.SendMsgToActiveView("SaveAs")
		if App.ActiveDocument.FileName == "":   
			App.Console.PrintMessage("macro terminated by user (no target file definition)\n")
		return App.ActiveDocument.FileName	

	def config (self): #only to prevent errors in creation
		pass	
	
	def checkParameter(self, piece, param, typeOf, nameOf, value):
		try:
			piece.addProperty(typeOf , nameOf  ,"","",1)
		except:
			pass
		return value

	def initParameters(self,piece):
		piece.version        = self.checkParameter(piece, "piece.version"       , "App::PropertyFloat" , "version"       , self.getTimeStamp ("CSV"))  
		piece.representation = self.checkParameter(piece, "piece.representation", "App::PropertyString", "representation", self.config)
		piece.matiere        = self.checkParameter(piece, "piece.matiere"       , "App::PropertyString", "matiere"       , self.material)
		piece.spiresExtremes = self.checkParameter(piece, "piece.spiresExtremes", "App::PropertyString", "spiresExtremes", self.extremeTurns)
			
	def aspect(self, material):
		def tupled (myStr):
			myStr   = myStr.replace("(", "").replace(")", "").replace(",", " ")
			myTuple = tuple(list(map(float, myStr.split())))
			return myTuple
		
		matFile = open(self.materialColor, 'r')
		thisMaterial = ""
		while thisMaterial != material or thisMaterial == "UNKNOWN MATERIAL":
			thisMaterial, diffuse, ambient, specular, emissive, shiny , transpar = matFile.readline().split(';')
		Gui.ActiveDocument.ActiveObject.ShapeMaterial   = App.Material(
			DiffuseColor  = tupled(diffuse) , AmbientColor  = tupled(ambient)  ,\
			SpecularColor = tupled(specular), EmissiveColor = tupled(emissive) ,\
			Shininess     = float(shiny)    , Transparency  = float(transpar))
		matFile.close()
			

