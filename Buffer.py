from osgeo import ogr
from ospybook.vectorplotter import VectorPlotter
from matplotlib import pyplot as plt

Point = ogr.Geometry(ogr.wkbPoint)
Line = ogr.Geometry(ogr.wkbLineString)
Line.AddPoint(12,34)
Line.AddPoint(15,56)
Line.AddPoint(34,37)
Point.AddPoint(12,34)
BufferDistance = 50
Poly1 = Point.Buffer(BufferDistance)
Poly2 = Line.Buffer(10)
vp = VectorPlotter(True)
vp.plot(Poly1,symbol='b')
vp.plot(Poly2,symbol='r')
plt.ioff()
plt.show()
