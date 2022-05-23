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
