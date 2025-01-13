# -*- coding: utf-8 -*-
import time
import tkinter as tk
from PIL import Image, ImageTk
import Settings as s
import random


class Screen(tk.Tk):
    def __init__(self):
        print("screen start")
        tk.Tk.__init__(self, className='Poppy')
        self._frame = None
        self.switch_frame(EyesPage)
        self["bg"] = "#F3FCFB"

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            if hasattr(self._frame, 'background_label'):
                self._frame.background_label.destroy()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

##### need to make sure all paths are good##############
class EyesPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//eyes.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class How_Hardware(tk.Frame):
    def __How_Hardware__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//How_Hardware.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class What_Hardware(tk.Frame):    
    def __What_Hardware__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//What_Hardware.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class Why_Hardware(tk.Frame):   
    def __Why_Hardware__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//Why_Hardware.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class What_inter(tk.Frame): 
    def __What_inter__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//What_inter.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class Why_inter(tk.Frame): 
    def __Why_inter__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//Why_inter.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class Continue(tk.Frame):     
    def __Continue__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//Continue.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class impossible_EX(tk.Frame): 
    def __impossible_EX__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//impossible_EX.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class bend_elbows(tk.Frame): 
    def __bend_elbows__(self, master): 
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//bend_elbows.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class raise_arms_forward(tk.Frame): 
    def __raise_arms_forward__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//raise_arms_forward.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class open_and_close_arms(tk.Frame): 
    def __open_and_close_arms__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//open_and_close_arms.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class raise_arms_bend_elbows(tk.Frame):     
    def __raise_arms_bend_elbows__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//raise_arms_bend_elbows.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class finished_impossible_ex_good(tk.Frame): 
    def __finished_impossible_ex_good__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//finished_impossible_ex_good.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class continue_inter(tk.Frame):     
    def __continue_inter__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//continue_inter.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class Alert(tk.Frame): 
    def __Alert__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//Alert.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()
class goodbye(tk.Frame): 
    def __goodbye__(self, master):
        tk.Frame.__init__(self, master)
        image = Image.open('pictures//goodbye.png')
        self.photo_image = ImageTk.PhotoImage(image)  # self. - for keeping the photo in memory so it will be shown
        tk.Label(self, image=self.photo_image).pack()


    

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom=self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom


if __name__ == "__main__":
    s.screen = Screen()
    app = FullScreenApp(s.screen)
    s.screen.mainloop()
