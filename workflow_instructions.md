<H1>Instructions for processing Site-Pipelines workflow</H1>

These instructions are designed to be a step-by-step walk-through of the
workflow to process field data and compare them to satellite data, or a new
field dataset. It is assumed that this workflow will be run on the NCI VDI
platform, as the Digital Earth Australia (DEA) module is required to run the
workflows.<P>

# Pre-requisites

In order for the workflow to run, there are a number of other assumed
requirements that should be met. Go through this check-list before running
the workflow for the first time:
<OL>
<LI>The Python library for this workflow, as well as notebooks and support
scripts can be found on VDI and should be cloned/downloaded from this repo or
copied into the working directory directly on VDI:<BR><BR>
    cp -r /g/data/u46/users/aw3463/GuyByrne/calval .<BR><BR>
<LI>The DEAPlotting library is also needed for RGB plots and can be obtained
from https://github.com/GeoscienceAustralia/dea-notebooks under "10_Scripts" or
can be copied on VDI to the working directory:<BR><BR>
    cp /g/data/u46/users/aw3463/GuyByrne/calval/DEAPlotting.py .<BR><BR>
<LI>Start up the DEA module by typing:<BR><BR>
    > module load dea<BR><BR>
<LI>Copy the template in the Site-Pipelines directory to a new file and then
start the notebook. eg:<BR><BR>
    > cp Site-Pipelines/template.ipynb Pipeline-PIN-20-05-18.ipynb<BR>
    > jupyter notebook Pipeline-PIN-20-05-18.ipynb<BR><BR>
<LI>Input and output directories should be defined in the first cell, as
'indir' and 'output', respectively. For the input directory, it is assumed
that there are multiple sub-directories, with format 'line1, line2, line3' etc.
Note that lower case is required and no extra characters are allowed in the
directory names. So 'Line1' or 'line_1' will not work. The output directory
will be created by the workflow and is where PNG files will be stored, as well
as the data sheet text file.<P>
Raw data for testing purposes can be found under the directory 'Misc/Testdata'.
So 'indir' can be changed to point to this directory, if you need to check out
how the workflow operates. The raw data correspond to the 20MAY18 Pinnacles
field site measurements that are the default in the template workflow.<P>
<B>NOTE:</B> Each time the workflow is run, the output directory will be erased
and re-written, so that the directory can be cleaned up. If you want to save
older PNGs, you need to manually move them before re-running the
notebook.<BR><BR>
<LI>Within each 'line' sub-directory, there should be radiance spectrum files
in text format, with extension '.asd.rad.txt'.<BR><BR>
<LI>There are standard files that are used for determining the panel K-factor,
currently located either in this repo under <B>Misc</B> or:<BR><BR>
        /g/data/u46/users/aw3463/GuyByrne/30APR18/Panels/<BR><BR>
<LI>Satellite band response files are located either in this repo under
<B>Misc</B> or in the directory:<BR><BR>
        /g/data1a/u46/users/aw3463/GuyByrne/misc_others/<BR><BR>
        including landsat8_vsir.flt, Sent2a.flt and Sent2b.flt.<BR><BR>
<LI>The 'field_data' list should be edited to contain the relevant information
on: <BR>
1. Three-letter field name (eg. PIN for The Pinnacles)<BR>
2. Date of field site measurement (format: DDMMMYY)<BR>
3. Extra field site information (eg. Site1/2 or CSIRO)<BR>
4. Satellite name (must be one of Landsat8, Sentinel2a, Sentinel2b)<BR>
5. The name of the panel K-factor to use<BR>
6. Whether the data were recorded in Radiance or Reflectance mode.<BR><BR>

<LI>The lists 'bad_pans' and 'bad_grounds' can be left as empty for the first
time running the workflow (eg. 'bad_pans = []'). These are used to specify
any bad panel or ground readings identified later on.<BR><BR>
<LI>Variables firstGoodLine, firstGroundSpec and firstGoodPanelSpec need to be
specified. These are determined from knowledge of the field data and can be
used to eliminate bad data at the start of the field collection. If all goes
well, normally the first good line is number 1, the first good panel is number
0 and the first good ground spectrum is number 2. ie. there are two panel
spectra at the start of line 1 (spec=0 and 1), followed by the first ground
(spec=2).<BR><BR>
<LI>The BRDF correction should be calculated in a separate directory and a new
window on VDI.
Do NOT use a window where you have already typed 'module load dea' because the
BRDF calculation needs slightly different modules. In this example, the
directory '/g/data/u46/users/aw3463/GuyByrne/calval/brdf' is used (a copy is
also in this repo under the <B>brdf</B> directory). Once you have created your
own directory and you have changed into that directory, type the following to
copy over the required files:<BR><BR>
        > cp /g/data/u46/users/aw3463/GuyByrne/calval/brdf/* .<BR><BR>
</OL>

# Calculating BRDF correction

One of the first things you need to do in this notebook is calculate the BRDF
correction, but this requires that you read in the field data so that the
latitude, longitude and time of the field data can be used to create the
correction. Do the following steps:

<OL>
<LI>Run the first five cells of the workflow.
<LI>The fifth cell will print out scripts for determining the BRDF correction.
You will see the script output below something like:<BR><BR>
        
        
        #################################################################################
        # Copy and paste the following into a terminal window on VDI for SATELLITE data #
        #################################################################################
<BR><BR>
        
        
where 'SATELLITE' is either 'Landsat 8' or 'Sentinel 2'.<BR><BR>
<LI>Copy and paste the output text directly into the brdf terminal
window.<BR><BR>
<LI>The result in the terminal window (takes about 30 seconds) will be a
formatted version of the 'brdf_data' numpy array. This can be directly copied
and pasted over the top of the existing brdf_data array near the bottom of the
first cell in the notebook.<BR><BR>
</OL>

# Running the notebook
Once the BRDF correction has been added to the notebook, it should be possible
to run the notebook in its entirety. To do this, go to the top of the Jupyter
Notebook and click on 'Kernel', then 'Restart & Run All', then click on the
red button to confirm and run the workflow. It should take about 2-5 minutes
to complete.

### Interpreting results of the first notebook run
Here, it is assumed that the notebook ran to completion, such that all the
cells were processed. If the notebook stopped midway, then please see the
<B>Troubleshooting</B> section below for some hints on what might have gone
wrong.<BR><BR>
    
<B>Cell [4]</B> (Define 'alldata'...) lists a small section of the field data
as a pandas dataframe. Only data for a wavelength of 350nm is shown. Check
that the values in each column appear reasonable.<BR><BR>
    
<B>Figure 1</B> (Plot panel radiances...) will show overlay plots of panel
radiances on both the left- and right-hand-sides, with the middle pane empty.
All panel radiances should appear close together. If you notice a small number
of panels that look significantly different, then these are probably bad panel
radiances. You should try to identify the corresponding spectra and then add
them to the 'bad_pans' list in Cell [1]. Once you have flagged the bad panel
spectra, you should be able to re-run the notebook and this Figure will now
show you the good and bad panels separated into the left and middle panes,
respectively, with all panels together shown in the right pane.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig1_PanelRadiances.png"><HR>
    
<B>Figure 2</B> (Diagnosis plots...) Will show various plots of any identified
bad panel spectra. This is only used if you are curious about why some panel
spectra may be misbehaving.<HR>
    
<B>Figure 3</B> (Plot ground spectra...) shows two panes, which initially will
be the same, showing an overlay of all the ground radiances (without panels).
This plot can be used to identify any outlying ground radiances, which can be
subsequently identified using 'bad_grounds' in Cell [1]. Once such bad
radiances have been flagged, then the two panes will show a with/without
comparison.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig3_GroundRadiances.png"><HR>
    
<B>Figures 4 and 5</B> (Plot timelines...) will initially be the same. They
show a line-by-line plot of the timelines of spectra taken, with the horizontal
axis being seconds since the first spectrum was taken. Panel radiances are
shown as blue crosses and ground radiances are shown as orange vertical lines.
If there are any errant panel or ground radiances, based on the time they were
taken, they can be identified here. Also, these plots can be used to assess
when the panel readings for each line occur. If there are any bad panels or
ground radiances, then they will be removed from the second figure.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig4_AllTimeLineData.png"
width=50%>
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig5_GoodTimeLineData.png"
width=50%><HR>
    
<B>Figure 6</B> (Create timeline...) Shows two panes with averaged radiances
for panel spectra, as a function of time (in seconds, since the first
spectrum). Initially they will show the same. The average panel readings
should show a slowly changing curve that follows insolation. For example,
field data taken in the morning will show a slowly rising curve, as the Sun
rises. Deviations from this slowly changing curve may identify bad panel
readings that should be flagged out in 'bad_pans' in Cell [1]. Once the
notebook is re-run, any bad panels will be removed from the second pane.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig6_TimevsAvgPanels.png"><HR>
    

<B>Figure 7</B> (Fit Insolation Curve) Plot the averaged panel radiance as a
function of the cosine of the Solar zenith angle. On these axes, the data
should follow a straight line, which can then be fit.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig7Insolation.png" width=50%><HR>

<B>Figure 8</B> (Plot all ground...) shows reflectance spectra for all good
ground observations as black curves. Coloured curves show the average for all
spectra in a Line. the right pane just shows a zoomed y-axis, compared to the
left pane. Any unusually different spectra can be identified here and may be
flagged in 'bad_grounds' in Cell [1].
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig8_Reflectances.png"><HR>
    
<B>Figure 9</B> (Plot band reflectances) shows the reflectance spectra
convolved to the satellite bands.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig9_BandReflectances.png"><HR>
    
<B>Figure 10</B> Alternate plot of Figs 9 and 10, friendly for inclusion in a
paper or technical report.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig10_Reflectances_Band.png"><HR>

<B>Figure 11</B> (Histogram of all...) shows band-by-band histograms for all
reflectances. The histograms typically conform to a Normal distribution, but
unusually bright or dark spectra may be identified as extreme outliers
here.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig11_BandHistograms.png"><HR>
    
<B>Figure 12</B> (Plot satellite band...) show the median ground reflectance,
together with the wavelength ranges for the satellite bands, corresponding to
the field data. This is just to check that the satellite bands fall within
well-behaved parts of the spectrum.

<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig12_BandWavelengths.png"
width=50%><HR>
    
<B>Figure 13</B> (Plot relative locations...) shows a relative
longitude/latitude positions for both field and satellite data. A grid is also
shown to represent the extent of the satellite pixels.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig13_SatFieldLocations.png"><HR>
    
<B>Figures 14, 15 and 16</B> show RGB images of the Satellite and field data,
where the field data have been averaged into pixels that match the satellite
data. A blank field pixel means that there is no field data corresponding to
that pixel.

<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig14_Satellite_bigRGB.png"
width=50%>
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig15_Satellite_RGB.png" width=50%>
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig16_Field_rgb.png" width=50%><HR>

<B>Figure 17</B> shows the band-by-band satellite data. This gives an
indication of how much change there is across the field site. There should
typically be less than 5% variability.

<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig17_SatBands.png"><HR>
    
<B>Figure 18</B> (Plot ratio arrays) shows band-by-band images of the ratio
between satellite and field arrays. All images have been scaled to ratios
between 0.9 and 1.1, such that green colours indicate a close match between
field and satellite pixels.

<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig18_RatioSatOverFieldData.png">
<HR>
    
<B>Figure 19</B> (Plot comparison spectra...) shows a band-by-band comparison
of satellite and field data. Three spectra are shown. Black is the average
spectrum for <I>all</I> satellite pixels, orange is the average for only those
satellite pixels that overlap with at least one field spectrum. The blue
spectrum shows the average for all field data. Any difference between the
orange and black spectra is indicative of the variation in the ground spectrum,
as measured by the satellite at slightly varying positions, so it gives a
guide for how reliable the satellite data is.

<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig19_InnerFieldBandCompare.png"
width=50%>
<HR>
    
<B>Figure 20</B> A similar plot to Figure 19 that is more suitable for papers
and technical reports.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig20_InnerFieldBandCompare.png"
width=50%><HR>

<B>Figure 21</B> (Comparison plot of...) shows a scatter plot, comparing the
satellite and field data where there is at least one field spectrum overlapping
with each satellite pixel. Different bands are shown with different symbols and
colours.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig21_PixelByPixelComparison.png"
width=50%><HR>
    
<B>Figure 22</B> shows the same as Figure 21, but for each band all the pixel
data is averaged, so there is one data point per band. Error-bars are shown,
which represent the standard deviation of the satellite and field data.
<img src="Misc/Example/PIN_20MAY18__Landsat8_Fig22_AvgComparison.png" width=50%><HR>
    
<B>Data Sheet</B> text file is written out to the PNG directory, which has some
summary information on the field site and corresponding satellite data. Example
datasheet: 

```
DATA SHEET FOR PIN taken on 20MAY18,  Landsat8 overpass
------------------------------------------------------------------

Time of field site measurements is from 02:17:06 to 02:42:36 on the 20 May, 2018 (UTC)
Satellite overpass was at 2018-05-20T02:10:11.500000000 (UTC)

Difference in time between start of field site measurement
and satellite overpass is -1 days +23:53:05.500000

Good GPS Coordinates were found in the headers
Approximate bounding box coordinates:
SE: (115.15636, -30.585108)
SW: (115.155105, -30.585108)
NE: (115.15636, -30.583947)
NW: (115.155105, -30.583947)

Solar Zenith angle is from 58.0 to 55.3 degrees.

Data were read in from /g/data1a/u46/users/aw3463/GuyByrne/30APR18/Pinnacles/20MAY18/
PNGs were written to /g/data/u46/users/aw3463/GuyByrne/calval/PNGS/TMP/

Panel is assumed to be GA_Panel
Data is assumed to be recorded in Radiance mode.

Satellite processing and historical data can be found using the following dataset ID and location:
[Dataset <id=92f3d234-f1d1-48ac-9737-64b84b9ad3e7 type=ls8_nbart_scene location=/g/data/rs0/scenes/nbar-scenes-tmp/ls8/2018/05/output/nbart/LS8_OLITIRS_NBART_P54_GANBART01-032_113_081_20180520/ga-metadata.yaml>]

Summary Statistics over entire field site:
------------------------------------------

Band      Sat     Sat   Field    Field    Sat    Field  Sat/Fld Sat
         mean     rms    mean     rms  rms/mean rms/mean Ratio  Pixel-by-pixel
                                         (%)     (%)            rms (%)
CA	0.18	0.0152	0.19	0.0136	8.46	7.2	0.947	6
blue	0.217	0.0192	0.239	0.0169	8.86	7.07	0.908	6.13
green	0.428	0.0297	0.473	0.03	6.92	6.35	0.906	4.9
red	0.557	0.0383	0.595	0.0369	6.88	6.2	0.938	4.93
nir	0.653	0.0498	0.672	0.0407	7.62	6.06	0.972	5.2
swir1	0.733	0.0506	0.769	0.045	6.9	5.85	0.953	4.86
swir2	0.589	0.0348	0.629	0.04	5.91	6.36	0.935	4.55
```
<HR>
    
# Troubleshooting
If the notebook does not complete, there are a few likely causes that can be
checked.<BR>
    
It is possible that field data were recorded without GPS location information
in the header. In such cases, the header will appear like:<BR><BR>


    GPS-Latitude is S0
    GPS-Longitude is E0


The notebook will automatically identify such cases and try to deal with them,
but it needs to know the coordinates for the box over which the field data was
measured. These coordinates are fed into the variable "Corners" at the bottom
of Cell [1], along with a True/False declaration for "RockWalk". If no
coordinates are given and datacube manages to find satellite data, datacube
will try and find a map at (0,0) and fail.<BR><BR>

The coordinate fix necessarily makes assumptions about how the field data were
collected. In particular, the direction the data collector was walking.
"RockWalk", if set to True, will assume that the collector walked in a
South -> North line, then North -> South, then South -> North etc. If
"RockWalk" is set to False, then it is assumed the direction of walk is always
South -> North.<BR>
Note: Cell [36] will always say whether or not good GPS coordinates were
found.<BR><BR>

### Cell [4] (Define 'alldata'...) errors:

One of the most common errors is that the code will fail on Cell [4]
(Define 'alldata'...), which is most likely because the input data files or
directories are incorrectly formatted. Here are a list of errors and likely
solutions:<BR><BR>

<B>ValueError: No objects to concatenate</B>: The code cannot find any relevant
files. Check 'indir' is correct, check the line directories are formatted as
line1, line2 etc. Also check .asd.rad.txt files in the line directories.<BR><BR>


<B>ValueError: not enough values to unpack (expected 6, got 0)</B>: Most likely
there is one (or more) .asd.rad.txt file with incorrectly formatted header
information. For example, a file that is not a spectrum at all.<BR><BR>

<B>ValueError: invalid literal for int() with base 10</B>: This is casued by
an incorrectly formatted spectral file name, which is found on line 39 of the
header. The code requires this line to be in the format *00.asd.rad or 
*00.asd, where the two numbers '00' will be read as the spectrum number. This
error complains that it is finding a string at this position, rather than a
number.<BR><BR>

### Datacube query errors:

The notebook uses Datacube to extract satellite data for comparison. However,
it is only expected that exactly one satellite dataset will be found. So
errors can occur when no relevant dataset is found.<BR><BR>

<B>Cell [31]: KeyError: 'the label [band11] is not in the [index]'</B>: This
error occurs when you have previously generated a brdf_data array for Sentinel
data but then process the workflow, assuming Landsat 8 data, with fewer bands.
In this case, you need to re-calculate your BRDF array in Cell [4] for the
correct satellite.<BR><BR>

<B>Cell [31]: AttributeError: 'Dataset' object has no attribute 'x'</B>: This
error is casued by Datacube not finding any relevant satellite data for the
timerange given. Check the dates given in timerange. Also check that Datacube
contains the data that you are looking for. It is possible that the data have
yet to be indexed, if the observations were recent.<BR><BR>

<B>Cell [31]: ValueError: cannot rename '1' because it is not a variable or
dimension in this dataset</B>: This error also happens because datacube has
not found any relevant satellite data for the time range.<BR><BR>
