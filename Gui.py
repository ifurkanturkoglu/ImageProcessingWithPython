import os
from tkinter import *
from turtle import fd

import pandas as pd
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog as fd

from Image_process import Image_process_
from Machine_Learning import Machine_Learning_
from Preprocessing import Preprocessing_


class gui:
    __Dataset=""
    __Image=""
    __data_csv='material_/path_data.csv'
    __image1 = Image.open("material/backg.jpg").resize((200, 200))
    __image2 = Image.open("material/backg.jpg").resize((200, 200))
    __type=""
    __response=""
    __image_bool = False
    master = Tk()
    canvas = Canvas(master, height=600, width=1200)
    canvas.pack()

    fi = Frame(master, bg="lightslategray")
    fi.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    def convert_csv(self,url, type):
        print("assfcc")
        if type == 1:#file
            self.__type=type
            with open(self.__data_csv, mode='w') as yeni_dosya:
                print(url)
                files = os.scandir(url+"/")
                for fileIndex,a in enumerate(files):
                    img = os.scandir(a)
                    for imgIndex,b in enumerate(img):
                        yeni_dosya.write(a.name+"/"+b.name+","+a.name+","+str(imgIndex)+","+str(fileIndex)+"\n")

        elif type == 2:
            self.__type = type
            with open('material_/path_data.csv', mode='a') as yeni_dosya:
                print("burda")
                yeni_dosya.write(url + "," + "None" + "," + str(0) + "," + str(1) + "\n")##############İNDEXİ GUİDEN GİİİR????????
            self.__Image=Image.open(url)

        self.Load_button_0['state'] = NORMAL
        self.Load_button2['state'] = NORMAL

    def apply_1(self):

        if len(Ip_opsion.get()) != 1 and len(Ed_opsion.get()) != 1:
            if type ==2:
                ed= Preprocessing_()
                ed.Create_(Ed_opsion.get(),30,self.__Image)
                self.Pp_view(ed.getImg())
            ip = Image_process_(self.__data_csv)
            ip.Create(Ip_opsion.get(),self.__image_bool)

    def apply_2(self):
        if  len(Mlearn_opsion.get()) != 1:

            features="material_/features.csv"
            ml = Machine_Learning_(features)
            ml.Create(Mlearn_opsion.get(),self.entry2.get(),self.__image_bool)
            self.Output(ml.return_response())

    Load_button_0 = ttk.Button(fi, text='Apply', state=DISABLED)
    Load_button2 = ttk.Button(fi, text='Apply', state=DISABLED)

    entry2= Entry(fi, width=5)
    def Create(self):

        self.Load_button_0['command']=self.apply_1
        self.Load_button2['command'] = self.apply_2
        # veri button
        Load_button = ttk.Button(self.fi, text='Veri seti', command=self.select_file)  ##command=
        Load_button.pack(expand=True)
        Load_button.place(relx=0.1, rely=0.7)

        #İmage_index


        # image button
        Load = ttk.Button(self.fi, text='Image', command=self.select_image)
        Load.pack(expand=True)
        Load.place(relx=0.1, rely=0.8)

        ########################
        # Edge detection
        global Ed_opsion
        Ed_opsion = StringVar(self.fi)
        Ed_opsion.set("\t")
        Ed_menu = OptionMenu(self.fi, Ed_opsion, "sobel", "prewitt")
        Ed_menu.pack()
        Ed_menu.place(relx=0.4, rely=0.7)

        # Image processing
        global Ip_opsion
        Ip_opsion = StringVar(self.fi)
        Ip_opsion.set("\t")
        Ip_menu = OptionMenu(self.fi, Ip_opsion, "HOG", "LBP")
        Ip_menu.pack()
        Ip_menu.place(relx=0.5, rely=0.7)

        # apply1 button
        self.Load_button_0.pack(expand=True)
        self.Load_button_0.place(relx=0.5, rely=0.8)

        print(type(self.Load_button_0))
        ########################
        # algorihtm
        global Mlearn_opsion
        Mlearn_opsion = StringVar(self.fi)
        Mlearn_opsion.set("\t")
        Mlearn_menu = OptionMenu(self.fi, Mlearn_opsion, "K-nn", "SVM")
        Mlearn_menu.pack()
        Mlearn_menu.place(relx=0.8, rely=0.7)


        self.entry2.pack()
        self.entry2.place(relx=0.9, rely=0.7)

        # apply2 button
        self.Load_button2.pack(expand=True)
        self.Load_button2.place(relx=0.8, rely=0.8)
        # self.Image_view("")

        ########################
        # Images1
        ph1 = ImageTk.PhotoImage(self.__image1)
        r1 = Label(self.fi, image=ph1)
        r1.place(relx=0.05, rely=0.15)
        # self.Pp_view("")

        # Images2
        ph2 = ImageTk.PhotoImage(self.__image2)
        r2 = Label(self.fi, image=ph2)
        r2.place(relx=0.3, rely=0.15)
        # self.Ip_view("")

        self.Output("")
        self.master.mainloop()


    def Output(self,text):
        Output = Text(self.fi, height=10, width=50, bg="light cyan")
        Output.insert(1.0, text)
        Output.pack()
        Output.place(relx=0.6, rely=0.2)
        self.master.mainloop()

    def select_file(self):

        self.Load_button_0['state'] = DISABLED
        self.Load_button2['state'] = DISABLED

        Selected_file = fd.askdirectory(
            title='Open a file',
            initialdir='/',
            )
        try:
            self.__Dataset = Selected_file ##url

            if len(Selected_file)!=0:
                    self.__image_bool=False
                    self.convert_csv(Selected_file,type=1)
                    self.master.mainloop()

        except Exception as e:
            print(e)


    def select_image (self):
        self.Load_button_0['state'] = DISABLED
        self.Load_button2['state'] = DISABLED

        filetypes = (
            ('image files', '.jpg'),
            ('All files', '.*')
        )
        Selected_image = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        try:
            print(Selected_image)
            print(type(Selected_image))
            print(len(Selected_image))
            if len(Selected_image) != 0:
                self.__image_bool=True
                self.__Dataset = Selected_image
                #self.Image_view(Selected_image)
                self.convert_csv(Selected_image, type=2)

        except Exception as e:
            print(e)

    def Image_view(self, image):
        # sadece open
        image=Image.open(image)
        self.__image1 = image
        ph1 = ImageTk.PhotoImage(image.resize((200, 200)))
        r1 = Label(self.fi, image=ph1)
        r1.place(relx=0.05, rely=0.15)
        self.master.mainloop()

    def Pp_view(self, image):
        self.__image2 = image
        ph2 = ImageTk.PhotoImage(image.resize((200, 200)))
        r2 = Label(self.fi, image=ph2)
        r2.place(relx=0.3, rely=0.15)
        self.master.mainloop()
