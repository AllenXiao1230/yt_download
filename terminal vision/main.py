from importlib.resources import path
from pytube import YouTube, Playlist, Stream
import hashlib
import time
import subprocess
import configparser
import os

import natsort

from function import*

print('歡迎使用Youtube下載工具 (終端機版本)\n')

def start():
    print('請輸入網址：')
    url = input()
    print('搜尋中...')
    result = get_info(url)
    print('\n影片資訊：\n==================================================\n')
    print(result[0],'\n\n'+result[2]+' ｜ '+result[1])
    print('\n==================================================')
    ask_yn = input('是否為這部影片(y/n)：')

    if ask_yn == 'y':
        q_str = str(result[4]).strip("{}")
        q_str = ' ' + q_str
        print('\n此影片提供的畫質：')
        
        for i in range(len(q_str.split(","))):
            print(q_str.split(",")[i])

        quantity = input('選擇下載畫質(請輸入編號)：')
        quantity = result[4].get(int(quantity))
        
        
        download(url, quantity)
        
        start()
    else:
        start()

def download(url, quantity):
    qua = str(quantity)
    yt = YouTube(url, on_progress_callback=onProgress)
 
    try:
        yt.streams.filter(subtype='mp4',resolution='1080p')[0].download()
        print('開始下載!')
    except AttributeError:
        print('此畫質暫不提供下載')
        pass

start()