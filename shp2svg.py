import os
import shapefile

print 'Welcome to SvgGenerator. To start the workflow you have to initialize svgLooper class passing 5 parameters: in_path (to the shapefiles folder container), out_path (to the future svg folder container), field_name (field what you want as svg geometries id), pixels_size (of the output svg file).'
print


class SvgLooper:
    def __init__(self, in_path, out_path, pixels_size):
        self.files = []
        self.in_path = os.path.realpath(in_path)
        self.out_path = out_path
        self.pixels_size = pixels_size
        self.generator = SvgGenerator(in_path, out_path, pixels_size)

    def setFilesListed(self):
        for file in os.listdir(self.in_path):
            if '.shp' in file:
                self.files.append(os.path.join(self.in_path, file))

    def startLooper(self, id_field):
        for file in self.files:
            self.generator.runSvgGenerator(file, id_field)

    def setupLooper(self):
        self.setFilesListed()
        print self.generator.printFields(self.files[0])


class SvgGenerator:
    def __init__(self, in_file, out_path, width_pixels):
        self.in_file = os.path.realpath(in_file)
        self.out_path = os.path.realpath(out_path)
        self.width_pixels = width_pixels

    def writeToFile(self, ofile, svg):
        svg_filename = ofile.split('.')[0] + '.svg'
        output = svg
        file = open(svg_filename, "wb")
        for line in output:
            file.write(line.encode('utf-8'))
        file.close()
        print 'SVG generat. Verifica que realment es aixi, al cap i a la fi soc un socioleg jugant a programar'

    def printFields(self, ifile):
        fieldsList = []
        layer = shapefile.Reader(ifile)
        for field in layer.fields:
            if type(field) is tuple:
                continue
            else:
                fieldsList.append(field[0])

        print
        print fieldsList
        print

    def feature2svg(self, feature, field_num, layer_extent, mupp):
        geom = feature[1]
        id = self.sanitizeStr(unicode(feature[0][field_num], 'utf-8').lower())
        svgGroup = [u'<g id="' + id + '">\n']

        if len(geom.parts) == 1:
            svgGroup.extend(self.polygon2path(geom, layer_extent, mupp))
        elif len(geom.parts) > 1:
            svgGroup.extend(self.multiPolygon2path(geom, layer_extent, mupp))
        else:
            pass

        svgGroup.append('</g>\n')

        return svgGroup

    def multiPolygon2path(self, geom, layer_extent, mupp):
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
            last_pixel = [0, 0]
            coordCount = 0

            for latLng in ring:
                x, y = latLng[0], latLng[1]
                if layer_extent[0] > 0 and layer_extent[2] > 0 or layer_extent[0] > 0 and layer_extent[2] > 0:
                    pixpoint = self.w2p(x, y, abs(layer_extent[0] - layer_extent[2]) / mupp, layer_extent[0],
                                        layer_extent[3])
                else:
                    pixpoint = self.w2p(x, y, (abs(layer_extent[0]) + abs(layer_extent[2])) / mupp, layer_extent[0],
                                        layer_extent[3])

                if last_pixel <> pixpoint:
                    coordCount += 1
                    if coordCount > 1:
                        svgPath += 'L '
                    svgPath += (str(pixpoint[0]) + ',' + str(pixpoint[1]) + ' ')
                    last_pixel = pixpoint

            if coordCount > 2:
                svgPath += '" />\n'
                svgPolygon.extend([svgPath])

        return svgPolygon

    def polygon2path(self, geom, layer_extent, mupp):
        svgPolygon = []
        svgPath = '<path d="M '
        last_pixel = [0, 0]
        coordCount = 0

        for latLng in geom.points:
            x, y = latLng[0], latLng[1]
            if layer_extent[0] > 0 and layer_extent[2] > 0 or layer_extent[0] > 0 and layer_extent[2] > 0:
                xExtension = abs(layer_extent[0] - layer_extent[2])
                yExtension = abs(layer_extent[1]) + abs(layer_extent[3])
                pixpoint = self.w2p(x, y, abs(layer_extent[0] - layer_extent[2]) / mupp, layer_extent[0], layer_extent[3])
            else:
                xExtension = abs(layer_extent[0]) + abs(layer_extent[2])
                yExtension = abs(layer_extent[1]) + abs(layer_extent[3])
                pixpoint = self.w2p(x, y, (abs(layer_extent[0]) + abs(layer_extent[2])) / mupp, layer_extent[0],
                                    layer_extent[3])

            if last_pixel <> pixpoint:
                coordCount += 1
                if coordCount > 1:
                    svgPath += 'L '
                svgPath += (str(pixpoint[0]) + ',' + str(pixpoint[1]) + ' ')
                last_pixel = pixpoint

        if coordCount > 2:
            svgPath += '" />\n'
            svgPolygon.extend([svgPath])

        return svgPolygon

    def w2p(self, x, y, mupp, minx, maxy):
        pix_x = (x - minx) / mupp
        pix_y = (y - maxy) / mupp
        return [round(float(pix_x), 1), round(float(-pix_y), 1)]

    def sanitizeStr(self, string):
        return string.replace(' ', '_').replace('/', '_').replace(',', '_').replace('.', '_').replace('-', '_')

    def runSvgGenerator(self, in_file, id_name):

        # Definim les variables d'entrada per al proces
        layer = shapefile.Reader(in_file)
        out_file = os.path.join(self.out_path, os.path.basename(in_file))
        field_name = id_name
        count_fields = 0
        field_num = 0
        mupp = self.width_pixels
        for field in layer.fields:
            if type(field) is tuple:
                continue
            else:
                if field[0] == field_name:
                    field_num = count_fields
                else:
                    count_fields += 1

        # Generant la bounding box del shapefile i convertint-la en variable
        layer_extent = layer.bbox
        boxConstructor = shapefile.Writer(shapefile.POLYGON)

        boxConstructor.poly(parts=[[[layer_extent[0], layer_extent[1]], [layer_extent[2], layer_extent[3]]]])

        # Generant la llista de fields i geometries asociades per a cada element grafic del shapefile
        records = layer.records()
        shapes = layer.shapes()

        features = zip(records, shapes)

        # Escrivint les capsaleres de l'arxiu SVG
        svg = [u'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n']
        svg.append(
            u'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        svg.append(u'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n')

        for feature in features:
            svg.extend(self.feature2svg(feature, field_num, layer_extent, mupp))

        svg.append(u'</svg>')

        self.writeToFile(out_file, svg)
