#coding:utf-8

# %% imports
# from nowcast.configure import AEScryptoConfigParser
# from nowcast.notification import SlackWebhookHandler
import shutil
import subprocess
import tempfile
import imp

#region basic import section
import codecs
import datetime
from decimal import Decimal
import glob
import math
import numpy as np
import os
from os import path
import pandas as pd
import sys
import time
import traceback
from typing import Any, List, Dict
#endregion

#region logging section
import logging
from logging import getLogger, StreamHandler, FileHandler
loggers = {} # type: Dict[str, logging.Logger]
def SetLogger(name: str)->logging.Logger:
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:
        logger = getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
        slackFormatter = logging.Formatter('@channel\n%(asctime)s - %(levelname)s : %(message)s')

        fhandler = FileHandler(filename = logPath)
        fhandler.setLevel(logging.DEBUG)
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)

        shandler = StreamHandler()
        shandler.setLevel(logging.INFO)
        shandler.setFormatter(formatter)
        logger.addHandler(shandler)

        #slackhandler = SlackWebhookHandler(config.get('log', 'hookURL'), 'SKUsource Nikkei format Bot', ':skull_and_crossbones:')
        #slackhandler.setLevel(logging.WARNING)
        #slackhandler.setFormatter(slackFormatter)
        #logger.addHandler(slackhandler)
        #loggers.update(dict(name=logger))

        return logger
#endregion

# %% config
#region constants section
delimiter = ','
thisCodec = 'cp932'
newLine = '\n'
dt = pd.DateOffset(months=12)
#endregion

# %% deffinitions
def loadDataSource(source: str, isBase: bool)->pd.DataFrame:
    # source = r'C:\temp\Lproject\extract\A\Weekly\A_20160905.csv'
    # thisDF.head()
    thisDF = pd.read_csv(source, encoding=thisCodec, header=None, dtype={0: "object", 1: "object", 2: "object", 3: "object", 4: "object", 5: "object", 6: "object", 7: "object", 8: "object",
                                                                            9: "float", 10: "float"})
    thisDF.rename(columns={0: 'date', 1: 'LPOINT_KEY', 2: 'STORECODE', 3: 'PD_HLV_C', 4: 'PD_MCLS_C', 5: 'PD_SCLS_C', 6: 'MA_FEM_DV_C', 7: 'CST_AGE_PRD', 8: 'HIST_SEG', 9: 'BUY_AM', 10: 'BUY_CT'}, inplace=True)
    thisDF.date = pd.to_datetime(thisDF.date, format="%Y%m")

    if isBase:
        thisDF['matchKey'] = (thisDF.date + dt).dt.strftime('%Y%m') + ',' + thisDF.LPOINT_KEY + ',' + thisDF.STORECODE
    else:
        thisDF['matchKey'] = thisDF.date.dt.strftime('%Y%m') + ',' + thisDF.LPOINT_KEY + ',' + thisDF.STORECODE
    thisDF['category'] = thisDF.PD_HLV_C + '-' + thisDF.PD_MCLS_C + '-' + thisDF.PD_SCLS_C
    thisDF = thisDF[['date', 'STORECODE', 'category', 'matchKey', 'BUY_AM', 'BUY_CT']].groupby(['date', 'STORECODE', 'category', 'matchKey'], as_index=False ).agg({'BUY_AM': 'sum', 'BUY_CT': 'sum'})

    thisDF['unitPrice'] = thisDF.BUY_AM / thisDF.BUY_CT

    return thisDF
    pass # def

def makeDirectory(filepath: str):
    if not os.path.exists(path.dirname(path.join(filepath))):
        try:
            os.makedirs(path.dirname(path.join(filepath)))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    return

# %% main
if __name__ == '__main__':
    start = time.time()
    now = datetime.datetime.now()

    allianceCode = 'A'
    sourcePath = r"F:\FlatData\L.POINT\phase2_2\converted\A\Outliers_removed\Sliced_monthly"
    destinationPath = r"F:\FlatData\L.POINT\phase2_2\result\A\sliced_yoy"
    logPath = path.join(destinationPath, 'index_{0:%Y%m%d}.log'.format(now))
    logger = SetLogger(__name__)
    logger.info(now)


    for roots1, slices, filenames1 in os.walk(sourcePath):
        for slice in slices:

            for roots2, keys, filenames2 in os.walk(path.join(sourcePath, slice)):
                for key in keys:

                    try:
                        startDate = datetime.datetime(2013, 12, 1)
                        endDate = datetime.datetime(2018, 2, 1)

                        thisDate = startDate
                        while thisDate <= endDate:
                            baseDate = thisDate - dt
                            logger.info(allianceCode+'-'+slice+key+'progress:t{},t-dt:{}'.format(thisDate.strftime("%Y/%m"), baseDate.strftime("%Y/%m")))

                            tFile = path.join(sourcePath, slice, key, allianceCode + '_tot_master_{:%Y%m}.csv'.format(thisDate))
                            t_dtFile = path.join(sourcePath, slice, key, allianceCode + '_tot_master_{:%Y%m}.csv'.format(baseDate))

                            if path.exists(tFile) and path.exists(t_dtFile):
                                tDF = loadDataSource(tFile, False)
                                t_dtDF = loadDataSource(t_dtFile, True)

                                # level 1
                                matched = pd.merge(tDF, t_dtDF, on='matchKey', suffixes=['_t','_t_dt'])
                                shareDeno_t = matched[['date_t', 'STORECODE_t', 'category_t', 'BUY_AM_t']].groupby(['date_t', 'STORECODE_t', 'category_t'], as_index=False).sum()
                                shareDeno_t.columns = ['date_t', 'STORECODE_t', 'category_t', 'sum_A_t']
                                shareDeno_t_dt = matched[['date_t', 'STORECODE_t', 'category_t', 'BUY_AM_t_dt']].groupby(['date_t', 'STORECODE_t', 'category_t'], as_index=False).sum()
                                shareDeno_t_dt.columns = ['date_t', 'STORECODE_t', 'category_t',  'sum_A_t_dt']

                                weighted = pd.merge(matched, shareDeno_t, on=['date_t', 'STORECODE_t', 'category_t'], how='left')
                                weighted = pd.merge(weighted, shareDeno_t_dt, on=['date_t', 'STORECODE_t', 'category_t'], how='left')

                                weighted['r'] = np.log(weighted.unitPrice_t / weighted.unitPrice_t_dt)
                                weighted['st'] = weighted.BUY_AM_t / weighted.sum_A_t
                                weighted['st_dt'] = weighted.BUY_AM_t_dt / weighted.sum_A_t_dt
                                weighted['wt'] = (weighted.st + weighted.st_dt) / 2
                                weighted['wt_r'] = weighted.wt * weighted.r

                                level1 = weighted.groupby(['date_t', 'STORECODE_t', 'category_t'], as_index=False).agg({'BUY_AM_t': 'sum', 'BUY_AM_t_dt': 'sum', 'wt_r': 'sum', 'matchKey': pd.Series.nunique})
                                level1.columns = ['date', 'STORECODE', 'category', 'sum_A_t', 'sum_A_t_dt', 'i_o_c', 'unique']
                                makeDirectory(path.join(destinationPath, slice, key, 'level1_{:%Y%m}.csv'.format(thisDate)))
                                with codecs.open(path.join(destinationPath, slice, key, 'level1_{:%Y%m}.csv'.format(thisDate)), 'w', thisCodec) as writer:
                                    level1[['date', 'STORECODE', 'category', 'unique', 'sum_A_t', 'sum_A_t_dt', 'i_o_c']].to_csv(writer, header = True, index=False)

                                # level 2
                                shareDeno = level1[['date', 'category', 'sum_A_t', 'sum_A_t_dt']].groupby(['date', 'category'], as_index=False).agg({'sum_A_t': 'sum', 'sum_A_t_dt': 'sum'})
                                shareDeno.columns = ['date', 'category', 'deno_t',  'deno_t_dt']
                                level1 = pd.merge(level1, shareDeno, on=['date', 'category'], how='left')
                                level1['st'] = level1.sum_A_t / level1.deno_t
                                level1['st_dt'] = level1.sum_A_t_dt / level1.deno_t_dt
                                level1['wt'] = (level1.st + level1.st_dt) / 2
                                level1['wt_i'] = level1.wt * level1.i_o_c

                                level2 = level1.groupby(['date', 'category'], as_index=False).agg({'unique': 'sum', 'sum_A_t': 'sum', 'sum_A_t_dt': 'sum', 'wt_i': 'sum'})
                                level2.columns = ['date', 'category', 'unique', 'sum_A_t', 'sum_A_t_dt', 'i_c']
                                makeDirectory(path.join(destinationPath, slice, key, 'level2_{:%Y%m}.csv'.format(thisDate)))
                                with codecs.open(path.join(destinationPath, slice, key, 'level2_{:%Y%m}.csv'.format(thisDate)), 'w', thisCodec) as writer:
                                    level2[['date', 'category', 'unique', 'sum_A_t', 'sum_A_t_dt', 'i_c']].to_csv(writer, header = True, index=False)

                                # level 3
                                shareDeno = level2[['date', 'sum_A_t', 'sum_A_t_dt']].groupby(['date'], as_index=False).agg({'sum_A_t': 'sum', 'sum_A_t_dt': 'sum'})
                                shareDeno.columns = ['date', 'deno_t',  'deno_t_dt']
                                level2 = pd.merge(level2, shareDeno, on=['date'], how='left')
                                level2['st'] = level2.sum_A_t / level2.deno_t
                                level2['st_dt'] = level2.sum_A_t_dt / level2.deno_t_dt
                                level2['wt'] = (level2.st + level2.st_dt) / 2
                                level2['wt_i'] = level2.wt * level2.i_c

                                level3 = level2.groupby(['date'], as_index=False).agg({'unique': 'sum', 'sum_A_t': 'sum', 'sum_A_t_dt': 'sum', 'wt_i': 'sum'})
                                level3.columns = ['date', 'unique', 'sum_A_t', 'sum_A_t_dt', 'i']
                                makeDirectory(path.join(destinationPath, slice, key, 'level3_{:%Y%m}.csv'.format(thisDate)))
                                with codecs.open(path.join(destinationPath, slice, key, 'level3_{:%Y%m}.csv'.format(thisDate)), 'w', thisCodec) as writer:
                                    level3[['date', 'unique', 'sum_A_t', 'sum_A_t_dt', 'i']].to_csv(writer, header = True, index=False)
                                pass # end if
                            thisDate += pd.DateOffset(months=1)
                            pass # while

                    except Exception as e:
                        logger.critical('[%s]: %s\n%s' % (type(e) ,e.args, traceback.format_exc()))
                    finally:
                        pass
