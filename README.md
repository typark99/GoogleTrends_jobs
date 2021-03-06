# GoogleTrends_jobs

This project is from the manuscript "Building Longitudinal Google Trends to Measure Dynamic Local-Level Issue Attention" by Taeyong Park, Haewoon Kwak, and Jisun An. The manuscript is available at http://www.taeyongpark.com/uploads/1/1/6/6/116640555/longitudinalgoogletrends1.pdf

CrossSection_jobs.py: This code is to collect DMA-level cross-sectional Google Trends indices for the jobs search term for the period between December 31, 2006 and December 31, 2016. DMA refers to the Designated Market Area, a geographic area where people receive the same television station offerings in the United States.

TimeSeries_jobs.py: This code is to collect the DMA-level time-series Google Trends indices for the jobs search term for the period between December 31, 2006 and December 31, 2016. Though this code generates 210 DMAs' jobs time-series, the manuscript only uses the Honolulu time-series as the reference for the rescaling method.

Rescale_jobs.ipynb: This Jupyter Notebook code is to rescale the cross-sectional jobs indices using the reference Honolulu time-series. This code corresponds to the second and third steps in the manuscript.

dma_googleid.tsv: This text data file includes individual DMAs' Google ID. This file is called in the Python code where needed.
