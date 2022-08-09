from pytube import YouTube, Playlist, Stream
import urllib.request
import string
import time
import natsort

def get_info(url):
    if 'watch' in url:
        yt = YouTube(url)
        
        title=yt.title
        punctuation_string = string.punctuation
        for i in punctuation_string:
            title = title.replace(i, '')
        

        total_time = time.strftime("%H:%M:%S", time.gmtime( float(yt.length) ))
        #print(total_time,yt.views)
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
        
        
        return yt.title,  total_time, yt.author, date, q_dict, qa_list
        
    elif 'playlist' in url:
        yt = Playlist(url)
        
        title=yt.title
        
        path='./resource/playlist.jpg'

        length=str(yt.length)+' Videos'
        
        date='Last Updated '+str(yt.last_updated)
        print(date)
        return yt.title, path, length, yt.owner, date
    else:
        print('error')



def onProgress(stream, chunk, remains):
        total = stream.filesize                     # 取得完整尺寸
        percent = (total-remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
        if percent != 100:
            print(f'下載中… {percent:05.2f}% ({remains}/{total})', end='\r')
        else:
            print(f'下載完成！ {percent:05.2f}% ({total}/{total})')

#get_info('https://www.youtube.com/watch?v=17C0QjEaqo0')