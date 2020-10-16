from pytrends.request import TrendReq
import datetime
from dateutil.relativedelta import relativedelta
import time
import os
from urllib.parse import quote_plus
import logging
import itertools

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

# US CST https://pypi.org/project/pytrends/
pytrend = TrendReq(hl='en-US', tz=360) 

resolution = "DMA"

directory2keywords = {
    "jobs": ["jobs"], 
}

directory2period = {
    "jobs": (datetime.date(2006,12,31), datetime.date(2016,12,31))
}

# weekly
TIME_WINDOW = 7

try:
    os.mkdir("by_region")
except:
    pass

for keyword_for_directory in directory2keywords:
    logger.info("keyword_for_directory: {}".format(keyword_for_directory))
    keywords = directory2keywords[keyword_for_directory]
    keywords_indexes = list(range(0,len(keywords)))
    START_TIME, END_TIME = directory2period[keyword_for_directory]

    MAX_LENGTH = -1

    if not os.path.exists("by_region/" + keyword_for_directory):
        os.mkdir("by_region/" + keyword_for_directory)       

    # generate keyword combinations
    for r in range(1,len(keywords)+1): 
        for selected in list(itertools.combinations(keywords_indexes, r)):
            current_datetime = START_TIME            
            keyword = "+".join([keywords[i] for i in selected])
            logger.debug(keyword)
            if MAX_LENGTH != -1 and len(keyword) > MAX_LENGTH:
                logger.debug("len(keyword)[{}] is longer than MAX_LENGTH[{}]".format(len(keyword), MAX_LENGTH))
                continue

            # send queries from START_TIME to END_TIME
            while True:
                if current_datetime > END_TIME:
                    break
                current_end_time = current_datetime + datetime.timedelta(days=TIME_WINDOW-1)
                if os.path.exists("by_region/{}/{}-{}-{}-{}-by_region.csv".format(keyword_for_directory,"_".join([str(s) for s in selected]), resolution, current_datetime.strftime("%Y%m%d"), current_end_time.strftime("%Y%m%d"))):
                    logger.debug("by_region/{}/{}-{}-{}-{}-by_region.csv is collected...".format(keyword_for_directory,"_".join([str(s) for s in selected]), resolution, current_datetime.strftime("%Y%m%d"), current_end_time.strftime("%Y%m%d"))) 
                    current_datetime += datetime.timedelta(days=TIME_WINDOW)   
                    continue

                try:
                    pytrend.build_payload(kw_list=[keyword], geo="US", 
                                        timeframe='%s %s' % (current_datetime.strftime("%Y-%m-%d"), current_end_time.strftime("%Y-%m-%d"))) 
                    time.sleep(15)
                    df = pytrend.interest_by_region(resolution=resolution)
                    time.sleep(15)
                except:
                    logger.error("error", exc_info=1)
                    MAX_LENGTH = len(keyword)
                    time.sleep(120)

                df.to_csv("by_region/{}/{}-{}-{}-{}-by_region.csv".format(keyword_for_directory,"_".join([str(s) for s in selected]), resolution, current_datetime.strftime("%Y%m%d"), current_end_time.strftime("%Y%m%d")))
                current_datetime += datetime.timedelta(days=TIME_WINDOW)