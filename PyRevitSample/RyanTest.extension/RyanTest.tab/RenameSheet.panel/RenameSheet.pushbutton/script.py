import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# get the active document and create a transaction
doc = __revit__.ActiveUIDocument.Document
print("Starting")
t = Transaction(doc, "Rename Sheet")

# start the transaction
t.Start()

# loop through all the sheets in the document
for sheet in FilteredElementCollector(doc).OfClass(ViewSheet):
    if sheet.Name == "evantest":
        # set the new name for the sheet
        sheet.Name = "RYANTEST"
        sheet.SheetNumber = "SOMENEWNUMBER"
        break

# commit the changes and close the transaction
t.Commit()
