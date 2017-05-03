import os.path
from qgis.core import *

def writeToFile(ofile, svg):
	svgFilename = ofile
	output = svg
	file = open(svgFilename, "wb")
	for line in output:
		file.write(line.encode('utf-8'))
	file.close()
	print 'SVG generated, verify it is really genereted, after all, i am a sociologist playing to be a programmer'

def feature2svg(feature, fieldName, doCrsTransform, extentAsPoly, currentExtent):
	geom = feature.geometry()
	id = sanitizeStr(unicode(feature[fieldName]).lower())
	svgGroup = [u'<g id="'+id+'">\n']
	
	if doCrsTransform:
		if hasattr(geom, "transform"):
			geom.transform(crsTransform)
		else:
			print 'problemes amb els sistemes de reprojeccio, intenteu equiparar els crs del projecte i de la capa'
			pass
			
	if geom.wkbType() == QGis.WKBMultiPolygon:
		svgGroup.extend(multiPolygon2path(geom,extentAsPoly,currentExtent))
	elif geom.wkbType() == QGis.WKBPolygon:
		svgGroup.extend(polygon2path(geom, extentAsPoly,currentExtent))
	
	svgGroup.append('</g>\n')

	return svgGroup
	
def multiPolygon2path(geom, extentAsPoly, currentExtent):
	svgPolygon = []
	
	for polygon in geom.asMultiPolygon():
		for ring in polygon:
			svgPath = '<path d="M '
			lastPixel = [0,0]
			coordCount = 0
			insideExtent = False
			
			for point in ring:
				if extentAsPoly.contains(point) or insideExtent == True:
				
					insideExtent = True
					pixpoint = w2p(point.x(),point.y(),iface.mapCanvas().mapUnitsPerPixel(),currentExtent.xMinimum(),currentExtent.yMaximum())
					
					if lastPixel<>pixpoint:
						coordCount += 1
						
						if coordCount > 1:
							svgPath += 'L '
							
						svgPath += (str(pixpoint[0]) + ',' + str(pixpoint[1]) + ' ')
						lastPixel = pixpoint
						
			if insideExtent:
				if coordCount > 2:
					svgPath += '" />\n'
					svgPolygon.extend([svgPath])
		
	return svgPolygon
	
def polygon2path(geom, extentAsPoly, currentExtent):
	svgPolygon = []
	
	for ring in geom.asPolygon():
		svgPath = '<path d="M '
		lastPixel = [0,0]
		coordCount = 0
		insideExtent = False
		
		for point in ring:
			if extentAsPoly.contains(point) or insideExtent == True:
				insideExtent = True
				pixpoint = w2p(point.x(),point.y(),iface.mapCanvas().mapUnitsPerPixel(),currentExtent.xMinimum(),currentExtent.yMaximum())
				if lastPixel<>pixpoint:
					coordCount += 1
					if coordCount > 1:
						svgPath += 'L '
					svgPath += (str(pixpoint[0]) + ',' + str(pixpoint[1]) + ' ')
					lastPixel = pixpoint
					
		if insideExtent:
			if coordCount > 2:
				svgPath += '" />\n'
				svgPolygon.extend([svgPath])
		
	return svgPolygon

def w2p(x, y, mupp, minx, maxy):
	pixX = (x - minx)/mupp
	pixY = (y - maxy)/mupp
	return [round(float(pixX),1), round(float(-pixY),1)]
	
def sanitizeStr(string):
	return string.replace(' ','_').replace('/','_').replace(',','_').replace('.','_')

def runSvgGenerator(ofile, nameField):
	currentExtent = iface.mapCanvas().extent()
	w=iface.mapCanvas().size().width()
	h=iface.mapCanvas().size().height()

	extentAsPoly = QgsGeometry();
	extentAsPoly = QgsGeometry.fromRect(currentExtent);

	fieldName = nameField
	layer = iface.mapCanvas().currentLayer()
	doCrsTransform = False

	svg = [u'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n']
	svg.append(u'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
	svg.append(u'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')
	  
	if hasattr(iface.mapCanvas().mapRenderer(), "destinationSrs"):
		destinationCrs = iface.mapCanvas().mapRenderer().destinationSrs()
		layerCrs = layer.srs()
	else:
		destinationCrs = iface.mapCanvas().mapRenderer().destinationCrs()
		layerCrs = layer.crs()

	if not destinationCrs == layerCrs:
		if iface.mapCanvas().hasCrsTransformEnabled():
			crsTransform = QgsCoordinateTransform(destinationCrs, layerCrs)
			mapCanvasExtent = crsTransform.transformBoundingBox(mapCanvasExtent)
			
		crsTransform = QgsCoordinateTransform(layerCrs, destinationCrs)
		doCrsTransform = True

	for feature in iface.mapCanvas().currentLayer().getFeatures():
		svg.extend(feature2svg(feature, fieldName, doCrsTransform, extentAsPoly, currentExtent))
		
	svg.append(u'</svg>')

	writeToFile(ofile, svg)
	
print "Escolliu un dels seguents camps com a ID; la funcio demana dos parametres: l'ID per una banda i la ruta de l'arxiu per l'altre. Per a executar el codi piqueu runSvgGenerator() i passeu-hi en primer lloc la ruta amb el nom de l'arxiu que voleu generar; i com a segon parametre, l'ID escollit de la llista"

for field in iface.activeLayer().fields():
	print 'name: ' + field.name() + ',  type: ' + field.typeName()