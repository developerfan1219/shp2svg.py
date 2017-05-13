# shp2svg.py
Python library to convert shapefiles in svg maps including a fields from the shapefile as svg geometries id.

Start importing the library to your python console:

  	  usage: import shp2svg as s2s

The library contains two classes: the generator (translator between shp and svg) and the looper. The looper allows you to batch not only one shp nor all files containeds in a folder. 

Generator:

  First you need to instantiate the class. The generator require two parameters: the output path where you want to create the new 
  files, and the width size, in pixels, what the svg file will be layout.

      usage: generator = s2sSvgGenerator('outputPath',600)
  
  Continue with shapefile exploring function. Use printFields() method to know the layer fields names. With this method you can  
  chose which field you want to use as svg output file id.

  	  usage: generator.printFields('pathToTheShpFile')
  
  Once you have tried your id, you have to call runSvgGenerator() method. This function require four parameters: The shapefile 
  field name you want as id; the path to the shp file; the path to the output svg file, and the witdth in pixels of the output 
  file. Parameters must be introduced in the next order: input_file, output_file, id_name and width_pixels.

  	  usage: generator.run('input_file','id_name')
      
Looper:

  Like before, the first step is to instantiate the class: The looper require 
