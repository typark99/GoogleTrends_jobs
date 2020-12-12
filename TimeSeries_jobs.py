from pytrends.request import TrendReq
import datetime
from dateutil.relativedelta import relativedelta
import time
import os
from urllib.parse import quote_plus
import logging
import itertools


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

# US CST https://pypi.org/project/pytrends/
pytrend = TrendReq(hl='en-US', tz=360) 

TIME_WINDOW = 1883

directory2keywords = {
    "jobs": ["jobs"], 
}

directory2period = {
    "jobs": (datetime.date(2006,12,31), datetime.date(2016,12,31))
}

import pandas as pd

# Load a mapping file between Google's internal ID and DMA
import sys
df = pd.read_table(os.path.join(sys.path[0], 'dma_googleid.tsv'), sep="\t")

for r_index, row in df.iterrows():
    GEO = row['googleid']
    logger.info("[{}] {}".format(r_index, GEO, row['dma']))
    for keyword_for_directory in directory2keywords:

        logger.debug("keyword_for_directory: {}".format(keyword_for_directory))
        keywords = directory2keywords[keyword_for_directory]
        keywords_indexes = list(range(0,len(keywords)))
        START_TIME, END_TIME = directory2period[keyword_for_directory]
        if (END_TIME-START_TIME).days < TIME_WINDOW:
            TIME_WINDOW = (END_TIME - START_TIME).days 
            logger.debug("TIME_WINDOW is adjusted [{}]".format(TIME_WINDOW))

        try:
            os.mkdir("over_time-{}".format(TIME_WINDOW))
        except:
            pass

        MAX_LENGTH = -1

        if not os.path.exists("over_time-{}".format(TIME_WINDOW) + "/" + keyword_for_directory):
            os.mkdir("over_time-{}".format(TIME_WINDOW) + "/" + keyword_for_directory)       

        # generate keyword combinations
        for r in range(1,len(keywords)+1):
            for selected in list(itertools.combinations(keywords_indexes, r)):
                current_datetime = START_TIME  
                end_time = (current_datetime + datetime.timedelta(days=TIME_WINDOW))          
                if end_time > END_TIME:
                    end_time = END_TIME
                    TIME_WINDOW = (END_TIME - START_TIME).days
                keyword = "+".join([keywords[i] for i in selected])
                if MAX_LENGTH != -1 and len(keyword) > MAX_LENGTH:
                    logger.info("len(keyword)[{}] is longer than MAX_LENGTH[{}]".format(len(keyword), MAX_LENGTH))
                    continue
                    
                # send queries from START_TIME to END_TIME
                while True:
                    if current_datetime >= END_TIME:
                        break
                    
                    if os.path.exists("over_time-{}".format(TIME_WINDOW) + "/" + "{}/{}-{}-{}-{}-over_time.csv".format(keyword_for_directory,"_".join([str(s) for s in selected]), GEO, current_datetime.strftime("%Y%m%d"), end_time.strftime("%Y%m%d"))):
                        logger.info("over_time-{}".format(TIME_WINDOW) + "/" + "{}/{}-{}-{}-{}-over_time.csv is collected...".format(keyword_for_directory,"_".join([str(s) for s in selected]), GEO, current_datetime.strftime("%Y%m%d"), end_time.strftime("%Y%m%d"))) 
                        current_datetime += datetime.timedelta(days=TIME_WINDOW)  
                        end_time = (current_datetime + datetime.timedelta(days=TIME_WINDOW))          
                        if end_time > END_TIME:
                            end_time = END_TIME     
                        continue

                    try:
                        pytrend.build_payload(kw_list=[keyword], geo=GEO, 
                                            timeframe='%s %s' % (current_datetime.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d"))) 
                        time.sleep(20)
                        df = pytrend.interest_over_time()
                    except:
                        logger.error("error", exc_info=1)
                        MAX_LENGTH = len(keyword)
                        time.sleep(120)


                    df.to_csv("over_time-{}".format(TIME_WINDOW) + "/" + "{}/{}-{}-{}-{}-over_time.csv".format(keyword_for_directory,"_".join([str(s) for s in selected]), GEO, current_datetime.strftime("%Y%m%d"), end_time.strftime("%Y%m%d")))
                    current_datetime += datetime.timedelta(days=TIME_WINDOW)  
                    end_time = (current_datetime + datetime.timedelta(days=TIME_WINDOW))          
                    if end_time > END_TIME:
                        end_time = END_TIME     

                    time.sleep(60)                                   
