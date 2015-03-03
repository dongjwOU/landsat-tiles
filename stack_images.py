import arcpy
arcpy.env.workspace = r"C:/Workspace"

#Define scene names
scenes = ["00N_000E", "00N_010E", "00N_020E", "00N_030E",
          "10N_000E", "10N_010E", "10N_020E", "10N_030E",
          "10S_010E", "10S_020E", "10S_030E",
          "20S_000E", "20S_010E", "20S_020E", "20S_030E"]

#Define range (1999-2013)
years = range(1999, 2014)

#loop through years and scenes
for year in years:
    for scene in scenes:
        #Define bands (RGB = 453)
        band1 = "%s_%i_40.tif" % (scene, year)
        band2 = "%s_%i_50.tif" % (scene, year)
        band3 = "%s_%i_30.tif" % (scene, year)

        #Define input parameter for Composite Band tool
        input_bands = "%s;%s;%s" % (band1, band2, band3)

        #Define output parameter for Composite Band tool
        output = "%s_%i_453.jpg" % (scene, year)

        # Set JPEG compression quality to 100%
        arcpy.env.compression = "JPEG 100"

        if arcpy.Exists(band1) and arcpy.Exists(band2) and arcpy.Exists(band3):
            ##Compose multi types of single band raster datasets to a TIFF format raster dataset
            print "Create %s" % output
            arcpy.CompositeBands_management(input_bands, output)
        else:
            print "Cannot find input files"
            print "Cannot create %s" % output

raw_input('Press Enter to exit')
