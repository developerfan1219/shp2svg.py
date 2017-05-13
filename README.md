# shp2svg.py
Python library to convert shapefiles in svg maps including a fields from the shapefile as svg geometries id.

First, import the library to your python console:

  	  usage: import shp2svg as s2s
      
The library contains two classes: the generator (translator between shp and svg) and the looper. The looper allows you to transform not only one shp, but all files contained in a folder.

Generator:

  First you need to instantiate the class. The generator require two parameters: the output path where you want to create the 
  new files, and the width size, in pixels, what the svg file will be layout.

      usage: generator = s2s.SvgGenerator('outputPath',600)
  
  Continue with shapefile exploring function. Use printFields() method to know the layer fields names. With this method you can  
  chose which field you want to use as svg output file id.

  	  usage: generator.printFields('pathToTheShpFile')
  
  Once you have selected your id, you have to call run() method. This function require two parameters: The shapefile 
  field name you want as id and the path to the shp file like you can see below. This methow will create the svg file in the 
  defined output path.

  	  usage: generator.run('input_file','id_name')
      
Looper:

  Like before, the first step is to instantiate the class: The looper require three params: The path to the container folder, 
  the output path where files will be generated, and the width size, in pixels, like before.
  
      usage: looper = s2s.SvgLooper('pathToFolder','outputPath',600)
      
  Once the class is instantiated, you have to run the setupLooper method to storage all files and to print fields name to allow 
  you to chose which field do you want as id for the svg geometries.
  
      usage: looper.setup()
      
  At least, you only have to call the run method passing the selected ID and wait for the result.
  
      usage: looper.run('selectedId')
