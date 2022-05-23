import sqlite3 #site veritabanı ile iletişim kurmak için kullanılmıştır.
import cv2 # jpg dosyalarından plakaların okunarak sisteme aktarılması  için kullanılmıştır.
import imutils
import numpy as np
import pytesseract
import datetime # tarihlerin türkçe adlarıyla ifade edilmesi için
import os #klasör değerlerinin alınması için kullanıldı


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Tesseract uzantıyı da tanımlamamız gerekiyor

class Ozankent():
    def __init__(self, isim):
        self.veritabanı = sqlite3.connect("arac_plaka.db") #site veritabaı ile program arasında köprü
        self.islem = self.veritabanı.cursor() # işlemlerin yapılabilmesi için cursor oluşturulması
        self.isim = isim
        self.durum = True # programın devamı için kontrol değeri atanması

    def plaka_tanıma(self): #Programın ana parçası. Araç plakalarının resim klasörü içindeki dosyaların okunarak sisteme aktarılmasıdır.

        klasor = "resim" #resim dosyalarının bulunduğu klasörü tanımlama

        dosyalar=os.listdir(klasor) #klasör içindeki resimleri dosyalar değişkenine atama
        for dosya in dosyalar: #dosyalar değişkeninin içindeki dosyaların sıra ile okunması
                print("Site Bariyerlerine Gelen Araç :->",dosya) 

                img = cv2.imread(dosya, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (600, 400))

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray, 13, 15, 15)

                edged = cv2.Canny(gray, 30, 200)
                contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(contours)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
                screenCnt = None
