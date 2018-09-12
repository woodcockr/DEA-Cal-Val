import DEAPlotting
import matplotlib.pyplot as plt

import importlib
importlib.reload(DEAPlotting)

#
### FIGURE 
#
# Plot large-area context RGB array for satellite data
#
def FIG_many_bigRGB(ls8_array, s2a_array, s2b_array, ls8_bigarray, s2a_bigarray, s2b_bigarray, output, field_data, fignum):

    print('Landsat 8')
    DEAPlotting.three_band_image_subplots(ls8_bigarray, bands = ['nir', 'swir1', 'swir2'], num_cols=8, figsize = (18, 65), contrast_enhance=False)
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB_LS8.png')
    print('Sentinel 2a')
    DEAPlotting.three_band_image_subplots(s2a_bigarray, bands = ['nbart_nir_1', 'nbart_swir_2', 'nbart_swir_3'], num_cols=8, figsize = (18, 45), contrast_enhance=False)
    #plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB_S2a.png')
    print('Sentinel 2b')
    DEAPlotting.three_band_image_subplots(s2b_bigarray, bands = ['nbart_nir_1', 'nbart_swir_2', 'nbart_swir_3'], num_cols=4, figsize = (18, 25), contrast_enhance=False)
    #plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB_S2b.png')
