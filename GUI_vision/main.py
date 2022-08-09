from importlib.resources import path
from tkinter import*
import hashlib
import time
import subprocess
import configparser
from tkinter import filedialog
from tkinter import font
from tkinter import scrolledtext
from tkinter.font import*
import os
import tkinter.ttk as ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

import natsort
from pytube import YouTube, Playlist, Stream
import urllib.request
import string
LOG_LINE_NUM = 0


class MY_GUI(Frame):
    def __init__(self,init_window_name, *args, **kwargs):
        
        self.main_window = init_window_name
        self.config = configparser.ConfigParser()
        self.fontStyle = Font(family='Microsoft JhengHei UI',size=12)
        self.titleStyle = Font(family='Microsoft JhengHei UI',size=14,weight='bold')
        self.normalfont = Font(family='Microsoft JhengHei UI')
        self.infoStyle = Font(family='Microsoft JhengHei UI',size=9)
        
    #定義主要視窗
    def set_init_window(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.main_window.title("Youtube下載工具 V1.0")
        self.main_window.geometry('750x681')
        self.main_window.resizable(0, 0)

        menubar = Menu(self.main_window) #創建選單欄
        
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='開啟儲存資料夾',command=self.open_folder,font=self.normalfont)
        filemenu.add_separator() 
        filemenu.add_command(label='退出',command=self.main_window.destroy,font=self.normalfont)
        menubar.add_cascade(label="檔案", menu=filemenu,font=self.normalfont)

        settingmenu = Menu(menubar, tearoff=0)
        settingmenu.add_command(label='應用設定',font=self.normalfont)
        settingmenu.add_command(label='說明',font=self.normalfont)
        menubar.add_cascade(label="設定與說明", menu=settingmenu,font=self.normalfont)

        self.main_window.config(menu=menubar) #綁定選單
        
        #================

        self.link_frame = ttk.LabelFrame(self.main_window,text="鏈結")
        self.link_frame.grid(row=0, column=0,padx=15,pady=10, columnspan=5, sticky=W,ipadx=7)
        #标签
        self.text1 = ttk.Label(self.link_frame, text="YouTube網址：",font=self.fontStyle)
        self.text1.grid(row=0, column=0,padx=10,pady=10)
        
        #文本框
        self.link_entry = ttk.Entry(self.link_frame, width=47,font=self.normalfont)
        self.link_entry.grid(row=0, column=1,padx=5,pady=10)
        
        #按钮
        self.start_button = ttk.Button(self.link_frame, text="解析", width=15,command=self.start)
        self.start_button.grid(row=0, column=2,padx=5,pady=10)
        
        #================

        self.info_frame = ttk.LabelFrame(self.main_window,text="影片資訊")
        self.info_frame.grid(row=1, column=0,padx=15,pady=10, columnspan=3, sticky=W, ipadx=180)

        self.photo = ttk.Label(self.info_frame)
        self.photo.grid(row=0, column=0, rowspan=3, sticky=W)

        self.video_title = ttk.Label(self.info_frame,text="",font=self.titleStyle,wraplength=300,foreground='mediumblue')
        self.video_title.grid(row=0, column=1,padx=5,sticky=N)

        self.info_label = ttk.Label(self.info_frame,text="",font=self.infoStyle,wraplength=500)
        self.info_label.grid(row=1, column=1,padx=5, sticky=W)

        self.info_label1 = ttk.Label(self.info_frame,text="",font=self.infoStyle,wraplength=500)
        self.info_label1.grid(row=2, column=1,padx=5, sticky=W)

        #================

        self.config_frame = ttk.LabelFrame(self.main_window,text="下載配置")
        self.config_frame.grid(row=1, column=3,pady=10, columnspan=2, sticky=W, ipadx=10)
        
        self.qt_text = ttk.Label(self.config_frame,text="副檔名：",font=self.fontStyle)
        self.qt_text.grid(row=0,column=0,padx=10)

        self.video_type = ttk.Combobox(self.config_frame)
        self.video_type.grid(row=0,column=1,pady=10)

        self.video_type.bind('<<ComboboxSelected>>', self.combo_q)

        self.qt_text = ttk.Label(self.config_frame,text="　品質：",font=self.fontStyle)
        self.qt_text.grid(row=1,column=0,padx=10)

        self.qlty_combobox = ttk.Combobox(self.config_frame)
        self.qlty_combobox.grid(row=1, column=1,pady=10)
        

        #================
        self.dl_button = ttk.Button(self.main_window,text='下載',command=self.download)
        self.dl_button.grid(row=2, column=0,padx=10,pady=10, columnspan=5)

        #================
        self.log_window = scrolledtext.ScrolledText(self.main_window,width=70,bd=4,height=10,font=self.fontStyle)
        self.log_window.grid(row=3,column=0,columnspan=5)
        msg='['+time.strftime("%H:%M:%S")+']  '+'[Welcome]  '+'歡迎使用「YouTube下載工具 V1.0」\n'
        self.log_window.insert(END,msg)

        # self.dl_list = ttk.Treeview(self.main_window,columns=["1","2","3"],show="headings")
        # self.dl_list.column('1',width=400,anchor='center')
        # self.dl_list.column('2',width=100,anchor='center')
        # self.dl_list.column('3',width=200,anchor='center')
        # self.dl_list.heading("1",text="影片名稱")
        # self.dl_list.heading("2",text="品質")
        # self.dl_list.heading("3",text="下載進度")
        # self.dl_list.grid(row=3, column=0,padx=10,pady=10, columnspan=5)

    def download(self):
        self.config.read('config.ini')
        value = self.config.get("SETTINGS",'save_path')

        msg='['+time.strftime("%H:%M:%S")+']  '+'[Info]  '+'正在下載「%s」\n' % self.video_name
        self.log_window.insert(END,msg)
        self.log_window.see("end")
        time.sleep(5)
        self.yt.streams.get_by_resolution(self.qlty_combobox.get()).download(output_path=value)

        

    def call_setting_save_path_window(self):
        
        t = Toplevel(self)
        t.wm_title("Hint")
        l = ttk.Label(t, text="您尚未選擇儲存位置",font=self.normalfont)
        l.grid(row=0, column=0, padx=50, pady=10)
        b = ttk.Button(t, text="選擇路徑",command=lambda:[des(), self.set_path()])
        b.grid(row=2, column=0, padx=25, pady=10)
        
        def des():
            t.destroy()
            
    def start(self):
        
        self.video_type.config(values=['mp3','mp4'])
        self.check_save_path()
        rt_list = self.get_info(self.link_entry.get())
        self.video_title.config(text=rt_list[0],font=self.normalfont)
        self.info_frame.grid(ipadx=0)
        self.info_label.config(text=rt_list[3])
        self.info_label1.config(text=rt_list[2]+' ｜ '+rt_list[4])
        def cv_imread(filePath):
            cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
            return cv_img

        im = cv_imread(rt_list[1])
        cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
        cv2image = cv2.resize(cv2image,(120,90))
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.photo.imgtk = imgtk
        self.photo.configure(image=imgtk,width=360)

        
        self.q_list = rt_list[5]
        self.qa_list = rt_list[6]
        self.video_name = rt_list[0]

        
    
    def combo_q(self, *args, **kwargs):
        if self.video_type.get() == 'mp4':
            self.qlty_combobox.config(values=self.q_list)
            self.qlty_combobox.current(0)
        elif self.video_type.get() == 'mp3':
            self.qlty_combobox.config(values=self.qa_list)
            self.qlty_combobox.current(0)

    def check_save_path(self):
        
        self.config.read('config.ini')
        value = self.config.get("SETTINGS",'save_path')

        if value == 'No_path':
            self.call_setting_save_path_window()
        else:
            return True

    def open_folder(self):
        self.config.read('config.ini')
        self.out_path = self.config.get("SETTINGS",'save_path')
        if self.check_save_path():
            os.startfile(self.out_path)
            
            

    def set_path(self, *args, **kwargs):
        
        floder_path = filedialog.askdirectory()
        print(floder_path)
        try:
            self.config.add_section("SETTINGS")
        except configparser.DuplicateSectionError:
            pass
        self.config.set("SETTINGS", "save_path", floder_path)

        with open('config.ini', "w") as config_file:
            self.config.write(config_file)
        
    
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    def onProgress(self,stream, chunk, remains, *args, **kwargs):
        total = stream.filesize                     # 取得完整尺寸
        percent = (total-remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
        print(f'下載中… {percent:05.2f}', end='\r')
        if  percent == 100:
            msg='['+time.strftime("%H:%M:%S")+']  '+'[Info]  '+'下載完成\n'
            self.log_window.insert(END,msg)
            self.log_window.see("end")
            self.link_entry.delete(0,END)

    def get_info(self,url):
        if 'watch' in url:
            self.yt = YouTube(url, on_progress_callback=self.onProgress)
            
            title=self.yt.title
            punctuation_string = string.punctuation
            for i in punctuation_string:
                title = title.replace(i, '')
            
            f = open('./cache/%s.jpg' % title,'wb')
            f.write(urllib.request.urlopen(f'{self.yt.thumbnail_url}').read())
            f.close()
            print("download successful")
            path='./cache/%s.jpg' % title

            total_time = time.strftime("%H:%M:%S", time.gmtime( float(self.yt.length) ))
            print(total_time,self.yt.views)
            date=str(self.yt.publish_date).split()[0]

            q_list = []
            qa_list = []
            #================

            for i in range(len(str(self.yt.streams.asc().filter(type='video',subtype='mp4')).split(','))):
                list_t=str(self.yt.streams.asc().filter(type='video',subtype='mp4')).split(',')[i].strip().split(" ")[3].strip('res="')
                q_list.append(list_t)

            q_list = list(set(q_list))
            q_list.sort()
            q_list = natsort.natsorted(q_list)

            #================

            for i in range(len(str(self.yt.streams.asc().filter(type='audio')).split(','))):
                list_t=str(self.yt.streams.asc().filter(type='audio')).split(',')[i].strip().split(" ")[3].strip('abr="')
                qa_list.append(list_t)

            qa_list = list(set(qa_list))
            qa_list.sort()
            qa_list = natsort.natsorted(qa_list)
            print(qa_list)
            
            #================
            #self.yt_stream=Stream('https://www.youtube.com/watch?v=XKEE0sW_lVg')
            
            return self.yt.title, path, total_time, self.yt.author, date, q_list, qa_list

        elif 'playlist' in url:
            self.yt = Playlist(url)
            
            title=self.yt.title
            
            path='./resource/playlist.jpg'

            length=str(self.yt.length)+' Videos'
            
            date='Last Updated '+str(self.yt.last_updated)
            print(date)
            return self.yt.title, path, length, self.yt.owner, date
        else:
            print('error')

def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    window = MY_GUI(init_window)
   
    window.set_init_window()
    
    

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    



#def get_dl_info():

#get_info('https://www.youtube.com/watch?v=17C0QjEaqo0')


gui_start()