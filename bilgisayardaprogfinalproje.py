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
                print("Site Bariyerlerine Gelen Araç :->",dosya) # plakası okunan araç plakasının ekrana yazdırılması

                img = cv2.imread(dosya, cv2.IMREAD_COLOR) # okunan plaka resminin program tarafından işlenmesi
                img = cv2.resize(img, (600, 400))

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray, 13, 15, 15)

                edged = cv2.Canny(gray, 30, 200)
                contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(contours)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
                screenCnt = None

                for c in contours:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                    if len(approx) == 4:
                        screenCnt = approx
                        break
                if screenCnt is None:
                    detected = 0
                    print("No contour detected")
                else:
                    detected = 1
                if detected == 1:
                    cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
                mask = np.zeros(gray.shape, np.uint8)
                new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
                new_image = cv2.bitwise_and(img, img, mask=mask)
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
                plaka_no = pytesseract.image_to_string(Cropped, config='--psm 11')
                print("Plaka Numarası ->", plaka_no) # okunan plakanın plaka_no değerine aktarılması
                img = cv2.resize(img, (500, 300))
                Cropped = cv2.resize(Cropped, (400, 200))
                cv2.imshow('Araba', img) # tekrar boyutlandırılan araba resminin gösterilmesi
                cv2.imshow('Kirpildi', Cropped) # kesilen araba resminin gösterilmesi
                text = plaka_no.strip('\n,!')
                sql_select_query = """select * from Site where Plaka = ? """ #gelen aracın veritabanında siteye ait olup olmadığının tespiti
                self.islem.execute(sql_select_query, (text,))
                data = self.islem.fetchall()
                if data: # eğer araç siteye ait ise otomatik kapının açılmasını ve giriş-çıkış saatinin sisteme işlenmesi
                    print("K A P I   A Ç I L I Y O R")
                    sql_select_query = """select * from Arac_Kayit where Plaka_No = ? """
                    self.islem.execute(sql_select_query, (text,))
                    data = self.islem.fetchall()
                    an = datetime.datetime.now()
                    tarih = datetime.datetime.ctime(an)
                    zaman = datetime.datetime.strftime(an, '%d %B %Y') + ' ' + datetime.datetime.strftime(an, '%X')
                    for row in data: deger = row[1]
                    if len(data) > 0:
                        if deger == 'Ç': #veritabanındaki son değer eğer çıkışı gösteriyorsa kaydederken bu sefer giriş olarak kaydetmesi
                            girdi = ''
                            deger = 'G'
                            data = (text, deger, zaman, girdi)
                            self.islem.execute("""INSERT INTO Arac_Kayit VALUES (?,?,?,?)""", data)
                            self.veritabanı.commit()
                            print("\n Kayıt başarıyla girilmiştir.")
                        else: #veritabanındaki son değer eğer girişi gösteriyorsa kaydederken bu sefer çıkış olarak kaydetmesi
                            girdi = ''
                            deger = 'Ç'
                            data = (text, deger, girdi, zaman)
                            self.islem.execute("""INSERT INTO Arac_Kayit VALUES (?,?,?,?)""", data)
                            print("\n Kayıt başarıyla girilmiştir.")
                            self.veritabanı.commit()
                    else: # eğer aracın kaydı veritabanına ilk sefer yapılıyorsa
                        girdi = ''
                        deger = 'G'
                        data = (text, deger, zaman, girdi)
                        self.islem.execute("""INSERT INTO Arac_Kayit VALUES (?,?,?,?)""", (data))
                        self.veritabanı.commit()
                        print("\n Kayıt başarıyla girilmiştir.")
                else:
                    print ("Araç Siteye Ait Değil.Kapılar Kapalı") #veritabanında olmayan bir araç geldiğinde kapıların kapalı olduğunu belirten ibare

        cv2.waitKey(0) #gösterilen resimlerin ekrandan kaybolması için bir tuşa basılması gerekmektedir
        cv2.destroyAllWindows() #açılan tüm pencereleri kaptmak için kullanılmıştır.





    def menu(self): #program ilk çalıştırıldığında ekrana gelecek olan menünün işlendiği kod kısmıdır
        print("\n ******** OZANKENT SİTESİ ARAÇ PLAKA TANIMA SİSTEMİ *******\n")
        print(" 1) Kayıt İşlemleri \n 2) Plaka Tanıma Demo \n 3) Araç Sorgulama\n 4) Çıkış \n ")

        self.anahtar = "off" #  doğru seçim yapılana kadar menüyü veya uyarıları ekrana getirecektir.
        while self.anahtar == "off":
            secim = input("\nHangi işlemi yapmak istediğinizi yazınız: ")
            choice = secim.lower()
            if choice == "1": #  eğer seçim 1 ise  alt kayıt menünün açılması
                self.kayıt_menu()
                self.anahtar = "on"
            elif choice == "2": #  eğer seçim 2 ise  plaka tanımanın yaptırılması
                self.plaka_tanıma()
                self.anahtar = "on"
            elif choice == "3": #  eğer seçim 3 ise sorgulamanın yapılması
                self.sorgulama()
                self.anahtar = "on"
            elif choice == "4": #  eğer seçim 4 ise programdan çıkılması
                self.Cikis_yap()
                self.anahtar = "on"
            else:
                print("Girilen değer anlaşılmadı. Lütfen tekrar deneyin.")

    def ana_menu(self):
        print("\n ******** OZANKENT SİTESİ ARAÇ PLAKA TANIMA SİSTEMİ *******\n")
        print(" 1) Kayıt İşlemleri \n 2) Plaka Tanıma Demo \n 3) Araç Sorgulama\n 4) Çıkış \n ")

        self.anahtar = "off"
        while self.anahtar == "off":
            secim = input("\nHangi işlemi yapmak istediğinizi yazınız: ")
            choice = secim.lower()
            if choice == "1": #  eğer seçim 1 ise  alt kayıt menünün açılması
                self.kayıt_menu()
                self.anahtar = "on"
            elif choice == "2": #  eğer seçim 2 ise  plaka tanımanın yaptırılması
                self.plaka_tanıma()
                self.anahtar = "on"
            elif choice == "3": #  eğer seçim 3 ise sorgulamanın yapılması
                self.sorgulama()
                self.anahtar = "on"
            elif choice == "4": #  eğer seçim 4 ise programdan çıkılması
                self.Cikis_yap()
                self.anahtar = "on"
            else:
                print("Lütfen olan seçenek numaralarından girerek tekrar deneyiniz!")

    def Cikis_yap(self): # programdan çıkışın yapılmasını  ve veritabanının kapatılmasını sağlayan kod
        print("\n Çıkış başarıyla yapıldı.")
        self.veritabanı.close()
        self.durum = False

    def kayıt_menu(self): #veritabanına kayıt eklenmesi, güncelleştirilmesi veya silinmesi için kullanıcıya menü göstermek
        print("\n-----  KAYIT İŞLEMLERİ MENÜSÜ  -----\n")
        print(" 1) Kayıt Girişi \n 2) Kayıt Güncelle \n 3) Kayıt Sil \n 4) Kayıtları Görüntüle \n 5) Ana Menü \n 6) Çıkış")

        anahtar1 = 0
        while anahtar1 == 0:
            secim = input("\nHangi işlemi yapmak istediğinizi yazınız: ")
            choice = secim.lower()
            if choice == "1": # kayıt eklemek için kullanılacak kod bölümü
                self.kayıt_ekle()
                anahtar1 = 1
            elif choice == "2": # kayıt güncellemek için kullanılacak kod bölümü
                self.kayıt_guncelle()
                anahtar1 = 1
            elif choice == "3": # kayıt silmek için kullanılacak kod bölümü
                self.kayit_sil()
                anahtar1 = 1
            elif choice == "4": # kayıt görüntülemek için kullanılacak kod bölümü
                self.kayıt_goruntule()
                anahtar1 = 1
            elif choice == "5": # üst ana menüye gitmek için kullanılacak kod bölümü
                self.ana_menu()
                anahtar1 = 1
            elif choice == "6": # çıkış yapmak için kullanılacak kod bölümü
                self.Cikis_yap()
                anahtar1 = 1
            else: # listede olmayan bir değer girildiğinde verilecek uyarı
                print("Girilen değer anlaşılmadı. Lütfen tekrar deneyin.")

    def sorgulama(self): # araç veritabanında bulunan araç giriş-çıkışlarını basit bir şekilde ekrana getiren kod bölümü
        print("\n Araç Kayıt veritabanındaki tüm kayıtlar:  --------------------------------------")
        self.islem.execute("SELECT * FROM Arac_Kayit")
        data = self.islem.fetchall()
        karar = bool(data)
        print("Plaka No Giriş-Çıkış Giriş Saati Çıkış Saati")
        print("-------- ----------- ----------- -----------\n")

        for value in data:
            print(value[0], "\t\t", value[1], "\t\t", value[2], "\t\t", value[3])

    def kayıt_goruntule(self):  # daire ve araç sahipleri veritabanında bulunan bilgileri basit bir şekilde ekrana getiren kod bölümü
        print("\n Veritabanındaki tüm kayıtlar:  --------------------------------------")
        self.islem.execute("SELECT * FROM Site")
        data = self.islem.fetchall()
        karar = bool(data)
        print ("Blok Daire Adı Soyadı Plaka No")
        print ("---------- ---------- --------\n")

        for value in data:
            print(value[0],"\t\t",value[1],"\t\t",value[2])
        self.kayıt_menu()

    def kayıt_ekle(self): # daire ve araç sahipleri veritabanına yeni bir kaydın yapılmasını sağlayan kod bölümü
        print("\n Yeni Kayıt:  -----------------------------------------------")
        key = "off"
        while key == "off":
            daire = input(" Blok-Daire: ")
            adsoyad = input(" Adı Soyadı: ")
            plaka = input(" Araç Plaka No: ")
            listem = [daire, adsoyad, plaka]
            self.islem.execute("INSERT INTO Site VALUES (?,?,?)", (listem))
            self.veritabanı.commit()
            print("\n Kayıt başarıyla girilmiştir.")
            self.kayıt_goruntule()
            self.kayıt_menu()

    def kayıt_guncelle(self): # daire ve araç sahipleri veritabanında varolan bir kaydın değiştirilmesini sağlayan kod bölümü
        print("\n Kayıt Güncelleme:  --------------------------------")
        self.islem.execute("SELECT * FROM Site")
        data = self.islem.fetchall()
        karar = bool(data)
        if karar == True:
            print("-> Lütfen Güncelleme yapılacak kayıdın sırasını seçin:\n")
            sayı = 0
            for sıra, veri in enumerate(data):
                print(sıra + 1, ") ", veri, sep="")
                sayı = sayı + 1

            while True:
                try:
                    secim = int(input("\n -- Seçiminiz: "))
                    if secim > 0 and secim < sayı + 1:
                        self.islem.execute("SELECT * FROM Site WHERE rowid = {}".format(secim))
                        alınan = self.islem.fetchall()
                        print("Seçilen Kayıt -> ", alınan, end="\n\n")
                        print("Hangi Değeri Değiştireceksiniz\n 1.Blok Daire\n 2.Adi_soyadi\n 3.Plaka\n 4.Çıkış) ")
                        choice = input(" -> Güncelleme Yapılacak Değerin Numarasını Yazınız: ")
                        if choice == "1":
                            yeni_veri = input("\n-- Yeni veriyi girin: ")
                            self.islem.execute(
                                "UPDATE Site SET Blok_Daire = '{}' WHERE rowid = {}".format(yeni_veri, secim))
                            self.veritabanı.commit()
                            print("-- Güncelleme tamamlandı!")
                            break
                        elif choice == "2":
                            yeni_veri = input("\n-- Yeni veriyi girin: ")
                            self.islem.execute("UPDATE Site SET Adi_Soyadi = '{}' WHERE rowid = {}".format(yeni_veri, secim))
                            self.veritabanı.commit()
                            print("-- Güncelleme tamamlandı!")
                            break
                        elif choice == "3":
                            yeni_veri = input("\n-- Yeni veriyi girin: ")
                            self.islem.execute("UPDATE Site SET Plaka = '{}' WHERE rowid = {}".format(yeni_veri, secim))
                            self.veritabanı.commit()
                            print("-- Güncelleme tamamlandı!")
                            break
                        elif choice == "4":
                            kayıt_menu()
                            break
                        else:
                            print(" (!) Girilen Kriter anlaşılmadı. Doğru yazdığınızdan emin olun.\n")
                            break
                    else:
                        print(" (!) Girilen sıra değerinde kayıt bulunmamaktadır. Sıra numarasını doğru girin!")

                except:
                    print(" (!) Girilen değer anlaşılmadı! Lütfen rakam giriniz.\n")

        else:
            print("\n Veritabanında güncellenebilecek öğrenci kaydı bulunmamaktadır!\n")

        self.kayıt_goruntule()
        self.kayıt_menu()

    def kayit_sil(self): # daire ve araç sahipleri veritabanında verolan bir kaydın sislmnmesini sağlayan kod bölümü
        print("\n KAYIT SİLME:  --------------------------------")
        self.islem.execute("SELECT * FROM Site")
        data = self.islem.fetchall()
        karar = bool(data)
        if karar == True:
            print("-> Lütfen Silinmesini İstediğiniz Kayıdın Sıra Numarasını Giriniz:\n")
            sayı = 0
            for sıra, veri in enumerate(data):
                print(sıra + 1, ") ", veri, sep="")
                sayı = sayı + 1
        while True:
            try:
                secim = int(input("\n -- Seçiminiz: "))
                if secim > 0 and secim < sayı + 1:
                    self.islem.execute("DELETE FROM Site WHERE rowid = {}".format(secim))
                    self.veritabanı.commit()
                    print("\n Seçilen kayıt başarıyla silinmiştir.\n")
                    break
                else:
                    print("\n Seçilen değerde kayıt bulunmamaktadır. Tekrar deneyin.")
            except:
                print("Sadece sayı giriniz!")

        self.kayıt_goruntule()
        self.kayıt_menu()

Site = Ozankent("Ozankent Sitesi")

while Site.durum == True:
    Site.ana_menu()
