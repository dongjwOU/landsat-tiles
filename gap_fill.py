import arcpy
import numpy


# Get input Raster properties

scenes = ["00N_000E", "00N_010E", "00N_020E", "00N_030E",
          "10N_000E", "10N_010E", "10N_020E", "10N_030E",
          "10S_010E", "10S_020E", "10S_030E",
          "20S_000E", "20S_010E", "20S_020E", "20S_030E"]

years = range(2000,2014)

bands = [30, 40, 50, 70]

for scene in scenes:
    for year in years:

        a = None

        for band in bands:
            r1 = arcpy.Raster('%s_%i_%i.tif' % (scene, year-1, band))
            r2 = arcpy.Raster('%s_%i_%i.tif' % (scene, year, band))

            lowerLeft = arcpy.Point(r1.extent.XMin,r1.extent.YMin)
            cellSize = r1.meanCellWidth

            # Convert Raster to numpy array
            a1 = arcpy.RasterToNumPyArray(r1,nodata_to_value=0)
            a2 = arcpy.RasterToNumPyArray(r2,nodata_to_value=0)

            a3 = np.expand_dims(np.where(a2==0,a1,a2), axis=0)
            
            if not a:
                a = a3
            else:
                a = np.vstack((a,a3))

        #Convert Array to raster (keep the origin and cellsize the same as the input)
        r = arcpy.NumPyArrayToRaster(a,lowerLeft,cellSize,value_to_nodata=0)
        r.save('%s_%i_filled.tif' % (scene, year))
