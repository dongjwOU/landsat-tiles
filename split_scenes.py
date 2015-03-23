import arcpy
import glob
import os

from joblib import Parallel, delayed  
import multiprocessing




def split_scene(scene):

    base = os.path.basename(scene)[:-4]
    print base
    arcpy.SplitRaster_management(scene,r"G:\UMD_Landsat_tiles","%s_" % base,"NUMBER_OF_TILES","TIFF","NEAREST","10 10","2048 2048","0","PIXELS","#","#","#","NONE","#","#")


if __name__ == '__main__':
	#arcpy.env.workspace = r"F:\UMD_Landsat"
	
	#get scenes
	scenes = glob.glob(r"F:\UMD_Landsat\*.tif")
				
	num_cores = multiprocessing.cpu_count()			
	Parallel(n_jobs=num_cores/2)(delayed(split_scene)(scene) for scene in scenes) 	
	raw_input('Press Enter to exit')
