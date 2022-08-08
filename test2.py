from pytube import YouTube, Playlist, Stream
from tkinter import*
def test_dowmload(url, q, value):
    
    app = Tk()
    yt = YouTube(url, on_progress_callback=onProgress)
    yt.streams.get_by_resolution(q).download(output_path=value)
    app.mainloop()
def onProgress(stream, chunk, remains, *args, **kwargs):
    total = stream.filesize                     # 取得完整尺寸
    percent = (total-remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
    print(f'下載中… {percent:05.2f}', end='\r')

