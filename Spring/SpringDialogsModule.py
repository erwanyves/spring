# -*- coding: utf-8 -*-
""" Dialogs file """

__author__      = "Yves Guillou"
__licence__     = "GPL"

from   PySide import QtGui, QtCore
from   PySide.QtGui import QInputDialog, QWidget, QAbstractButton


def dialogCalcExecutableNotFound(osType, osName):
	msgBox = QtGui.QMessageBox()
	msgBox.setWindowTitle ("Chemin LibreOffice Calc non trouvé") 
	msgBox.setText("<center>Le chemin de l'exécutable LibreOffice Calc"+\
	" n'a pas été trouvé ou est incorrect sur votre système d'exploitation.</center>")
	msgBox.setInformativeText("<center>Editez le fichier <font size = +1><b><font color = 'yellow'>"+\
	"/'macros'</font color>/Spring/pathConfig.csv</b></font size> de votre système: <b>"+\
	osType+ " - "+ osName +"</b> en ajoutant le chemin de votre exécutable LibreOffice Calc "+\
	"(conventions décrites dans le fichier).</center>")
	msgBox.setStandardButtons (msgBox.Ok)
	msgBox.exec_()
		
def dialogCalcNotFound():
	msgBox = QtGui.QMessageBox()
	msgBox.setWindowTitle ("Classeur LibreOffice non trouvé") 
	msgBox.setText("<center>Le classeur pour votre ressort n'a pas été trouvé (supprimé, déplacé ou renommé)."+
	               " Vous pouvez uniquement changer sa représentation.</center>")
	msgBox.setInformativeText("<center>Pour modifier ses paramètres, essayez de retrouver le classeur " +\
			"associé (fichier <font size = +1><b>ods</b>)</font size>.</center>")
	msgBox.setStandardButtons (msgBox.Ok)
	msgBox.exec_()

def dialogCopyNew():
	msgBox=QtGui.QMessageBox()
	msgBox.setWindowTitle ("Initialisation du ressort") 
	msgBox.setText("<center>Les fichiers ODS et CSV ont été créés (paramètres par défaut) dans le répertoire"+\
		" de votre ressort. Modifiez les paramètres de votre ressort dans le tableur et cliquez "+\
		"'Sauver les données'.</center>\n<center>Le fichier CSV est alors mis à jour avec vos paramètres.\n</center>"+\
		"<center>Relancez la macro depuis votre fichier FreeCAD pour actualiser votre modèle.</center>")
	msgBox.setStandardButtons (msgBox.Ok)
	msgBox.exec()
	
def dialogInitialSaveAlert():
	msgBox=QtGui.QMessageBox()
	msgBox.setWindowTitle("Sauvegarde initiale du fichier requise")
	msgBox.setText("<center>En préalable, il vous faut sauver votre fichier</center>"+
	               "<center> dans le répertoire de votre choix</center>")
	msgBox.exec()
	
def dialogMissingCsv():
	msgBox = QtGui.QMessageBox()
	msgBox.setWindowTitle ("Fichier CSV manquant") 
	msgBox.setText("<center>Le fichier de données <font size = +1><b>CSV</b></font size> n'a pas été trouvé."+
	              " Sauvez les données du classeur <font size = +1><b>ODS</b></font size> pour le régénérer" +
	              " puis relancez la macro.</center>")
	msgBox.setStandardButtons (msgBox.Ok)
	msgBox.exec_()
	
def dialogMissingCsvOds():
	msgBox = QtGui.QMessageBox()
	msgBox.setWindowTitle ("Fichiers CSV et ODS absents") 
	msgBox.setText("<center>Les fichiers <font size = +1><b>CSV</b></font size> et <font size = +1><b>ODS</b>"+
		"</font size> n'ont pas été trouvés. La macro n'est pas utilisable sans ces deux fichiers.</center>")
	msgBox.setStandardButtons (msgBox.Ok)
	msgBox.exec_()
	
def dialogConfiguration (data): 
	msgBox =  QtGui.QInputDialog()
	configType = ["Ressort sous charge (par défaut)",
		      "Ressort libre",
		      "Ressort comprimé à bloc"]
	ok = msgBox.getItem(None, "Représentation", 
			  "Choix du mode de représentation du ressort"+
			  "\n Actuellement: "+ data.config.upper(), configType)
	reply = ok[0]
	if   reply   == configType[0] : #"Ressort sous charge (par défaut)":
		hight       = data.onLoadHight			
		turnsHight  = data.activeTurnsHight
		data.config = "Ressort sous charge"
	elif reply   == configType[1] : #"Ressort libre",
		hight       = data.onLoadHight - data.activeTurnsHight + data.maxActiveTurnsHight 
		turnsHight  = data.maxActiveTurnsHight
		data.config = "Ressort libre"
	elif reply   == configType[2] : #"Ressort comprimé à bloc",
		hight       = data.onLoadHight - data.activeTurnsHight + data.minActiveTurnsHight 
		turnsHight  = data.minActiveTurnsHight
		data.config = "Ressort comprimé à bloc"
	else:				#"Représentation par défaut"
		hight       = data.onLoadHight
		turnsHight  = data.activeTurnsHight
		data.config = "Ressort sous charge"
	turnsPitch = turnsHight / data.activeTurnsQty
	return (hight, turnsHight, turnsPitch)	
	
def dialogSpringStatus(data, piece):
	if piece.version != data.getTimeStamp ("CSV"): 
		msg= "<font color = 'orangered'>"+ "n'est pas à jour"+"</font color>"
		buttonText = "Actualiser"
	else:
		msg= "<font color = 'lime'>"+"est à jour"+"</font color>"
		buttonText = "Changer la représentation"
	if data.newFile == False:
		message = "<center>Le ressort <b><font size = +1>" + msg.upper() +\
	          "</font size></b> avec les données du fichier <b>CSV</b>.</center>"
		msgBox = QtGui.QMessageBox()
		msgBox.setWindowTitle ("Actualisation du ressort") 
		msgBox.setText(message)
		msgBox.setInformativeText("<center>"+"Représentation actuelle: <font size = +1><b>"+\
	                        data.config.upper()+ "</b></font size>.</center>")
		msgBox.setStandardButtons(msgBox.Cancel| msgBox.Ok)
		msgBox.button(msgBox.Ok).setText(buttonText)
		msgBox.setDefaultButton(msgBox.Ok)
		QAbstractButton.openLibreOfficeButton =msgBox.addButton('Modifier le classeur', msgBox.ActionRole)
		ret = msgBox.exec_()
		if msgBox.clickedButton() == QAbstractButton.openLibreOfficeButton:  
			return ("open")
		elif ret == msgBox.Ok:
			return("ok")
