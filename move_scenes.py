#import arcpy
import glob
import os

from joblib import Parallel, delayed  
import multiprocessing



def move_scene(year):
    scenes = glob.glob(r"G:\UMD_Landsat_tiles\*%i*" % year)
    print year
    print len(scenes)

    for scene in scenes:
        basename = os.path.basename(scene)
        if not os.path.exists(r"G:\UMD_Landsat_tiles\%i" %year):
            os.mkdir(r"G:\UMD_Landsat_tiles\%i" %year)
        try:
            os.rename(scene, os.path.join(r"G:\UMD_Landsat_tiles\%i" %year, basename))
        except:
            print basename
    

if __name__ == '__main__':
	#arcpy.env.workspace = r"F:\UMD_Landsat"
	
	#get scenes
        years = range(2000,2014)
				
	num_cores = multiprocessing.cpu_count()			
	Parallel(n_jobs=num_cores/2)(delayed(move_scene)(year) for year in years) 	
	raw_input('Press Enter to exit')
