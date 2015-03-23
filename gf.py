import arcpy
import numpy as np
import os
import gc
import sys

arcpy.env.overwriteOutput = True

def gf(scene, year, i):
    input_folder = r'G:\UMD_Landsat_tiles\%i' % year
    bands = [30, 40, 50, 70]

    if not os.path.exists(r'%s\filled\%s_%i_%i_filled.tif' % (input_folder, scene, year, i)):

        if not os.path.exists(r'%s\filled' % input_folder):
            os.mkdir(r'%s\filled' % input_folder)
        if year == 1999:
            band1 = os.path.join(input_folder,"%s_%i_30_%i.tif" % (scene, year, i))
            band2 = os.path.join(input_folder,"%s_%i_40_%i.tif" % (scene, year, i))
            band3 = os.path.join(input_folder,"%s_%i_50_%i.tif" % (scene, year, i))
            band4 = os.path.join(input_folder,"%s_%i_70_%i.tif" % (scene, year, i))
            input_bands = "%s;%s;%s;%s" % (band1, band2, band3, band4)
            output = r'%s\filled\%s_%i_%i_filled.tif' % (input_folder,scene, year, i)
            print output
            arcpy.CompositeBands_management(input_bands, output)
        else:

            a = None

            for band in bands:
                if band ==30:
                    r1 = arcpy.Raster(r'G:\UMD_Landsat_tiles\%i\filled\%s_%i_%i_filled.tif\Band_1' % (year-1,scene, year-1, i))
                elif band == 40:
                    r1 = arcpy.Raster(r'G:\UMD_Landsat_tiles\%i\filled\%s_%i_%i_filled.tif\Band_2' % (year-1,scene, year-1, i))
                elif band == 50:
                    r1 = arcpy.Raster(r'G:\UMD_Landsat_tiles\%i\filled\%s_%i_%i_filled.tif\Band_3' % (year-1,scene, year-1, i))
                elif band == 70:
                    r1 = arcpy.Raster(r'G:\UMD_Landsat_tiles\%i\filled\%s_%i_%i_filled.tif\Band_4' % (year-1,scene, year-1, i))



                r2 = arcpy.Raster(r'%s\%s_%i_%i_%i.tif' % (input_folder, scene, year, band, i))

                lowerLeft = arcpy.Point(r1.extent.XMin,r1.extent.YMin)
                cellSize = r1.meanCellWidth

                # Convert Raster to numpy array
                a1 = arcpy.RasterToNumPyArray(r1,nodata_to_value=0)
                a2 = arcpy.RasterToNumPyArray(r2,nodata_to_value=0)

                del r1, r2

                a3 = np.expand_dims(np.where(a2==0,a1,a2), axis=0)

                del a1, a2

                if a == None:
                    a = a3
                else:
                    a = np.vstack((a,a3))

                del a3

            #Convert Array to raster (keep the origin and cellsize the same as the input)

            if not os.path.exists(r'%s\filled' % input_folder):
                os.mkdir(r'%s\filled' % input_folder)

            r = arcpy.NumPyArrayToRaster(a,lowerLeft,cellSize,value_to_nodata=0)
            print r'%s\filled\%s_%i_%i_filled.tif' % (input_folder, scene, year, i)
            r.save(r'%s\filled\%s_%i_%i_filled.tif' % (input_folder, scene, year, i))

            del a, r

            gc.collect()

if __name__ == '__main__':

    if len(sys.argv) == 4:
        gf(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    else:
        print "wrong number of arguments"