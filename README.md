DERSİN ADI 	: BİLGİSAYARDA PROGRAMLAMA

PROJE ADI	: PLAKA TANIMA SİSTEMİ

PROJE ÜYELERİ	: Mete YALÇINKAYA (222180530)
                  Kemal TORUN (221880529)
                  Mehmet Hakan DİLEK (222180501)
			
PROJE AMACI	: GİRİŞ KAPISI OLAN SİTE VEYA BENZERİ KURUMLARDA KULLANILMAKTA OLAN KAMERA SİSTEMLERİNE ENTEGRE EDİLEREK ÇALIŞTIRILABİLECEĞİNİ DÜŞÜNEREK
		  GİREN VE ÇIKAN ARAÇLARIN PLAKALARININ OTOMATİK OLARAK SİSTEM TARAFINDAN OKUNARAK VERİTABANINDA ARATILARAK VAR İSE OTOMATİK KAPININ AÇILMASI İÇİN 
		  EMİR VEREN AKSİ DURUMDA DA KAPININ AÇILMAMASINI SAĞLAYAN BİR PROJEDİR.PLAKA OKUMA KODLARI OPENCV MODÜLÜ KULLANILARAK YAPILMIŞTIR.
		  AYNI ZAMANDA VERİTABANINA DAİRE VE ARAÇ BİLGİLERİNİN KAYDEDİLMESİ,DEĞİŞTİRİLEBİLMESİ VEYA SİLİNEBİLMESİ MAKSADIYLA sqlite KÜTÜPHANESİ DE KULLANILMIŞTIR. 

PROJE HEDEFLERİ	: KULLANICIYA MENÜLER YARDIMIYLA HAREKET SERBESTLİĞİ SAĞLAYARAK KOLAY BİR ŞEKİLDE PROGRAMIN KULLANILABİLMESİNİ SAĞLAMAKTIR.

NOT: OZANKENT SİTESİ METE YALÇINKAYA'NIN OTURDUĞU SİTEDİR VE SİTENİN İÇİNDEKİ ARABA PLAKALARININ RESİMLERİ SAHİPLERİNİN DE RIZASIYLA ÇEKİLMİŞTİR.

PROGRAM ADIMLARI:

1. KULLANICIYA ÖNCELİKLE BİR ANA MENÜ SUNULMAKTADIR.

	******** OZANKENT SİTESİ ARAÇ PLAKA TANIMA SİSTEMİ *******

	 1) Kayıt İşlemleri 
	 2) Plaka Tanıma Demo 
	 3) Araç Sorgulama
 	 4) Çıkış 
 

	Hangi işlemi yapmak istediğinizi yazınız: 

BURADAN KULLANICININ HANGİ İŞLEMİ YAPMAK İSTEDİĞİ SORULMAKTADIR.1,2,3, VEYA 4 SEÇENEKLERİNDEN BAŞKA BİR TUŞA BASILMASI DURUMUNDA PROGRAM 

	"Lütfen olan seçenek numaralarından girerek tekrar deneyiniz!"

	Hangi işlemi yapmak istediğinizi yazınız:
UYARISINI VERMEKTE OLUP TEKRAR GİRİŞ YAPMASI İSTENMEKTEDİR.

2. KULLANICI EĞER DAİRE VEYA ARAÇ BİLGİLERİ İLE BİLGİ GİRİŞİ,DEĞİŞTİRME VE SİLME İŞLEMLERİ YAPMAK İSTİYORSA 1'E BASMAKTADIR.1'E BASILMASI DURUMUNDA DA EKRANA

	 -----  KAYIT İŞLEMLERİ MENÜSÜ  -----

	1) Kayıt Girişi 
 	2) Kayıt Güncelle 
 	3) Kayıt Sil 
 	4) Kayıtları Görüntüle 
 	5) Ana Menü 
 	6) Çıkış

	Hangi işlemi yapmak istediğinizi yazınız:

KAYIT İŞLEMLERİ MENÜSÜ AÇILMAKTADIR. KULLANICI BURADAN HANGİ İŞLEMİ YAPMAK İSTİYORSA İLGİLİ 1,2,3 VEYA 4 RAKAMINA BASARAK İŞLEMLERİNE DEVAM ETMEKTEDİR.YANLIŞ BİR TUŞA BASILMASI DURUMUNDA
ÜST MENÜDE BAHSEDİLEN UYARI MESAJI DA BU BÖLÜM İÇİN DE GELMEKTEDİR.EĞER KULLANICI ÜST MENÜYE ULAŞMAK İSTİYORSA 5 RAKAMINA BASARAK 1nci MADDEDE ANLATILAN ANA MENÜYE GEÇİŞ YAPABİLMEKTEDİR.
6 RAKAMINA BASILMASI DURUMUNDA DA PROGRAMDAN ÇIKIŞ SAĞLANMAKTADIR.

3. KULLANICI ANA MENÜDE BULUNAN "PLAKA TANIMA DEMO" BÖLÜMÜNE AİT 2 RAKAMINI TUŞLAR İSE PROGRAM SANKİ KAMERA SİSTEMİNE BAĞLI ÇALIŞAN BİR ALT SİSTEM OLARAK GELEN ARACIN PLAKA KISMININ RESMİNİ 
ÇEKEREK PROGRAMA AKTARILMASINI VE PLAKASININ OKUTULMASININ SAĞLAMAKTA, SİTEYE AİT BİR ARAÇ İSE KAPILARIN AÇILMASINI VE ARAÇ TABLOSUNA GİRİŞ ÇIKIŞLARININ YAPILMASINI SAĞLAMAKTADIR.EĞER GELEN 
ARACIN PLAKASI DAİRE-ARAÇ TABLOSUNDA BULUNAMAZ İSE KAPILARI AÇMAMAKTA VE ARACI İÇERİ ALMAMAKTADIR.

4. KULLANICI ANA MENÜDE 3'E BASARAK ARAÇ SORGULAMA BÖLÜMÜNE GİDEREK VERİTABANINDAKİ BİLGİLERİN EKRANA GETİRİLMESİNİ SAĞLAYABİLMEKTEDİR. 

5. GELİŞTİRDİĞİMİZ BU PROGRAMI YAPARKEN DAHA ÖNCEDEN BU KONULARLA İLGİLİ OLAN VE YAYIMLANAN KODLARDAN DA FAYDANILARAK KOD YAPILARI DEĞİŞTİRİLEREK KENDİ PROGRAMIMIZA ADAPTE EDİLMİŞTİR.GELİŞTİRMEYE ÇALIŞTIĞIMIZ
BU PROGRAM BU GİBİ İHTİYACI OLAN YERLER İÇİN BİR TEMEL TEŞKİL EDEBİLİR DİYE DÜŞÜNDÜK VE PROGRAM SİTE VEYA KURUMLARIN İHTİYAÇLARI DOĞRULTUSUNDA DAHA DA GELİŞTİRİLEBİLİR.SORGULAMA BÖLÜMÜ ÇOK KAPSAMLI TUTULMAMIŞ OLUP 
ÖZELLİKLE BU BÖLÜM DAHA DA DETAYLANDIRILABİLİR.

6. BİZİM BU PROGRAMDA GERÇEKLEŞTİRMEYE ÇALIŞTIĞIMIZ UNSUR HEM OPENCV NİN KULLANILABİLİRLİĞİNİ VE OPENCV MODÜLÜNDEN ALINAN HERHANGİ BİR DEĞERİN BAŞKA BİR VERİTABANINA GİRDİ OLARAK VERİLEREK 
VERİTABANI MODÜLÜ İLE ENTEGRE OLARAK ÇALIŞABİLMESİNİ GÖRMEK İDİ. BU HUSUSU DA BAŞARDIĞIMIZI DÜŞÜNÜYORUM.

UMARIM YAPTIĞIMIZ BU PROJEYİ BİZİM KADAR SİZ DE BEĞENİRSİNİZ.


