import tkinter as tk
from tkinter import filedialog
from moviepy import editor
import datetime
import os
import numpy as np


def file_import():
    filename = filedialog.askopenfilenames()#filename is tuple
    
    for x in filename:
        file_list.insert(1,x) #file location + filename

    
    

def file_up():
    if not file_list.curselection():
        return
    
    for pos in file_list.curselection():
        try:
            if pos==0:
                continue
            text = file_list.get(pos)
            file_list.delete(pos)
            file_list.insert(pos-1, text)
            file_list.pop(pos)
            file_list.insert(pos-1, text)
            file_list.selection_set(pos-1)
        except:
            pass

def file_down():
    if not file_list.curselection():
        return
    
    for pos in file_list.curselection():
        try:
            if pos==(file_list.size()-1):
                continue
            text = file_list.get(pos)
            file_list.delete(pos)
            file_list.insert(pos+1, text)
            file_list.pop(pos)
            file_list.insert(pos+1, text)
            file_list.selection_set(pos+1)
        except:
            pass


def video_duration(file_loc):
    clip = editor.VideoFileClip(file_loc)
    duration = clip.duration
    video_time = str(datetime.timedelta(seconds = int(duration)))
    clip.close()
    return duration
    
    
    
def movie_scale(v_time):
    root = tk.Tk()
    tk.Scale(root, from_=0, to=v_time, orient="horizontal").pack()
    root.mainloop()
    
    



def init():
    global list_all
    list_all = file_list.get(0,"end")
    global count
    global scales
    global labels
    count=0
    labels = {}
    scales = {}
    root = tk.Tk()
    
    for x in list_all:
        head,tail = os.path.split(x)
        labels[count] = tk.Label(root,text=tail)
        labels[count].pack()
        scales[count]=tk.Scale(root, from_=0, to=video_duration(x),length=200,resolution=1,label="start", orient="horizontal")
        scales[count].pack()
        scales[count+1]=tk.Scale(root, from_=0, to=video_duration(x),length=200,resolution=1,label="end", orient="horizontal")
        scales[count+1].pack()
        count+=2
    
    proceed_btn = tk.Button(root,text="start",command=get_scale_values)
    proceed_btn.pack()
    root.mainloop()

def change_sec(x):
    hours = int(x/3600)
    minutes = int((x%3600)/60)
    secs = int((x%3600)%60)
    return ('%02d:%02d:%02d'%(hours,minutes,secs))


def get_scale_values():
    
    global each_clip
    each_clip=[]
    for x in list_all:
        each_clip.append(x)
    for x in range(len(each_clip)):
        each_clip[x]=each_clip[x].replace(".mp4","_cut")

            
    for i in range(0,len(scales),2):
        s_time = scales[i].get()
        e_time = scales[i+1].get()
        du = e_time-s_time
        start_time = change_sec(s_time)
        end_time = change_sec(e_time)
        
        os.system("ffmpeg -i "+list_all[int(i/2)]+" -ss "+start_time+" -t "+str(du)+" -c copy "+each_clip[int(i/2)]+".mp4")
        
    com = 'ffmpeg -i concat:"'
    for i in range(len(each_clip)):
        com+=each_clip[i]+".mp4|"
    
    com = com[:-1]
    com+='" output.mp4'
    os.system(com)
    for i in range(len(each_clip)):
        os.remove(each_clip[i]+".mp4")

    
    
    
    



window = tk.Tk()
file_open_btn = tk.Button(window,text="import file",command=file_import)
file_open_btn.pack()
file_list = tk.Listbox(window,selectmode=tk.BROWSE,width=100)
file_list.pack()
file_up_btn = tk.Button(window,text="move up",command=file_up)
file_up_btn.pack()
file_down_btn = tk.Button(window,text="move down",command=file_down)
file_down_btn.pack()
start_btn = tk.Button(window,text="start",command=init)
start_btn.pack()
window.mainloop()


