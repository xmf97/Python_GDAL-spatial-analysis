from osgeo import ogr
from matplotlib import pyplot as plt
from ospybook.vectorplotter import VectorPlotter
line = ogr.Geometry(ogr.wkbLineString)
line.AddPoint(1111.7655,65432.88)
line.AddPoint(2244.544,87654.86)
line.AddPoint(3216.877,5434.097)
line.AddPoint(5444.766,6559.98)
print(line.ExportToWkt())
vp = VectorPlotter(True)
vp.plot(line,symbol='yellow')
plt.ioff()
plt.show()