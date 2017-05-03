# shp2svg.py
Python library to convert shapefiles in svg maps with geometries' ids from shapefile fields.

Start importing the library to your python console:

  	usage: import shp2svg

Continue with shapefile exploring function. Use printFields() method to know the layer fields names. With this method you can chose which field you want to use as svg output file id.

  	usage: printFields('pathToTheShpFile')
  
Once you have tried your id, you have to call runSvgGenerator() method. This function require four parameters: The shapefile field name you want as id; the path to the shp file; the path to the output svg file, and the witdth in pixels of the output file. Parameters must be introduced in the next order: input_file, output_file, id_name and width_pixels.

  	usage: runSvgGenerator('input_file','output_file','id_name',width_pixels)
  
