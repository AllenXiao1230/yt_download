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
        
        f = open('./cache/%s.jpg' % title,'wb')
        f.write(urllib.request.urlopen(f'{yt.thumbnail_url}').read())
        f.close()
        print("download successful")
        path='./cache/%s.jpg' % title

        total_time = time.strftime("%H:%M:%S", time.gmtime( float(yt.length) ))
        print(total_time,yt.views)
        date=str(yt.publish_date).split()[0]

        q_list = []
        qa_list = []
        #================

        for i in range(len(str(yt.streams.asc().filter(type='video',subtype='mp4')).split(','))):
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
        print(qa_list)
        
        #================
        #yt_stream=Stream('https://www.youtube.com/watch?v=XKEE0sW_lVg')
        
        return yt.title, path, total_time, yt.author, date, q_list, qa_list

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

def get_size(url,q):
    yt = YouTube(url)
    size = yt.streams.get_by_resolution('%s' % q).filesize
    return size
#def get_dl_info():

#get_info('https://www.youtube.com/watch?v=17C0QjEaqo0')