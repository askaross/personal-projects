# %%
import pandas as pd
import numpy as np
import glob
import os
from os import path
import sys
import csv
import codecs
sys.path.append('scripts')
from settings import ROOT_DIR,DATA_DIR,APPS_DIR,OUTPUT_DIR

app_master_path = path.join(APPS_DIR,'app_master.tsv')
install_dir = path.join(APPS_DIR,'install')

app_daily_install_path = path.join(install_dir,'appinstallinfo_summary_daily.csv')
all_apps_daily_user_path = path.join(install_dir,'app_install_total_sample_count.xlsx')

# app_list_path = path.join(APPS_DIR,'apps_top10K.XLSX')
app_list_path = path.join(APPS_DIR,'sort_10K_applist.xlsx')

first_chosen_applist_path = path.join(APPS_DIR,'first_app_list.xlsx')

# Test

# %%
def error_explore(fpath,sep):
    wrong_list =[]
    with codecs.open(fpath,mode='r',encoding='utf-8',errors='strict') as reader:
        header = next(reader)
        len_header = len(header.split(sep))
        count=1

        try:

            for line in reader:
                if len(line.split(sep))!=len_header:
                    wrong_list.append(line)
                count+=1

        except:
            print('stopped at: ', count)

    return count,len_header,wrong_list


# %% master clean
def read_master():
    with codecs.open(app_master_path,mode='r',encoding='utf-8',errors='ignore') as reader:
        df=pd.read_table(reader,sep='\t')
        df = df.iloc[:-1]
    df.sort_values(by=['package','crawl_date'], inplace=True)
    df.drop_duplicates(subset=['package'],keep='last',inplace=True)

    return df


# %% アプリインストールデータ
# 個別データ

def read_installation_data():
    # 個別のファイルread
    with codecs.open(app_daily_install_path,mode='r',encoding='utf-8',errors='ignore') as reader:
        df=pd.read_table(reader,sep='|')
        df = df.iloc[:-1]
        df.sort_values(by=['package','accessdate_day'], inplace=True)
        df['accessdate_day']= pd.to_datetime(df['accessdate_day'])
        df.rename(columns={'num_of_samples':'inst_user_counts'},inplace=True)

    # 割り算のための全体データ
    all_user = pd.read_excel(all_apps_daily_user_path, skiprows=2)
    all_user = all_user[['date_trunc','num_of_samples']]
    # merge

    # print('shape before: ', df.shape)
    df = pd.merge(left=df, right=all_user, how='inner', left_on=['accessdate_day'], right_on=['date_trunc'])
    # print('shape after: ', df.shape)
    df['install_rate'] = df['inst_user_counts']/df['num_of_samples']

    df.sort_values(by=['package','accessdate_day'], inplace=True)

    return df


# %%
def read_app_rank_list():
    app_list = pd.read_excel(app_list_path)
    app_list.sort_values('app_rank',inplace=True)
    # print('before shape: ',app_list.shape)
    app_list = pd.merge(left=app_list, right=master_df, how='left', on=['package'],suffixes=('', '_master'))
    # print('after shape: ',app_list.shape)

    #
    # print(app_list['app_type1_en'].value_counts())
    # print(app_list['category1_en'].value_counts())

    apptype_cate=app_list.groupby(['app_type1_en','category1_en']).size()
    # apptype_cate.loc[('APPLICATION',)]
    # apptype_cate.loc[('GAME',)]

    app_list['type_cate_rank'] = app_list.groupby(['app_type1_en','category1_en'])['app_rank'].rank()
    app_list = app_list[['package','app_name','creator','app_type1_en','category1_en','app_rank','type_cate_rank']]
    app_list_cut = app_list[(app_list.app_rank<=800)&(app_list.type_cate_rank<=5)]
    apptype_cate_cut=app_list_cut.groupby(['app_type1_en','category1_en']).size()

    spath = path.join(OUTPUT_DIR,'selected_apps.csv')
    app_list_cut.to_csv(spath,encoding='utf-8')

    return app_list_cut,apptype_cate_cut,apptype_cate


def read_location_data():
    loc_h_path = os.path.join(DATA_DIR, 'location','location_hourly_summary_20180628_revised.csv')

    with codecs.open(loc_h_path,mode='r',encoding='cp932',errors='strict') as reader:
        df = pd.read_table(reader,sep=',')
        df = df.iloc[:-1]

    transl_path = os.path.join(DATA_DIR, 'location','building_translation_map.csv')
    with codecs.open(transl_path,mode='r',encoding='utf-8',errors='strict') as reader:
        transl_df = pd.read_table(reader,sep=',')

    mdf  = pd.merge(left=df, right=transl_df, on=['building_name'], how='inner')
    mdf.sort_values(['building_name_en','day_aggregated','hour_aggregated'], inplace=True)

    return mdf


# %%

if __name__ == '__main__':
    # %% master data
    count,len_h,wrong_list = error_explore(app_master_path,'\t')
    print(count)
    print(len_h)
    print(wrong_list)
    master_df = read_master()

    # %% アプリインストールデータ
    # 個別データ
    count,len_h,wrong_list = error_explore(app_daily_install_path,'|')
    print(count)
    print(len_h)
    print(wrong_list)
    inst_df = read_installation_data()
    # inst_df = pd.merge(left=inst_df, right=master_df, how='inner', on=['package'])

    # app_rank_list
    app_list_cut,apptype_cate_cut,apptype_cate = read_app_rank_list()

    rank_list = set(app_list_cut.package.tolist())


    first_applist_df = pd.read_excel(first_chosen_applist_path)
    first_list = set(first_applist_df.package.tolist())

    # 今回に入っているけど，最初はなかったもの
    here_in_not_first= app_list_cut[app_list_cut.package.apply(lambda x: x not in first_list)]
    spath = path.join(OUTPUT_DIR,'here_in_not_first.csv')
    here_in_not_first.to_csv(spath,encoding='utf-8')

    # 最初はあったけど，今回ないもの
    first_in_not_here= first_applist_df[first_applist_df.package.apply(lambda x: x not in rank_list)]
    spath = path.join(OUTPUT_DIR,'first_in_not_here.csv')
    first_in_not_here.to_csv(spath,encoding='utf-8')


    # len(rank_list)
    # len(first_list)
    # len(rank_list&first_list)
    # rank_list-first_list
