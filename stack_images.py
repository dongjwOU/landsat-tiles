import arcpy
import os

from joblib import Parallel, delayed  
import multiprocessing


#loop through years and scenes
def stack_scenes(year):
#for year in years:
	arcpy.env.overwriteOutput = True
	#Define scene names
	scenes = ["00N_000E", "00N_010E", "00N_020E", "00N_030E",
			  "10N_000E", "10N_010E", "10N_020E", "10N_030E",
			  "10S_010E", "10S_020E", "10S_030E",
			  "20N_000E", "20N_010E", "20N_020E", "20N_030E"]
	input_folder = r"F:\UMD_Landsat"
	for scene in scenes:
        #Define bands (RGB = 453)
		band1 = os.path.join(input_folder,"%s_%i_40.tif" % (scene, year))
		band2 = os.path.join(input_folder,"%s_%i_50.tif" % (scene, year))
		band3 = os.path.join(input_folder,"%s_%i_30.tif" % (scene, year))

        #Define input parameter for Composite Band tool
		input_bands = "%s;%s;%s" % (band1, band2, band3)
		#print input_bands

        #Define output parameter for Composite Band tool
		output_folder = r"G:\UMD_Landsat_Stack\%i" % year
		if not os.path.exists(output_folder):
			os.mkdir(output_folder)
		output = os.path.join(output_folder,"%s_%i_453.png" % (scene, year))

        # Set JPEG compression quality to 100%
        #arcpy.env.compression = "JPEG 100"

		if arcpy.Exists(band1) and arcpy.Exists(band2) and arcpy.Exists(band3):
            ##Compose multi types of single band raster datasets to a TIFF format raster dataset
			print "Create %s" % output
			arcpy.CompositeBands_management(input_bands, output)
		else:
			#print "Cannot find input files"
			print "Cannot create %s" % output

if __name__ == '__main__':
	#arcpy.env.workspace = r"F:\UMD_Landsat"
	
	#Define range (1999-2013)
	years = range(1999, 2014)
				
	num_cores = multiprocessing.cpu_count()			
	Parallel(n_jobs=num_cores/2)(delayed(stack_scenes)(year) for year in years) 	
	raw_input('Press Enter to exit')
