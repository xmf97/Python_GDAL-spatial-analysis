from osgeo import ogr
from matplotlib import pyplot as plt
from ospybook.vectorplotter import VectorPlotter
point = ogr.Geometry(ogr.wkbPoint)
point.AddPoint(11.34,63.09)
print(point.ExportToWkt())
x = point.GetX()
y = point.GetY()
vp= VectorPlotter(True)
vp.plot(point,'rs')
plt.title('CreatePoint')
plt.ioff()
plt.show()