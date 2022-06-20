import numpy
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris



class Machine_Learning_:
    __algorithm = ""
    __features_path = ""
    __test_size=0.2 
    __response=""
    __image_bool=False

    def __init__(self, features_path):
        self.__features_path = features_path

    def Create(self, algorithm, test_size,bool):
        if test_size!='':
            self.__test_size = test_size
        self.__image_bool=bool
        self.__algorithm = algorithm
        if self.__algorithm == "SVM":
            self.SVM()
        elif self.__algorithm == "K-nn":
            self.K_nn()

    def SVM(self):
        dataset_first = pd.read_csv(self.__features_path, header=None)
        dataset = dataset_first.sample(frac=1)
        X = dataset.iloc[:,4:].values
        y = dataset.iloc[:, 3].values
        if self.__image_bool:
            self.__test_size=(100/len(X))/100
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(self.__test_size), random_state=0)
            X_test=dataset_first.iloc[-1,4:].values
            y_test=dataset_first.iloc[-1,3]
            X_test=numpy.array([X_test])
            y_test=numpy.array([y_test])
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(self.__test_size), random_state=0)

        sc_X = StandardScaler()
        X_train = sc_X.fit_transform(X_train)
        X_test = sc_X.transform(X_test)
        classifier = SVC(kernel='linear', random_state=0)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        if self.__image_bool:
            print("TAHMİNİ DEĞER \n"+str(y_pred))
            self.__response = "TAHMİNİ DEĞER \n" + str(y_pred)
        else:
            Output="Confision Matris \n"
            cm = confusion_matrix(y_test, y_pred)
            self.__response = Output+str(cm)
            print(self.__response)

    def K_nn(self):
        # Loading data
        dataset_first = pd.read_csv(self.__features_path, header=None)
        dataset = pd.read_csv(self.__features_path, header=None)        # Create feature and target arrays
        dataset = dataset.sample(frac=1)
        X =  dataset.iloc[:,4:].values
        y = dataset.iloc[:, 3].values
        # Split into training and test set
        if self.__image_bool:
            self.__test_size = (100 / len(X)) / 100
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(self.__test_size), random_state=0)
            X_test = dataset_first.iloc[-1, 4:].values
            y_test = dataset_first.iloc[-1, 3]
            X_test = numpy.array([X_test])
            y_test = numpy.array([y_test])
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(self.__test_size), random_state=0)

        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        if self.__image_bool:
            print("TAHMİNİ DEĞER \n" + str(y_pred))
            self.__response = "TAHMİNİ DEĞER \n" + str(y_pred)
        else:
            Output = "Confision Matris \n"
            cm = confusion_matrix(y_test, y_pred)
            self.__response = Output + str(cm)
            print(cm)

    def return_response(self):
        return self.__response


# print("SVM")
# ml = Machine_Learning_("material_/features.csv")
# ml.Create("K-nn",'',False)
# print("knn")
# ml = Machine_Learning_("material_/features.csv")
# ml.Create("K-nn")
# dataset = pd.read_csv("material_/features.csv", header=None)
# print(dataset.iloc[0:1797,0].values)