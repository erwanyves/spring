# -*- coding: utf-8 -*-
"""Class Helix define simple helixes of the spring"""

import FreeCAD as App
import Part
import Sketcher

class Helix ():
	###################################################
	### Class defining the geometry of the helixes  ###  
	###################################################
	###---GAP PROPORTIONNALITY TO BE INVESTIGATED---###
	###################################################
	
	def __init__ (self, data, name, sketch , pitch, height, turns, reverse, gap = 0):
		if data.leftHanded: #  gap = 0.1° ok with linkstage, and 0.5° on 0.20 - To be clarified
			self.gap = gap 
		else:
			self.gap = -gap	
		self.drawing = self.part.newObject('Sketcher::SketchObject', sketch) 
		self.helix                = self.part.newObject('PartDesign::AdditiveHelix',name) 
		self.draw_sketch (data)
		self.helix.Profile        = self.part.getObject(sketch)
		self.helix.ReferenceAxis  = self.part.getObject(sketch),['V_Axis']
		self.helix.Mode           = 0
		self.helix.Pitch          = pitch
		self.helix.Height         = height
		self.helix.Turns          = turns
		self.helix.LeftHanded     = data.leftHanded
		self.helix.Reversed       = reverse
		self.helix.AllowMultiFace = False
		
	def draw_sketch (self,data):
		self.drawing.Support = self.part.getObject('YZ_Plane'),['']
		self.drawing.MapMode = 'FlatFace'
		self.drawing.addGeometry(Part.Circle(App.Vector((data.meanDiameter / 2), data.deadTurnsHight + data.offsetY,0),\
		App.Vector(0,0,1), (data.adjustedWireDiameter / 2)), False)
		if self.gap!=0:	#gap prevent non solid construction for the top helix. To be worked on. Not clear at this point
			self.drawing.AttachmentOffset = App.Placement(App.Vector(0,data.activeTurnsHight,0),\
			App.Rotation(App.Vector(0,1,0),self.workingHelixAngle(data)+self.gap))
		self.drawing.Visibility = False
		
	def workingHelixAngle(self,data):
		activeTurnsAngle = data.activeTurnsQty % 1 * 360 
		if data.leftHanded: #à gauche
			activeTurnsAngle = - activeTurnsAngle 	
		return activeTurnsAngle	
