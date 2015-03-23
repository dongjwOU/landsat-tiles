import arcpy

from joblib import Parallel, delayed  
import multiprocessing

def delete_tiles(year):

    print year
    arcpy.MakeMosaicLayer_management(r'G:\UMD_Landsat_tiles\tiles.gdb\t%i'% year, 'Footprint')
    arcpy.SelectLayerByAttribute_management('Footprint', 'NEW_SELECTION', '"OBJECTID" >= 0')

    arcpy.MakeFeatureLayer_management ('D:\GIS Data\CountryBoundaries\CountryBoundaries.gdb\CountryBoundaries', "Countries",
                                 "ISO3 = 'COG' OR ISO3 = 'COD' OR ISO3 = 'CMR' OR ISO3 = 'CAF' OR ISO3 = 'GNQ' OR ISO3 = 'GAB'")


    arcpy.SelectLayerByLocation_management ('Footprint', 'INTERSECT', 'Countries', '#', 'REMOVE_FROM_SELECTION')

    cursor = arcpy.SearchCursor('Footprint')
    for row in cursor:
        basename = (row.getValue("Name"))
        f = r'G:\UMD_Landsat_tiles\%i\%s.tif'% (year, basename)
        if arcpy.Exists(f):
            arcpy.Delete_management(f)

if __name__ == '__main__':
	#arcpy.env.workspace = r"F:\UMD_Landsat"
	
	#get scenes
        years = range(1999,2000)
				
	num_cores = multiprocessing.cpu_count()			
	Parallel(n_jobs=num_cores)(delayed(delete_tiles)(year) for year in years) 	
	raw_input('Press Enter to exit')
