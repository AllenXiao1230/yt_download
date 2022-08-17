from importlib.resources import path
from pytube import YouTube, Playlist
from colorama import Fore
from colorama import Style
from colorama import*

from function import*

print(Fore.BLUE + Style.BRIGHT  +'\n\n歡迎使用Youtube下載工具 (終端機版本)'+ Style.RESET_ALL)

def start():
    print('\n請輸入網址：' + Fore.MAGENTA)
    

    url = input()
    print(Style.RESET_ALL)

    if url == 'error':
        print(Fore.RED +'發生錯誤，請重新輸入'+ Style.RESET_ALL)
        start()

    print(Style.BRIGHT + Fore.YELLOW+'搜尋中...'+ Style.RESET_ALL)

    if 'watch' in url:

        result = get_info(url)
        print(Fore.CYAN + Style.BRIGHT +'\n影片資訊：\n==================================================\n')
        print(result[0],'\n\n' + result[2]+' ｜ ' + result[1])
        print('\n=================================================='+ Style.RESET_ALL)
        ask_yn = input('是否為這部影片(y/n)：' + Fore.MAGENTA)
        print(Style.RESET_ALL)

        if ask_yn == 'y':

            type = input(Style.RESET_ALL + '選擇下載類型：\n1. mp4\n2. mp3\n' + Fore.MAGENTA)
            print(Style.RESET_ALL)
            if str(type) == '1' or str(type) == 'mp4':
                
                download(url)

            elif str(type) == '2' or str(type) == 'mp3':

                download_music(url)

            start()

        else:
            start()

    elif 'playlist' in url:
        result = get_info(url)
        print(Fore.CYAN + Style.BRIGHT + '\n播放清單資訊：\n==================================================\n')
        print( result[0],'\n\n' + result[1]+' Videos'+' ｜ ' + result[2]+' ｜ '+result[3])
        print('\n==================================================' + Style.RESET_ALL)
        ask_yn = input('是否為這份播放清單(y/n)：' + Fore.MAGENTA)
        print(Style.RESET_ALL)

        if ask_yn == 'y':

            type = input(Style.RESET_ALL + '選擇下載類型：\n1. mp4\n2. mp3\n' + Fore.MAGENTA)
            print(Style.RESET_ALL)
            if str(type) == '1' or str(type) == 'mp4':
                download_list(url,result[1])
            
            elif str(type) == '2' or str(type) == 'mp3':
                download_list_music(url,result[1])

            start()

        else:
            start()



def download(url):

    yt = YouTube(url, on_progress_callback=onProgress)
    print(Fore.YELLOW + '開始下載！' + Style.RESET_ALL)

    try:
        yt.streams.filter().get_highest_resolution().download()
        

    except:
        print(Fore.RED +'發生錯誤，此影片無法下載！'+ Style.RESET_ALL)
        print()
        pass


def download_list(url,len):

    playlist = Playlist(url)

    for i in playlist.video_urls:

        yt= YouTube(i, on_progress_callback=onProgress)
        print(Fore.YELLOW + '開始下載：'+ Style.RESET_ALL,yt.title)

        try:
            yt.streams.filter().get_highest_resolution().download()

        except:
            print(Style.BRIGHT + Fore.RED +'發生錯誤，此影片無法下載！'+ Style.RESET_ALL)
            pass

    print(Style.BRIGHT + Fore.GREEN + '\n'+str(len),'部影片完成下載！'+ Style.RESET_ALL)


def download_music(url):

    yt = YouTube(url, on_progress_callback=onProgress)
    print(Fore.YELLOW + '開始下載！' + Style.RESET_ALL)

    try:
        yt.streams.filter().get_audio_only().download()
        
    except:
        print(Style.BRIGHT + Fore.RED +'發生錯誤，此音樂無法下載！'+ Style.RESET_ALL)
        pass


def download_list_music(url,len):

    playlist = Playlist(url)

    for i in playlist.video_urls:

        yt= YouTube(i, on_progress_callback=onProgress)
        print(Fore.YELLOW + '開始下載：'+ Style.RESET_ALL,yt.title)

        try:
            yt.streams.filter().get_audio_only().download()

        except:
            print(Style.BRIGHT + Fore.RED +'發生錯誤，此音樂無法下載！'+ Style.RESET_ALL)
            pass

    print(Style.BRIGHT + Fore.GREEN + '\n' + str(len),'首音樂完成下載'+ Style.RESET_ALL)


start()
