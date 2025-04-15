#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 20:28:49 2022
2022-07-07 implémentation coefficient de forme
@author: yves
"""

import xml.etree.cElementTree as ET
           
class Materials ():
    def __init__(self):
        print ("creation bibliothèque materiaux")
        materiau = 'materials.xml'
        self.tree = ET.parse(materiau)
        self.matieres()
        
   
    def diametres (self, diametreMax ):
        root = self.tree.getroot()
        diam = eval(root.findtext ('liste_diametres'))
        listeDiam = list(diam)
        listeDiametres = []
        i=0
        while i< len(listeDiam):
            if listeDiam[i] <= diametreMax:
                listeDiametres.append(listeDiam[i])
            i=i+1
        diametres = tuple (listeDiametres)
        return diametres
 
        
    def matieres (self):    
        root = self.tree.getroot().findall('material')
        self.matieres=[] 
        for child in root:
            mat = Material()
            mat.spjcoef = []
            mat.spjpuis = []
            mat.name         = child.findtext('name')
            mat.moduleG      = float (child.findtext('moduleG'))
            mat.dmax         = float (child.findtext('dmax'))
            mat.travail      = int   (child.findtext('travail'))
            mat.tslbas       = float (child.findtext('taux_service/leger/bas'))
            mat.tslhaut      = float (child.findtext('taux_service/leger/haut'))
            mat.tsmbas       = float (child.findtext('taux_service/moyen/bas'))
            mat.tsmhaut      = float (child.findtext('taux_service/moyen/haut'))
            mat.tssbas       = float (child.findtext('taux_service/severe/bas'))
            mat.tsshaut      = float (child.findtext('taux_service/severe/haut'))
            mat.jointif      = float (child.findtext('taux_maxi_jointif'))
            mat.spjcoef.append(float (child.findtext('taux_spires_jointes/coef1')))
            mat.spjpuis.append(float (child.findtext('taux_spires_jointes/puissance1')))
            mat.spjcoef.append(float (child.findtext('taux_spires_jointes/coef2')))
            mat.spjpuis.append(float (child.findtext('taux_spires_jointes/puissance2')))
            mat.spjcoef.append(float (child.findtext('taux_spires_jointes/coef3')))
            mat.spjpuis.append(float (child.findtext('taux_spires_jointes/puissance3')))
            mat.spjcoef.append(float (child.findtext('taux_spires_jointes/coef4')))
            mat.spjpuis.append(float (child.findtext('taux_spires_jointes/puissance4')))
            mat.diffuse      = eval  (child.findtext('aspect/diffuse'))
            mat.ambient      = eval  (child.findtext('aspect/ambient'))
            mat.emissive     = eval  (child.findtext('aspect/emissive'))
            mat.specular     = eval  (child.findtext('aspect/specular'))
            mat.shininess    = float (child.findtext('aspect/shininess'))
            mat.transparency = float (child.findtext('aspect/transparency'))
            mat.diametres    = self. diametres(mat.dmax)
            self.matieres.append(mat)

            
class Material():
   
    def __init__(self):
        print ('_____________')
        print ("materiau créé")
        
    def getAttrib(self):
        print ('##########  GET ATTRIB  ##########')
        print ("materiau        = " + str (self.name))
        print ("moduleG         = " + str (self.moduleG))
        print ("dmax            = " + str (self.dmax))
        print ("Travail         = " + str (self.travail))
        print ("Tslbas          = " + str (self.tslbas))
        print ("Tslhaut         = " + str (self.tslhaut))
        print ("Tsmbas          = " + str (self.tsmbas))
        print ("Tsmhaut         = " + str (self.tsmhaut))
        print ("Tssbas          = " + str (self.tssbas))
        print ("Tsshaut         = " + str (self.tsshaut))
        print ("Taux jointif    = " + str (self.jointif))
        print ("Coef            = " + str (self.spjcoef))
        print ("Puissance       = " + str (self.spjpuis))
        print ("diffuse         = " + str (self.diffuse))
        print ("ambient         = " + str (self.ambient))
        print ("emissive        = " + str (self.emissive))
        print ("specular        = " + str (self.specular))
        print ("shininess       = " + str (self.shininess))
        print ("transparency    = " + str (self.transparency))
        print ("liste diametres = " + str (self.diametres))
       
        
    def tauxJointes(self, diametre):
        if diametre > self.dmax:
            print("calcul non autorisé pour cette matière dans ce diametre")
        self.tauxSpiresJointes = 0  
        for i in range(len(self.spjcoef)):
            self.tauxSpiresJointes = self.tauxSpiresJointes +\
                self.spjcoef[i] * (diametre ** self.spjpuis[i])
        if self.tauxSpiresJointes > self.jointif:
               self.tauxSpiresJointes = self.jointif
        return self.tauxSpiresJointes  

            
if __name__ == "__main__":        
    bib = Materials()
    print()
    
    
    for i in range(len(bib.matieres)):
        bib.matieres[i].getAttrib()
        print()
        
        print()
    print (bib.matieres[1].name)
    print (bib.matieres[1].tauxJointes(0.5))





