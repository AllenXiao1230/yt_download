

from pytube import YouTube
yt = YouTube('https://www.youtube.com/watch?v=R93ce4FZGbc')
print('download...')
yt.streams.filter().get_by_resolution('1080p').download(filename='oxxostudio_360p.mp4')
# 下載 480p 的影片畫質
print('ok!')