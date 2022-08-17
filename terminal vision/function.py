from pytube import YouTube, Playlist
import string
import time
import natsort
import colorama
from colorama import Fore
from colorama import Style


def get_info(url):
    if 'watch' in url:
        try:
            yt = YouTube(url)
            
            title=yt.title
            punctuation_string = string.punctuation
            for i in punctuation_string:
                title = title.replace(i, '')
            

            total_time = time.strftime("%H:%M:%S", time.gmtime( float(yt.length) ))
            
            date=str(yt.publish_date).split()[0]

            q_list = []
            qa_list = []
            #================

            for i in range(len(str(yt.streams.asc().filter(type='video',subtype='mp4', progressive=True)).split(','))):
                list_t=str(yt.streams.asc().filter(type='video',subtype='mp4')).split(',')[i].strip().split(" ")[3].strip('res="')
                q_list.append(list_t)

            q_list = list(set(q_list))
            q_list.sort()
            q_list = natsort.natsorted(q_list)

            #================

            for i in range(len(str(yt.streams.asc().filter(type='audio')).split(','))):
                list_t=str(yt.streams.asc().filter(type='audio')).split(',')[i].strip().split(" ")[3].strip('abr="')
                qa_list.append(list_t)

            qa_list = list(set(qa_list))
            qa_list.sort()
            qa_list = natsort.natsorted(qa_list)
            #print(qa_list)

            q_dict = {}
            for i in range(len(q_list)):
                q_dict[i+1] = q_list[i]
            
            qa_dict = {}
            for i in range(len(qa_list)):
                qa_dict[i+1] = qa_list[i]
            
            return yt.title,  total_time, yt.author, date, q_dict, qa_dict

        except:
            return 'error'

    elif 'playlist' in url:
        try:
            yt = Playlist(url)
            
            title=yt.title
            

            length=str(yt.length)
            
            
            date='Last Updated： '+str(yt.last_updated)
            
            return yt.title, length, yt.owner, date
        except:
            return 'error'

    else:
        return 'error'
def onProgress(stream, chunk, remains):

    total = stream.filesize                     # 取得完整尺寸
    percent = (total-remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
    all = '%.2f' % (int(total) / 1048576)
    l = '%.2f' % (int(total-remains) / 1048576)

    if percent != 100:
        i = round(round(percent) / 2)
        print(Fore.YELLOW + '下載中...  '+f'[{"■"*i}{" "*(50-i)}]' + f' {percent:05.2f}% ({l} MB / {all} MB)', end='\r')
        
    else:
        print(Fore.GREEN +'下載完成！ '+f'[{"■"*50}]'+f' {percent:05.2f}% ({all} MB/ {all} MB)\n' + Style.RESET_ALL)
    




#get_info('https://www.youtube.com/watch?v=gyknMNfPaKU')▬▮■■▮▮▬▬■■■■