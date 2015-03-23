
import os
import gf

from joblib import Parallel, delayed
import multiprocessing




def gap_fill_scenes(scene):

    years = range(1999,2014)

    index = range(0,100)




    for i in index:
        if os.path.exists(r'G:\UMD_Landsat_tiles\1999\%s_1999_30_%i.tif' % (scene, i)):
            for year in years:
                gf.gf(scene, year, i)


if __name__ == '__main__':


	scenes = ["00N_000E", "00N_010E", "00N_020E", "00N_030E",
              "10N_000E", "10N_010E", "10N_020E", "10N_030E",
              "10S_010E", "10S_020E", "10S_030E",
              "20S_000E", "20S_010E", "20S_020E", "20S_030E"]

	num_cores = multiprocessing.cpu_count()
	Parallel(n_jobs=num_cores)(delayed(gap_fill_scenes)(scene) for scene in scenes)
	raw_input('Press Enter to exit')