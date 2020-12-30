from tkinter import *
import pickle
import os
from tkinter.filedialog import askdirectory
from tkinter import PhotoImage
from pygame import mixer

class player(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.pack()
        mixer.init()
        if os.path.exists('songs.pickle'):
            with open('songs.pickle','rb') as f:
                self.playlist = pickle.load(f)

        else:
            self.playlist=[]

        self.current=0
        self.paused=True
        self.played=False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

    def create_frames(self):
        self.track= LabelFrame(self, text='song track',font='lucida 24 bold',bg='grey',fg='white',bd=5,relief=GROOVE)
        self.track.config(width=410,height=300)
        self.track.grid(row=0,column=0,padx=10)

        self.tracklist = LabelFrame(self, text=f'playlist - {str(len(self.playlist))}', font='lucida 24 bold', bg='grey', fg='white', bd=5,
                                relief=GROOVE)
        self.tracklist.config(width=190, height=400)
        self.tracklist.grid(row=0, column=1, pady=5,rowspan=3)

        self.control = LabelFrame(self, text='song track', font=('lucida 24 bold'), bg='grey', fg='white', bd=5,
                                relief=GROOVE)
        self.control.config(width=410, height=80)
        self.control.grid(row=2, column=0, padx=10,pady=5)

    def track_widgets(self):
        self.canvas = Label(self.track,image=img)
        self.canvas.config(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.songtrack = Label(self.track, text='Music Player', font='lucida 24 bold', bg='white', fg='black', bd=5,
                                relief=GROOVE)
        self.songtrack.config(width=30, height=1)
        self.songtrack.grid(row=3, column=0, padx=15)

    def control_widgets(self):
        self.loadSongs=Button(self.control,text='load songs',font='lucida 15 bold',fg='white',bg='green',bd=5,relief=GROOVE,command=self.load_songs)
        self.loadSongs.grid(row=0,column=0,padx=10)

        self.prev = Button(self.control, image=prev, command=self.prev_songs)
        self.prev.grid(row=0, column=1)

        self.pause = Button(self.control, image=pause, command=self.pause_songs)
        self.pause.grid(row=0, column=2)

        self.next = Button(self.control, image=next, command=self.next_songs)
        self.next.grid(row=0, column=3)

        self.volume = DoubleVar(self)
        self.slider = Scale(self.control, from_=0, to=20, orient=HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)


    def tracklist_widgets(self):
        self.scrollbar=Scrollbar(self.tracklist,orient=VERTICAL)
        self.scrollbar.grid(row=0,column=2,rowspan=5,sticky='ns')

        self.list=Listbox(self.tracklist,bg='skyblue',selectmode=SINGLE,yscrollcommand=self.scrollbar.set)
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>',self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0,column=0,rowspan=5)



    def load_songs(self):
        self.songlist=[]
        directory=askdirectory()
        for root_,dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\','/')
                    self.songlist.append(path)

        with open('songs.pickle','wb')as f:
            pickle.dump(self.songlist,f)

        self.playlist=self.songlist
        self.tracklist['text'] = f'playlist - {str(len(self.playlist))}'
        self.list.delete(0,END)
        self.enumerate_songs()




    def play_song(self,event=None):
        if event is not None:
            self.current=self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i,bg='white')

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image']=play
        self.paused=False
        self.played=True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current,bg='sky blue')

        mixer.music.play()

    def prev_songs(self):
        if self.current > 0:
            self.current = self.current - 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.play_song()

    def next_songs(self):
        if self.current < len(self.playlist)-1:
            self.current = self.current + 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.play_song()




    def pause_songs(self):
        if not self.paused:
            self.paused=True
            mixer.music.pause()
            self.pause['image']=pause

        else:
            if self.played==False:
                 self.play_song()
            self.paused=False
            mixer.music.unpause()
            self.pause['image']=play


    def enumerate_songs(self):
        for index,song in enumerate(self.playlist):
            self.list.insert(index,os.path.basename(song))


    def change_volume(self,event=None):
        self.v=self.volume.get()
        mixer.music.set_volume(self.v/10)


#this is my main function
root =Tk()
root.title('music player')
root.geometry('850x500')
img = PhotoImage(file='images/music.gif')
next = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')

app = player(master=root)
app.mainloop()
