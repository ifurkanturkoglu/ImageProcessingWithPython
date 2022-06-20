import csv
import numpy as np
import pandas as pd
from PIL  import Image
from matplotlib import pyplot as plt
from skimage.exposure import exposure
from skimage.feature import hog
from skimage.io import imread,imshow
from skimage.transform import resize
import cv2
class Image_process_:
    __Dataset=""
    __algorithm=""
    __image_bool=False
    def __init__(self,dataset):
        if len(dataset)!=0:
            print(self.__Dataset)
            print("init")
            self.__Dataset=dataset
            filename = "material_/features.csv"
            f = open(filename, "w+")
            f.close()

    def Create(self,algorithm,bool):
        print("Create")
        self.__image_bool=bool
        self.__type=type
        self.__algorithm=algorithm
        self.Processing()

    def HOG(self ,image):
        image=image.resize((64, 128))
        img = image.convert("L")
        img = np.float32(img) / 255.0
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)

        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

        length = len(img)
        width = len(img[0])
        t = 0
        Cell_magnitude = []
        for y in range(0, length, 8):
            array_cell_y = []
            for x in range(0, width, 8):
                array_cell_x = []
                for i in range(8):
                    for j in range(8):
                        pixel = mag[y + i][x + j]
                        array_cell_x.append(pixel)  # array
                array_cell_y.append(array_cell_x)
            Cell_magnitude.append(array_cell_y)

        Cell_direction = []
        for y in range(0, length, 8):
            array_cell_y = []
            for x in range(0, width, 8):
                array_cell_x = []
                for i in range(8):
                    for j in range(8):
                        pixel = angle[y + i][x + j]
                        array_cell_x.append(pixel)  # array
                array_cell_y.append(array_cell_x)
            Cell_direction.append(array_cell_y)

        Cell_magnitude = np.array(Cell_magnitude)
        Cell_direction = np.array(Cell_direction) / 2

        magnitude = 0
        direction = 0
        Histogram_array = []
        for i in range(len(Cell_direction)):  # i yatay 32 cell
            histogram_y = []
            for j in range(len(Cell_direction[i])):  # j 32 cell içinde
                hist = list(range(0, 180, 20))#20 li katsayılarla oluşturulmuş dizi
                histogram = [0] * 9#9 elemanlı boş dizi
                for k in range(len(Cell_direction[i, j])):  # bir değer=k
                    magnitude = Cell_magnitude[i, j, k]
                    direction = Cell_direction[i, j, k]#aynı indeks değerleriyle magnitude ve direction değerleri
                    ust = 0#
                    alt = 0#
                    alt_index = 0
                    for h in hist:#alt ve üst indeksleri belirlemek için döngü
                        if direction >= h:#direction'ın büyük olduğu sürece alt index artar
                            alt_index = int(h / 20)
                            alt = h
                        else:#üst indeks belirlenir
                            ust = h
                            break
                    t = alt_index + 1
                    if ust == 0:#direction 160'dan fazlaysa dizinin başına dönmesi için
                        ust = 180
                        t = 0
                    k1 = abs(direction - alt)
                    k2 = abs(direction - ust)#k1 ve k2 değerleri direction ile indexteki alt ve üst değer aralığı hesaplanır
                    div = magnitude / (k1 + k2)
                    histogram[alt_index] += div * k2#boş histogramın alt indeks değerine div eklenir.
                    histogram[t] += div * k1##boş histogramın üst indeks değerine div eklenir.
                histogram_y.append(histogram)
            Histogram_array.append(histogram_y)

            # Block Normalization
        index_array = [[0, 0], [0, 1], [1, 0], [1, 1]]
        Block_Normalization = []
        for i in range(len(Histogram_array) - 1):#yukarı oluşturulan histogram dizisi dönülür
            array_ = []
            for j in range(len(Histogram_array[i]) - 1):
                array = []
                for a in index_array:
                    array += Histogram_array[i + a[0]][j + a[1]]#index_array'deki değerlerle block
                                                                # normalization yapısına göre histogramlar gruplandırılır.(16x16)
                array_.append(array)#y dizisi
            Block_Normalization.append(array_)#block normalization dizisi(x*y)

        features = []
        for i_, i in enumerate(Block_Normalization):
            for j_, j in enumerate(Block_Normalization[i_]):
                # print(len(Block_Normalization[i_][j_]))
                features += Block_Normalization[i_][j_]#block normalization dizisi gezilerek featurelar çıkarılır.
        print(len(features))

        return features

    def LBP(self,image):
        image = image.resize((64, 128)).convert("L")

        features = []
        dataPixel = []
        for i in range(1, image.height - 1):
            for j in range(1, image.width - 1):
                sum = 0

                three = [[j - 1, i - 1], [j, i - 1], [j + 1, i - 1], [j + 1, i], [j + 1, i + 1], [j, i + 1],
                         [j - 1, i + 1], [j - 1, i]]
                merkez = image.getpixel((j, i))
                for index, k in enumerate(three):

                    x, y = three[index]
                    piksel = image.getpixel((x, y))

                    if (merkez > piksel):
                        sum += 2 ** index

                image.putpixel((j, i), sum)
                dataPixel.append(image.getpixel((j, i)))
        for index, i in enumerate(dataPixel):
            dataPixel[index] = i / 255
        print(len(dataPixel))

        features.append(dataPixel)
        return features

    def Processing(self):

        dataset = pd.read_csv(self.__Dataset, header=None)
        paths = dataset.iloc[ :, 0].values
        for index,path in enumerate(paths):
            if self.__image_bool==False:
                image = Image.open("material_/insect/images/" + path)
            else:
                if index<len(paths)-1:
                    print(index)
                    image = Image.open("material_/insect/images/" + path)
                else:
                    print("index+")
                    image=Image.open(path)

            features= self.Algorithm(image)
            data = dataset.iloc[index, :].values

            with  open("material_/features.csv", 'a', encoding='UTF8',newline='') as write_file:
                writer = csv.writer(write_file)
                row=np.append(data,features)
                writer.writerow(row)
                print(row)
            write_file.close()

    def Algorithm(self,image):
        if self.__algorithm  == "HOG":
           return self.HOG(image)
        elif self.__algorithm == "LBP":
           return self.LBP(image)
