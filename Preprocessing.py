import csv
import math
import sys
import numpy as np
import pandas as pd
from PIL import Image,ImageTk
import Gui
class Preprocessing_:
    __Dataset = ""
    __algorithm=""
    __image=""
    __threshold=0
    __gx_array=[]
    __gy_array = []
    # __Gmagnitude =[]
    # __Gdirection =[]
    size=256
    pp_gx = Image.open("material/prep_material/pp_gx.jpg").resize((size, size))
    pp_gy = Image.open("material/prep_material/pp_gy.jpg").resize((size, size))
    def __init__(self):
        pass

    def __sobel(self):
        width, height = self.__image.size
        Maskx = [[-1, 0, 1],
                 [-2, 0, 2],
                 [-1, 0, 1]]

        Masky = [[1, 2, 1],
                 [0, 0, 0],
                 [-1, -2, -1]]

        return self.__sobel_final(self.__sobel_gx(Maskx),self.__sobel_gy(Masky))

    def __sobel_gx(self,Maskx):

        Array = []

        max = 0
        min = 256
        sum = 0
        for y in range(1, self.__image.height - 1):
            for x in range(1, self.__image.width - 1):
                for i in range(3):
                    for j in range(3):
                        sum = sum + self.__image.getpixel((x - 1 + i, y - 1 + j)) * Maskx[0 + i][0 + j]

                sum = int(sum / 9)
                Array.append(sum)
                if sum > max:
                    max = sum
                if min > sum:
                    min = sum

        #     self.__gx_array.append(Array)
        # self.__gx_array = np.float32(self.__gx_array)
        ekle = ((max) * self.__threshold) / 100

        for t in range(len(Array)):
            if (Array[t] > ekle):
                Array[t] = 255
            else:
                Array[t] = 0
        d = 0
        for y in range(1, self.pp_gx.height - 1):
            for x in range(1, self.pp_gx.width - 1):
                self.pp_gx.putpixel((x, y), (Array[d], Array[d], Array[d]))
                d = d + 1

        ##self.pp_gx.show()
        return self.pp_gx
 #
    def __sobel_gy(self,Masky):
        Array = []

        max = 0
        min = 256
        sum = 0
        for y in range(1, self.__image.height - 1):
            for x in range(1, self.__image.width - 1):
                pixel = self.__image.getpixel((x, y))

                for i in range(3):
                    for j in range(3):
                        sum = sum + self.__image.getpixel((x - 1 + i, y - 1 + j)) * Masky[0 + i][0 + j]

                sum = int(sum / 9)
                Array.append(sum)
                if (sum > max):
                    max = sum
                if (min > sum):
                    min = sum

        #     self.__gy_array.append(Array)
        # self.__gy_array = np.float32(self.__gx_array)

        ekle = ((max) * self.__threshold) / 100

        for t in range(len(Array)):

            if (Array[t] > ekle):
                Array[t] = 255
            else:
                Array[t] = 0

        d = 0
        for y in range(1, self.pp_gy.height - 1):
            for x in range(1, self.pp_gy.width - 1):
                self.pp_gy.putpixel((x, y), (Array[d], Array[d], Array[d]))

                d = d + 1
        return self.pp_gy

    def __sobel_final(self,gx_image,gy_image):
        array1 = []
        array2 = []
        for y in range(gx_image.height ):
            for x in range(gx_image.width ):
                pixel_gx = gx_image.getpixel((x,y))
                pixel_gy = gy_image.getpixel((x,y))
                #    print(pixel_gx[1],pixel_gy)
                # magnitude=math.sqrt(self.__gx_array[y,x]**2+self.__gy_array[y,x]**2)
                # array1.append(magnitude)
                # try:
                #     direction=math.atan(self.__gy_array[y,x]/self.__gx_array[y,x])
                # except Exception as e:
                #     print("")
                #     print(y)
                #     print(x)
                #     print(self.__gy_array[y,x])
                #     print(self.__gx_array[y,x])

                # array2.append(direction)
                if(pixel_gx[0]==255 or pixel_gy[0]==255 ):##ikissi aynıysa yani beyaz varsa o kenardır
                    #self.pp_gy değişeblr
                    self.pp_gy.putpixel((x, y),(255,255,255))
                else:
                    self.pp_gy.putpixel((x, y), (0, 0, 0))

            # self.__Gmagnitude.append(array1)
            # self.__Gdirection.append(array2)

        # for i in self.__Gmagnitude:
        #     for j in self.__Gmagnitude:
        #         print(j,end="," )
        #     print("")
        #
        # print("asaf")
        # for i in self.__Gdirection:
        #     for j in self.__Gdirection:
        #         print(j,end=",")
        #     print("")
        return self.pp_gy

    def __prewitt(self):
        Maskx = [[-1, 0, 1],
                 [-1, 0, 1],
                 [-1, 0, 1]]

        Masky = [[1, 1, 1],
                 [0, 0, 0],
                 [-1, -1, -1]]

        return self.__prewitt_final(self.__prewitt_gx(Maskx), self.__prewitt_gy(Masky))

    def __prewitt_gx(self, Maskx):
        Array = []

        max = 0
        min = 256
        sum = 0
        for y in range(1, self.__image.height - 1):
            for x in range(1, self.__image.width - 1):
                pixel = self.__image.getpixel((x, y))

                for i in range(3):
                    for j in range(3):
                        sum = sum + self.__image.getpixel((x - 1 + i, y - 1 + j)) * Maskx[0 + i][0 + j]

                sum = int(sum / 9)
                Array.append(sum)
                if (sum > max):
                    max = sum
                if (min > sum):
                    min = sum
        ekle = ((max) * self.__threshold) / 100

        for t in range(len(Array)):

            if (Array[t] > ekle):
                Array[t] = 255

            else:
                Array[t] = 0

        d = 0
        for y in range(1, self.pp_gx.height - 1):
            for x in range(1, self.pp_gx.width - 1):
                self.pp_gx.putpixel((x, y), (Array[d], Array[d], Array[d]))
                d = d + 1

        return self.pp_gx

    def __prewitt_gy(self, Masky):
        Array = []

        max = 0
        min = 256
        sum = 0
        for y in range(1, self.__image.height - 1):
            for x in range(1, self.__image.width - 1):
                pixel = self.__image.getpixel((x, y))

                for i in range(3):
                    for j in range(3):
                        sum = sum + self.__image.getpixel((x - 1 + i, y - 1 + j)) * Masky[0 + i][0 + j]

                sum = int(sum / 9)
                Array.append(sum)
                if (sum > max):
                    max = sum
                if (min > sum):
                    min = sum

        ekle = ((max) * self.__threshold) / 100

        for t in range(len(Array)):

            if (Array[t] > ekle):
                Array[t] = 255
            else:
                Array[t] = 0

        d = 0
        for y in range(1, self.pp_gy.height - 1):
            for x in range(1, self.pp_gy.width - 1):
                self.pp_gy.putpixel((x, y), (Array[d], Array[d], Array[d]))

                d = d + 1
        return self.pp_gy

    def __prewitt_final(self, gx_image, gy_image):
        for y in range(gx_image.height ):
            for x in range(gx_image.width ):

                pixel_gx = gx_image.getpixel((x,y))
                pixel_gy = gy_image.getpixel((x,y))


                if(pixel_gx[1]==255 or pixel_gy[1]==255  ):
                    self.pp_gy.putpixel((x, y),(255,255,255))
                else:
                    self.pp_gy.putpixel((x, y), (0, 0, 0))

        return self.pp_gy

    def Create_(self,algorithm,threshold,image):
        self.__image= image.resize((self.size, self.size))
        self.__image=self.__image.convert('L')
        self.__algorithm= algorithm
        self.__threshold= threshold

        if(algorithm=="sobel"):
            self.__image=self.__sobel()
        elif(algorithm=="prewitt"):
            self.__image=self.__prewitt()

        self.pp_gx = Image.open("material/prep_material/pp_gx.jpg").resize((self.size, self.size))
        self.pp_gy = Image.open("material/prep_material/pp_gy.jpg").resize((self.size, self.size))

    def getImg(self):
        return self.__image
    def Img_none(self):
        self.__image=""

    def get_image_Gmagnatude_array(self):
        return self.__Gmagnitude
    def get_image_Gdirection_array(self):
        return self.__Gdirection

# def Create(self,algorithm,threshold):
        #     self.__algorithm = algorithm
        #     self.__threshold = threshold
        #     dataset = pd.read_csv("material_/path_data.csv", header=None)
        #     paths=dataset.iloc[:,0].values
        #     i=0
        #     save_url="material_"
        #     for  path in paths:
        #         print(path)
        #         self.__image = Image.open("material_/images/"+path).resize((self.size, self.size))
        #         self.__image=self.__image.convert("L")
        #         if (algorithm == "sobel"):
        #             self.__image = self.__sobel()
        #         elif (algorithm == "prewitt"):
        #             self.__image = self.__prewitt()
        #         print(type(self.__image))
        #         self.__image.save(save_url+"/Prep_images/image"+str(i)+".jpg" , "JPEG")
        #         self.__image=""
        #         self.pp_gx = Image.open("material/prep_material/pp_gx.jpg").resize((self.size, self.size))
        #         self.pp_gy = Image.open("material/prep_material/pp_gy.jpg").resize((self.size, self.size))
        #         i+=1
        #     #self.__Dataset=self.Save_new_csv(save_url)
        #
        # def Save_new_csv(self,images_folder):
        #     with open(images_folder+"/Prep_images", 'a', encoding='UTF8', newline='') as write_file:
        #         writer = csv.writer(write_file)
        #
        #     return csv
        #
        # def get_dataset(self):
        #     return self.__Dataset
        # def set_dataset(self, csv):
        #     pass