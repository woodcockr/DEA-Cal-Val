import numpy as np
import pandas as pd


#
# Create a statistics dataframe to compare field and satellite for a subset of pixels
#
def create_SUB_stats(sat_array, field_array, fstat_df, inpix):

    inner_array = np.array([['', 'LS8_inner_mean', 'Field_inner_mean'],
                            ['Band1', float(sat_array.coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band2', float(sat_array.blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band3', float(sat_array.green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band4', float(sat_array.red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band5', float(sat_array.nir[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nir[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band6', float(sat_array.swir1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.swir1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band7', float(sat_array.swir2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.swir2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                           ])

    inner_df = pd.DataFrame(data=inner_array[1:,1:],
                      index=inner_array[1:,0],
                      columns=inner_array[0,1:])

    inner_df['Field_SD'] = fstat_df['Field_SD']

    finner_df = inner_df.astype(float)
    return finner_df