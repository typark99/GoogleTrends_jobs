# GoogleTrends_jobs

This project is from the manuscript "Building Longitudinal Google Trends to Measure Dynamic Local-Level Issue Attention" (Taeyong Park, Haewoon Kwak, and Jisun An). The manuscript is available at http://www.taeyongpark.com/uploads/1/1/6/6/116640555/longitudinal_searches_ver3.pdf This manuscript is under review, and please do not cite.

The code crawl_search_snapshots_combined.py is to collect the DMA-level cross-sectional Google Trends indices for the jobs search term for the period between December 31, 2006 and December 31, 2016. DMA refers to the Designated Market Area, a geographic area where people receive the same television station offerings in the United States.

The code crawl_search_over_time_dma.py is to collect the DMA-level time-series Google Trends indices for the jobs search term for the period between December 31, 2006 and December 31, 2016.

The code Recale-combined.ipynb is to rescale the cross-sectional jobs indices using the Honolulu time-series jobs indices. This code is for the second and third steps in the manuscript.