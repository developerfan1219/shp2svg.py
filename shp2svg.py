import shapefile

def writeToFile(ofile, svg):
	svgFilename = ofile + '.svg'
	output = svg
	file = open(svgFilename, "wb")
	for line in output:
		file.write(line.encode('utf-8'))
	file.close()
	print 'SVG generat. Verifica que realment es aixi, al cap i a la fi soc un socioleg jugant a programar'
	
def printFields(ifile):
	fieldsList = []
	layer = shapefile.Reader(ifile)
	for field in layer.fields:
		if type(field) is tuple:
			continue
		else:
			fieldsList.append(field[0])
			
	print fieldsList
	print
	print u"Great, once you have tried your id, you have to call runSvgGenerator() method. This function require four parameters: The shapefile field name you want as id; the path to the shp file; the path to the output svg file, and the witdth in pixels of the output file. Parameters must be introduced in the next order: runSvgGenerator(input_file,output_file,id_name,width_pixels)."
		
def feature2svg(feature, fieldNum, extentAsPoly, layerExtent, mupp):
	geom = feature[1]
	id = sanitizeStr(unicode(feature[0][fieldNum],'utf-8').lower())
	svgGroup = [u'<g id="'+id+'">\n']
	
	if len(geom.parts) == 1:
		svgGroup.extend(polygon2path(geom, extentAsPoly,layerExtent, mupp))
	elif len(geom.parts) > 1:
		svgGroup.extend(multiPolygon2path(geom,extentAsPoly,layerExtent, mupp))
	else:
		pass
	
	svgGroup.append('</g>\n')

	return svgGroup
	
def multiPolygon2path(geom, extentAsPoly, layerExtent, mupp):
	svgPolygon = []
	geom.parts.append(len(geom.points))
	poly_list = []
	parts_counter = 0
	
	while parts_counter < len(geom.parts) - 1:
		coord_count = geom.parts[parts_counter]
		no_of_points = abs(geom.parts[parts_counter] - geom.parts[parts_counter + 1])
		part_list = []
		end_point = coord_count + no_of_points
		while coord_count < end_point:
			for coords in geom.points[coord_count:end_point]:
				x, y = coords[0], coords[1]
				poly_coord = [float(x), float(y)]
				part_list.append(poly_coord)
				coord_count = coord_count + 1
		poly_list.append(part_list)
		parts_counter = parts_counter + 1
		
	for ring in poly_list:
		svgPath = '<path d="M '
		lastPixel = [0,0]
		coordCount = 0
	
		for latLng in ring:
			x,y = latLng[0],latLng[1]
			if layerExtent[0] > 0 and layerExtent[2] > 0 or layerExtent[0] > 0 and layerExtent[2] > 0:
				xExtension = abs(layerExtent[0] - layerExtent[2])
				yExtension = abs(layerExtent[1]) + abs(layerExtent[3])
				pixpoint = w2p(x,y,abs(layerExtent[0] - layerExtent[2])/mupp,layerExtent[0],layerExtent[3], xExtension, yExtension)
			else:
				xExtension = abs(layerExtent[0]) + abs(layerExtent[2])
				yExtension = abs(layerExtent[1]) + abs(layerExtent[3])
				pixpoint = w2p(x,y,(abs(layerExtent[0]) + abs(layerExtent[2]))/mupp,layerExtent[0],layerExtent[3], xExtension, yExtension)
				
			if lastPixel<>pixpoint:
				coordCount += 1
				if coordCount > 1:
					svgPath += 'L '
				svgPath += (str(pixpoint[0]) + ',' + str(pixpoint[1]) + ' ')
				lastPixel = pixpoint
		
		if coordCount > 2:
			svgPath += '" />\n'
			svgPolygon.extend([svgPath])

	return svgPolygon
	
def polygon2path(geom, extentAsPoly, layerExtent, mupp):
	svgPolygon = []
	svgPath = '<path d="M '
	lastPixel = [0,0]
	coordCount = 0
	
	for latLng in geom.points:
		x,y = latLng[0],latLng[1]
		if layerExtent[0] > 0 and layerExtent[2] > 0 or layerExtent[0] > 0 and layerExtent[2] > 0:
			xExtension = abs(layerExtent[0] - layerExtent[2])
			yExtension = abs(layerExtent[1]) + abs(layerExtent[3])
			pixpoint = w2p(x,y,abs(layerExtent[0] - layerExtent[2])/mupp,layerExtent[0],layerExtent[3], xExtension, yExtension)
		else:
			xExtension = abs(layerExtent[0]) + abs(layerExtent[2])
			yExtension = abs(layerExtent[1]) + abs(layerExtent[3])
			pixpoint = w2p(x,y,(abs(layerExtent[0]) + abs(layerExtent[2]))/mupp,layerExtent[0],layerExtent[3], xExtension, yExtension)
			
		if lastPixel<>pixpoint:
			coordCount += 1
			if coordCount > 1:
				svgPath += 'L '
			svgPath += (str(pixpoint[0]) + ',' + str(pixpoint[1]) + ' ')
			lastPixel = pixpoint
					
	if coordCount > 2:
		svgPath += '" />\n'
		svgPolygon.extend([svgPath])
		
	return svgPolygon

def w2p(x, y, mupp, minx, maxy, xExtension, yExtension):
	pixX = (x - minx)/mupp
	pixY = (y - maxy)/mupp
	return [round(float(pixX),1), round(float(-pixY),1)]
	
def sanitizeStr(string):
	return string.replace(' ','_').replace('/','_').replace(',','_').replace('.','_').replace('-','_')

def runSvgGenerator(ifile, ofile, nameField, widthPixels):
	
	#Definim les variables d'entrada per al proces
	layer = shapefile.Reader(ifile)
	fieldName = nameField
	countFields = 0
	fieldNum = 0
	mupp = widthPixels
	for field in layer.fields:
		if type(field) is tuple:
			continue
		else:
			if field[0] == fieldName:
				fieldNum = countFields
			else:
				countFields += 1

	#Generant la bounding box del shapefile i convertint-la en variable	
	layerExtent = layer.bbox
	boxConstructor = shapefile.Writer(shapefile.POLYGON)
	
	boxConstructor.poly(parts=[[[layerExtent[0],layerExtent[1]],[layerExtent[2],layerExtent[3]]]])
	extentAsPoly = boxConstructor.shapes()[0]
	
	#Generant la llista de fields i geometries asociades per a cada element grafic del shapefile
	records = layer.records()
	shapes = layer.shapes()
	
	features = zip(records,shapes)

	#Escrivint les capsaleres de l'arxiu SVG
	svg = [u'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n']
	svg.append(u'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
	svg.append(u'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')

	for feature in features:
		svg.extend(feature2svg(feature, fieldNum, extentAsPoly, layerExtent, mupp))
		
	svg.append(u'</svg>')

	writeToFile(ofile, svg)
	
print
print u"Use printFields(pathToShpTheFile) method to know the layer fields names. With this method you can chose which field you want to use as svg output file id."