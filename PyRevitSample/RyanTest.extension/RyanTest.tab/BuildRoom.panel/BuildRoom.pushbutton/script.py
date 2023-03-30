import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
import System.Collections.Generic as Collections

doc = __revit__.ActiveUIDocument.Document

level = FilteredElementCollector(doc).OfClass(Level).FirstElement()
wallType = FilteredElementCollector(doc).OfClass(WallType).FirstElement()
wallWidth = wallType.Width

# Define room size
roomWidth = 10
roomDepth = 10

try:
    # Start a transaction
    t = Transaction(doc, "Create Walls")
    t.Start()

    # Create walls
    wall1 = Wall.Create(doc, Line.CreateBound(XYZ(0, 0, 0), XYZ(roomWidth, 0, 0)), wallType.Id, level.Id, wallWidth, 0, False, False)
    wall2 = Wall.Create(doc, Line.CreateBound(XYZ(roomWidth, 0, 0), XYZ(roomWidth, roomDepth, 0)), wallType.Id, level.Id, wallWidth, 0, False, False)
    wall3 = Wall.Create(doc, Line.CreateBound(XYZ(roomWidth, roomDepth, 0), XYZ(0, roomDepth, 0)), wallType.Id, level.Id, wallWidth, 0, False, False)
    wall4 = Wall.Create(doc, Line.CreateBound(XYZ(0, roomDepth, 0), XYZ(0, 0, 0)), wallType.Id, level.Id, wallWidth, 0, False, False)

    # Convert list of ElementIds to ICollection[ElementId]
    selected_ids = Collections.List[ElementId]([wall1.Id, wall2.Id, wall3.Id, wall4.Id])

    # Commit the transaction
    t.Commit()

    # Set selected element ids
    __revit__.ActiveUIDocument.Selection.SetElementIds(selected_ids)

except Exception as e:
    print(e)

finally:
    if t.HasStarted() and not t.HasEnded():
        t.RollBack()
