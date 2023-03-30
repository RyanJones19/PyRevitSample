import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
import System.Collections.Generic as Collections
import random
import traceback

doc = __revit__.ActiveUIDocument.Document

level = FilteredElementCollector(doc).OfClass(Level).FirstElement()
wallType = FilteredElementCollector(doc).OfClass(WallType).FirstElement()
wallWidth = wallType.Width

# Define building parameters
num_corners = 6  # change to any number of corners desired
min_width = 10  # minimum building width
max_width = 20  # maximum building width
min_depth = 10  # minimum building depth
max_depth = 20  # maximum building depth

# Create list of corner points
corners = []
for i in range(num_corners):
    x = random.uniform(0, 100)
    y = random.uniform(0, 100)
    z = 0  # set z coordinate to 0 for ground level
    corners.append(XYZ(x, y, z))

try:
    # Start a transaction
    t = Transaction(doc, "Create Walls")
    t.Start()

    # Create walls
    walls = []
    wall_ids = []
    curves = [Line.CreateBound(corners[i], corners[(i+1) % num_corners]) for i in range(num_corners)]
    for i in range(num_corners):
        wall = Wall.Create(doc, curves[i], wallType.Id, level.Id, 10.0, 0.0, False, False)
        walls.append(wall)
        wall_ids.append(wall.Id)

    # Convert list of ElementIds to ICollection[ElementId]
    selected_ids = Collections.List[ElementId](wall_ids)

    # Commit the transaction
    t.Commit()

    # Set selected element ids
    __revit__.ActiveUIDocument.Selection.SetElementIds(selected_ids)

except Exception as e:
    traceback.print_exc()
    print(e)

finally:
    if t.HasStarted() and not t.HasEnded():
        t.RollBack()
