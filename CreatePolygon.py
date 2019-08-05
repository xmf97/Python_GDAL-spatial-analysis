from osgeo import ogr
from matplotlib import pyplot as plt
from ospybook.vectorplotter import VectorPlotter

ring = ogr.Geometry(ogr.wkbLinearRing)
g = ogr.Geometry(ogr.wkbMultiPolygon)
ring.AddPoint(45,78)
ring.AddPoint(23,78)
ring.AddPoint(12,56)
ring.AddPoint(56,24)
polygon = ogr.Geometry(ogr.wkbPolygon)
polygon.AddGeometry(ring)
polygon.CloseRings()
g.AddGeometry(polygon)
vp = VectorPlotter(True)
ring = polygon.GetGeometryRef(0)
for i in range(ring.GetPointCount()):
    ring.SetPoint(i,ring.GetX(i)-5,ring.GetY(i))
g.AddGeometry(polygon)
vp.plot(g,name='Polygon')

plt.ioff()
plt.show()