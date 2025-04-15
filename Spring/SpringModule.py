# -*- coding: utf-8 -*-
"""Class Spring defining the whole geometry of the spring. 
   It comes with 2 LCS for positional features"""	

__author__      = "Yves Guillou"
__licence__     = "GPL"

import FreeCAD    as App
import FreeCADGui as Gui
import Sketcher
import Part
from   Spring.SpringDataModule    import DataSet
from   Spring.SpringHelixModule   import Helix
from   Spring.SpringDialogsModule import dialogConfiguration

#####################################################################
class Spring: 
	#########################################################
	##-- CLASS DEFINING THE WHOLE GEOMETRY OF THE SPRING --##
	##--   IT COMES WITH 2 LCS FOR POSITIONAL FEATURES   --##
	######################################################### 
		
	def __init__ (self,data,piece):
		self.piece = piece
		self.GAP = 0.5 # to be clarified. GAP is an offset angle to prevent problems while constructing helix_top 
		Gui.Selection.addSelection(self.piece)
		(data.onLoadHight, data.activeTurnsHight, data.activeTurnsPitch) = dialogConfiguration(data)
		self.helixes(data)
		self.Limits(data)
		data.aspect(data.material)	

	def helixes(self,data):
		#------CLASS VARIABLES TRANSMISSION------#
		Helix.part             = self.piece
		Helix.offsetY          = data.offsetY
		#--BUILDING OF THREE HELIXES INSTANCES--#
		helix_mid    = Helix (data,'MainHelix' , 'MainSketch' , data.activeTurnsPitch , data.activeTurnsHight , data.activeTurnsQty , False)
		helix_bottom = Helix (data,'LowerHelix', 'LowerSketch', data.deadTurnsPitch   , data.deadTurnsHight   , data.deadTurnsQty   , True )
		helix_top    = Helix (data,'UpperHelix', 'UpperSketch', data.deadTurnsPitch   , data.deadTurnsHight   , data.deadTurnsQty   , False, self.GAP)
		#--CREATING UPPER AND LOWER PLANES AND LCS--# 
		
	def Limits(self,data):
		offset = 0.00001
		self.Limit (data,self.piece, 'UpperPlaneSketch', 'UpperPlane', 1, data.onLoadHight-offset , 'Local_Top')
		self.Limit (data,self.piece, 'LowerPlaneSketch', 'LowerPlane', 0, offset                  , 'Local_Bottom')
	
	def Limit (self,data, Doc,sketchName, planeName, reverse, offset, nom_LCS):
		sketchName = Doc.newObject('Sketcher::SketchObject',sketchName).Name
		Doc.getObject(sketchName).Support = App.activeDocument().getObject (Doc.Origin.OriginFeatures[3].Name)
		Doc.getObject(sketchName).MapMode = 'FlatFace'
		Doc.getObject(sketchName).addGeometry (Part.Circle(App.Vector(0,0,0),App.Vector(0,0,1), data.externalDiameter/2*1.2), False)
		Doc.getObject(sketchName).addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
		Doc.getObject(sketchName).AttachmentOffset = App.Placement(App.Vector(0,0,offset), App.Rotation(App.Vector(0,0,1),0))
		######## LCS GENERATION ######################
		LCS                  = Doc.newObject('PartDesign::CoordinateSystem',nom_LCS)
		LCS.AttachmentOffset = Doc.getObject(sketchName).AttachmentOffset			   
		LCS.MapReversed      = False
		LCS.Support          = Doc.getObject(sketchName).Support
		LCS.MapPathParameter = 0.000000
		LCS.MapMode          = 'ObjectXY'
		######## SUBSTRACTIVE PAD GENERATION #########
		limit          = Doc.newObject('PartDesign::Pocket',planeName)
		planeName      = limit.Name	
		limit.Profile  = Doc.getObject(sketchName)
		limit.Length   = data.wireDiameter*2
		limit.Length2  = 100.0
		limit.Type     = 1
		limit.UpToFace = None
		limit.Reversed = reverse
		limit.Midplane = 0
		limit.Offset   = 0
		Doc.getObject(sketchName).Visibility = False
		
	
