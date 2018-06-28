import pandas as pd
import pyproj
import matplotlib.pyplot as plt


#
# # Figure 
#
### Plot relative locations of field and satellite data
#
def FIG_sat_field_locations(ground_brdf, sat_array, colpac, output, field_data, fignum):

    wgs_84 = pyproj.Proj(init='epsg:4326')
    aus_albers = pyproj.Proj(init='epsg:3577')

    xloc = [pyproj.transform(wgs_84, aus_albers, ground_brdf['Longitude'][i], ground_brdf['Latitude'][i]) for i in range(len(ground_brdf))]

    relxloc = [(xloc[i][0]-xloc[0][0], xloc[i][1]-xloc[0][1]) for i in range(len(ground_brdf))]

    satloc = [[0 for x in range(2)] for y in range(len(sat_array.x)*(len(sat_array.y)))]
    count=0
    for i in range(len(sat_array.x)):
        for j in range(len(sat_array.y)):
            satloc[count][0] = float(sat_array.x[i]-xloc[0][0])
            satloc[count][1] = float(sat_array.y[j]-xloc[0][1])
            count+=1

    satloc_df = pd.DataFrame(satloc)

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(fig_title+': GeoLocations for data taken with LS8 (black) and field data (colours).\nReference position = '+str(xloc[0][0])+', '+str(xloc[0][1]), fontweight='bold')
    plt.tight_layout(pad=4.0, w_pad=1.0, h_pad=1.0)

    def gridlines(satloc_df):
        axes.axhline(satloc_df[1].unique()[0]+12.5, linestyle='--', color='black', linewidth=0.5)
        for i in range(len(satloc_df[1].unique())):
            axes.axhline(satloc_df[1].unique()[0]-(12.5+(25*i)), linestyle='--', color='black', linewidth=0.5)

        axes.axvline(satloc_df[0].unique()[0]-12.5, linestyle='--', color='black', linewidth=0.5)
        for i in range(len(satloc_df[0].unique())):
            axes.axvline(satloc_df[0].unique()[0]+(12.5+(25*i)), linestyle='--', color='black', linewidth=0.5)


    rr = pd.DataFrame(relxloc)

    ground_brdf_XY = pd.concat([ground_brdf, rr], axis=1)
    ground_brdf_XY.rename(columns={0: 'RelX', 1: 'RelY'}, inplace=True)

    for i in ground_brdf_XY.Line.unique():
        ground_brdf_XY[(ground_brdf_XY['Line']==i)].plot.scatter('RelX', 'RelY', ax=axes, color=colpac[i])

    satloc_df.plot.scatter(0,1, ax=axes, color='black', )

    axes.set_xlabel("Relative Aus Albers Longitude (m)")
    axes.set_ylabel("Relative Aus Albers Latitude (m)")

    gridlines(satloc_df)

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_SatFieldLocations.png')

    return xloc