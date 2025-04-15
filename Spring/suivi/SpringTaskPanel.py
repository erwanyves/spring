import FreeCAD,FreeCADGui,Part
import os
import sys
 
#macroPath, macroFilename =os.path.split(__file__)
#modulePath= macropath + "/Spring"
#uiTaskPanel = "interface_choix_action.ui"
 
class TaskPanel:
   def __init__(self):
       modulePath, macroFilename =os.path.split(__file__)
       
       uiTaskPanel = modulePath+'/interface_choix_action.ui'
       self.form = FreeCADGui.PySideUic.loadUi(uiTaskPanel)
       self.choix = ''
       #a voir si cela ne doit pas être déplacé
       FreeCADGui.Control.showDialog(self)

   def accept(self):
        if self.form.rbCharge.isChecked():
           spring.configuration("sous charge")
           print ("sous charge")      
        elif self.form.rbLibre.isChecked():
           spring.configuration("Longueur libre")
           print ("libre")    
        elif self.form.rbBloc.isChecked():
           spring.configuration("Longueur à bloc")
           print ("A bloc")  
        elif self.form.rbSpecifique.isChecked():
           spring.configuration("Longueur spécifique")
           print ("Spécifique not implemented yet")  
        elif self.form.rbOuvrir.isChecked():
           spring.configuration("Ouvrir fichier de parametres")
           data.openLibreOfficeCalc()
        else:
           self.choix = ""
        
        FreeCADGui.Control.closeDialog()
        
   def exec(self):
       pass

   
if __name__ == "__main__":
   panel = TaskPanel()
   
        
        
