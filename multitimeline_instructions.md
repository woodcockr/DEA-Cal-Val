<H1>Instructions for processing MultiTimeLine workflow</H1>

This workflow follows on from the Site-Pipelines workflow. It produces a
time-series for the field site of both Landsat and Sentinel data, since the
beginning of 2013. The first part of the workflow is the same as the
Site-Pipelines workflow, so if Site-Pipelines has successfully completed, then
this workflow should require some minor* tweaking.<P>

Within the MultiTimeLine directory, there will be a template.ipynb file,
which can be used as a starting point. Copy this file and edit the first cell
as for the Site-Pipelines workflow. There are a few extra fields that need to
be filled in here:
<OL>
    <LI><B>ls8_bad_days, s2a_bad_days, s2b_bad_days</B>. These lists contain
        the dates for which the satellite data shows cloud and are therefore
        flagged out. Initially these lists should be left blank.</LI>
    <LI><B>ls8_csvs, sent_csvs</B>. These lists contain the name of a CSV file
        that was created in the penultimate cell of the Site-Pipelines workflow.
        The CSV file contains an output of the summary fstat_df DataFrame and
        the summary field data contained within is used to plot against the
        satellite data. In order to generate data points for both Landsat and
        Sentinel, The corresponding Site-Pipelines workflow needs to be run
        twice: once with field_data[3] set to "Landsat8" and once with
        field_data[3] set to "Sentinel2a" or "Sentinel2b".</LI>
    <LI><B>rain_dat</B>. The string points to a CSV file in the Weather
        subdirectory, which contains historical rainfall data close to the field
        site. The data must be manually generated from the BOM website, as
        described below.</LI>
</OL>

### Generating rainfall CSV data

In this example, Blanchetown rainfall data is generated. The first step is to
download the closest rain gauge data over the time period 2013-present:
<OL>
    <LI>Go to the <A HREF=http://www.bom.gov.au/climate/data/index.shtml>BOM
        Climate Data Online</A> website.</LI>
    <LI>Above the map, click the tab "Select using text".</LI>
    <LI>Under point 2 "Select a weather station in the area of interest", enter
        the name of the place you are looking for and click "Find". If you
        do not know the name, it is also possible to search by position, using
        the button on the far right-hand-side.</LI>
    <LI>You will be presented with a list of matching towns. Click on the most
        appropriate one.</LI>
    <LI>You will be presented with a list of the nearest rainfall gauges. Click
        on the closest one. Below this, a small graph will show you the date
        range over which this station has been collecting rainfall data. If the
        station has not been collecting enough data in the period since 2013,
        you may need to pick another station.</LI>
    <LI>Once you have chosen the appropriate station, click on the "Get Data"
        button under step 3 (at the bottom of the page). This will take you to
        a daily rainfall spreadsheet for the current year.</LI>
    <LI>You can download all the rainfall data (all years) for the station by
        clicking on the link "All years of data", found in the top-right corner
        of the page. This will initiate downloading of a zip file, which, when
        expanded, contains a CSV file with all the relevant rainfall data.</LI>
</OL>
Once you have the CSV of the rainfall data, you should move it to a CSV
directory in the top level. For example, if you have the CSV file in the
MultiTimeLine directory, and you are in that directory:

    > mv IDCJAC0009_024564_1800_Data.csv ../CSV/

Note, you may need to first create the CSV directory ("mkdir ../CSV").

Now the workflow should be ready to run through the first time. So at the top
of the Jupyter notebook page, click on "Kernel" and then click on
"Restart & Run All", then "Restart and Run All Cells".<P>

### After the first run.

Once the notebook has run all the way through, you will now be able to see
satellite maps for each individual overpass and assess them for cloud
contamination. There are automatic cloud mistigation strategies available for
both Landsat and Sentinel products, but at the time of writing they are not
fool-proof and it is much more reliable to manually edit out contamination by
clouds/shadow/fog etc.<P>

To edit out contaminated data, look through the satellite images shown in Cells
[34], [35] and [36] (for Landsat 8, Sentinel 2a and 2b, respectively) and note
down the dates of contaminated images. Then transfer these dates to the three
lists in Cell [1] (ls8_bad_days, s2a_bad_days and s2b_bad_days). The format of
these lists should look something like:

ls8_bad_days = ['2013-04-13', '2013-04-29', '2013-05-06']

When you have updated all three lists, you can then re-run the entire notebook
and hopefully you will only be using good data. Note that all the data
(including contaminated days) will still be shown in Cells [34-36]. However,
Cell [39] will show the summary spectra for only good satellite data. If you
see suspiciously different spectra here, it might mean you have not flagged out
all the bad data. Also Cell [40] (MultiTimeLine plots) will help any
contaminated data to stand out.

### Understanding the outputs of the workflow

The original aim of the workflow was to assess how much a field site might
change between successive satellite overpasses. It quickly became evident that
there could be large, quick changes shortly following rainfall. But that most
field sites tend to return to their original state in a matter of days. With
this in mind, the characterisation of the field sites is done in two ways:
<OL>
    <LI>Look at the change in surface reflectance between successive overpasses
        for all available data.</LI>
    <LI>Look at the change in surface reflectance between successive overpasses
        for only data where the ground could be considered as unaffected by any
        recent rain.</LI>
</OL>
In order to address the second point, the workflow uses the rainfall data to
flag out any satellite data that occurs no more than 10 days after a rainfall
event at the field site. This is a rather conservative time-scale (3-5 days
appears to be the typical timescale to return to normal), but ensures that any
remaining data should not be affected by moisture except under the most extreme
circumstances. Unfortunately, this results in some field sites without very
much dry data at all, because it rains often at the field site. In such cases,
it is wise to fall back on the full dataset, including satellite overpasses
just after rain events. This necessarily increases the variability of a field
site.<P>

<IMG SRC='Misc/Example/BLA_22APR18_LS8_Fig18_MultiTimeLine.png'>Figure 18 shows an
example output for Blanchetown, using all data. The left-hand axis is rainfall
in millimetres and the right-hand axis is Surface Reflectance (SR). The faint,
grey histogram shows the amount of rainfall on a daily basis. The black dots
represent the Landsat 8 SR values. The blue dot represents the single field site
SR value. Vertical blue lines are separated by 10 days each. Blanchetown shows
a clear annual variability in all the bands. The workflow will also produce a
similar figure for Sentinel data (not shown), with green points for Sentinel 2a
and black points for Sentinel 2b. Note that data for Sentinel 2a typically only
goes back as far as 2015 and Sentinel 2b goes back as far as 2017.<P>

The workflow will also output results like the following:<BR>
```
LANDSAT 8: Number of adjacent overpasses: 113
Landsat 8 Surface Reflectance for Band 1 is 0.067+/-0.008 (12.17%)
Landsat 8 Surface Reflectance for Band 2 is 0.068+/-0.008 (11.23%)
Landsat 8 Surface Reflectance for Band 3 is 0.097+/-0.008 (8.28%)
Landsat 8 Surface Reflectance for Band 4 is 0.125+/-0.013 (10.01%)
Landsat 8 Surface Reflectance for Band 5 is 0.231+/-0.013 (5.75%)
Landsat 8 Surface Reflectance for Band 6 is 0.306+/-0.022 (7.07%)
Landsat 8 Surface Reflectance for Band 7 is 0.228+/-0.02 (8.85%)
```
These results mean that during the time period 2013-2018/October, there were
113 overpasses. For the Coastal Aerosol band, the average SR value is 0.067.
The standard deviation of the difference between successive overpasses is
0.008, which is about 12% of the SR value (0.067). This result tells us that we
can expect a variability of about 12% between successive Landsat 8 overpasses
(separated by 14 days) over the Blanchetown site, for the Coastal Aerosol band.
Statistics for the other bands are also reported.<P>

The above data are based on using ALL satellite data. However, below, we
consider only dry data. ie. the satellite overpass occurred more than 10 days
since the previous rainfall event.

<IMG SRC='Misc/Example/BLA_22APR18_LS8_Fig19_MultiTimeLine.png'>Figure 19
shows the same data as previously, but with all wet data flagged out. For the
case of Blanchetown, most of the data is flagged out, since Blanchetown
regularly experiences rain. Corresponding statistics are shown below:<BR>
```
LANDSAT 8: Number of adjacent overpasses: 24
Landsat 8 Surface Reflectance for Band 1 is 0.072+/-0.007 (9.65%)
Landsat 8 Surface Reflectance for Band 2 is 0.075+/-0.006 (7.57%)
Landsat 8 Surface Reflectance for Band 3 is 0.102+/-0.005 (5.09%)
Landsat 8 Surface Reflectance for Band 4 is 0.135+/-0.006 (4.45%)
Landsat 8 Surface Reflectance for Band 5 is 0.224+/-0.007 (3.27%)
Landsat 8 Surface Reflectance for Band 6 is 0.321+/-0.007 (2.3%)
Landsat 8 Surface Reflectance for Band 7 is 0.246+/-0.006 (2.46%)
```

The number of dry-only Landsat 8 overpasses is only 24, which means the
statistics will be somewhat less reliable. However, the statistics for the
Coastal Aerosol band are slightly better than previously, with an average
SR of 0.072 and standard deviation of about 10% (difference between successive
overpasses). If there are not enough overpasses to produce reliable statistics,
then 'NaN' will be returned, as is the case for Sentinel 2b standard deviation
for Blanchetown (not shown), as there were only 4 overpasses.

<BR><BR><BR>* Easy, but laborious.
