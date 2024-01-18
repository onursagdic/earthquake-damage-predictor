import random
from math import radians, sin, cos, sqrt, atan2
import folium
import os
import pandas as pd


class Bina():
    def __init__(self, ilce, yas, yapi, zemin, enlem, boylam, deprem):
        self.ilce = ilce
        self.yas = yas
        self.yapi = yapi
        self.zemin = zemin
        self.enlem = enlem
        self.boylam = boylam
        self.depremUzakligi = self.depremUzaklikHesapla(deprem)
        self.yikilmaIhtimali = self.binaYikilidiMiHesapla(deprem)
        self.yikildiMi = self.binaYikildiMiHesapla()

    
    def binaYikilidiMiHesapla(self, deprem):
        yikilmaIhtimali = deprem.yikimOrani 

        if self.zemin == "Çok Riskli":
            yikilmaIhtimali += 4 
        elif self.zemin == "Orta Riskli":
            yikilmaIhtimali += 3
        elif self.zemin == "Az Riskli":
            yikilmaIhtimali += 2
        elif self.zemin == "Risksiz":
            yikilmaIhtimali += 0.3

        if self.yapi == "Yetersiz":
            yikilmaIhtimali += 1
        elif self.yapi == "Yeterli":
            yikilmaIhtimali -= 1

        if self.yas == "2000_Oncesi":
            yikilmaIhtimali += 1
        elif self.yas == "2000_Sonrasi":
            yikilmaIhtimali -= 1

        if 0 <= self.depremUzakligi <= 5:
            yikilmaIhtimali -= 0
        elif 5 <= self.depremUzakligi < 10:
            yikilmaIhtimali -= 0.2
        elif 10 <= self.depremUzakligi < 20:
            yikilmaIhtimali -= 0.6
        elif 20 <= self.depremUzakligi < 30:
            yikilmaIhtimali -= 0.9
        elif 30 <= self.depremUzakligi < 40:
            yikilmaIhtimali -= 1.2
        elif 40 <= self.depremUzakligi < 50:
            yikilmaIhtimali -= 1.5
        elif 50 <= self.depremUzakligi < 60:
            yikilmaIhtimali -= 1.6
        elif 60 <= self.depremUzakligi < 70:
            yikilmaIhtimali -= 1.7
        elif 70 <= self.depremUzakligi < 80:
            yikilmaIhtimali -= 1.8
        elif 80 <= self.depremUzakligi < 90:
            yikilmaIhtimali -= 1.9
        elif 90 <= self.depremUzakligi < 100:
            yikilmaIhtimali -= 2
        elif 100 <= self.depremUzakligi < 120:
            yikilmaIhtimali -= 2.1
        elif 120 <= self.depremUzakligi < 150:
            yikilmaIhtimali -= 2.3
        elif 150 <= self.depremUzakligi < 250:
            yikilmaIhtimali -= 2.4
        elif 250 <= self.depremUzakligi:
            yikilmaIhtimali -= 2.5

        return yikilmaIhtimali
    
    def depremUzaklikHesapla(self, deprem):
        R = 6371.0

        # Decimal dereceyi radyana çevir
        lat1, lon1, lat2, lon2 = map(radians, [self.enlem, self.boylam, deprem.enlem, deprem.boylam])

        # Haversine formülü
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance

    def binaYikildiMiHesapla(self):
        # 0 ile 1 arasında rastgele bir sayı üret
        rastgeleSayi = random.uniform(0, 100)
        # Eğer rastgele sayı binanın yıkılma ihtimalindne küçükse, bina yıkıldı olarak kabul et
        if rastgeleSayi < self.yikilmaIhtimali:
            return True
        else:
            return False

class Deprem():
    def __init__(self, siddet, derinlik, sure):
        self.siddet = siddet
        self.derinlik = derinlik
        self.sure = sure
        self.enlem = self.randomEnlem() 
        self.boylam = self.randomBoylam()
        self.yikimOrani = self.depremYikimOraniHesapla()
        self.haritaOlustur()     

    def depremYikimOraniHesapla(self):
        oran = 0

        if 1 <= self.siddet < 5:
            oran += 0
        elif 5 <= self.siddet < 6:
            oran += 0.1            
        elif 6 <= self.siddet < 6.1:
            oran += 0.15
        elif 6.1 <= self.siddet < 6.2:
            oran += 0.2
        elif 6.2 <= self.siddet < 6.3:
            oran += 0.4
        elif 6.3 <= self.siddet < 6.4:
            oran += 0.6
        elif 6.5 <= self.siddet < 6.6:
            oran += 1.5
        elif 6.6 <= self.siddet < 6.7:
            oran += 2
        elif 6.7 <= self.siddet < 6.8:
            oran += 3      
        elif 6.8 <= self.siddet < 6.9:
            oran += 4                                         
        elif 7 <= self.siddet < 7.1:
            oran += 8
        elif 7.1 <= self.siddet < 7.2:
            oran += 8.1
        elif 7.2 <= self.siddet < 7.3:
            oran += 8.2
        elif 7.3 <= self.siddet < 7.4:
            oran += 8.4
        elif 7.4 <= self.siddet < 7.5:
            oran += 8.7
        elif 7.5 <= self.siddet < 7.6:
            oran += 9.6
        elif 7.6 <= self.siddet < 7.7:
            oran += 9.8       
        elif 7.7 <= self.siddet < 7.8:
            oran += 9.9
        elif 7.8 <= self.siddet < 7.9:
            oran += 10.4                                                                                                                 
        elif 7.9 <= self.siddet < 8:
            oran += 11
        elif 8 <= self.siddet < 9:
            oran += 12
        elif 9 <= self.siddet < 11:
            oran += 13

        if 0 <= self.derinlik < 5: 
            oran += 5
        elif 5 <= self.derinlik < 6:
            oran += 4.8
        elif 6 <= self.derinlik < 8:
            oran += 4.5
        elif 8 <= self.derinlik < 10:
            oran += 4.3
        elif 10 <= self.derinlik < 14:
            oran += 4.1
        elif 14 <= self.derinlik < 18:
            oran += 3.8                                                       
        elif 18 <= self.derinlik < 22:
            oran += 3.5 
        elif 22 <= self.derinlik < 26:
            oran += 3.2
        elif 26 <= self.derinlik < 30:
            oran += 2.8
        elif 30 <= self.derinlik < 35:
            oran += 2.4
        elif 35 <= self.derinlik < 40:
            oran += 1.9
        elif 40 <= self.derinlik < 50:
            oran += 1.4                                               
        elif 50 <= self.derinlik < 60:
            oran += 0.9
        elif 60 <= self.derinlik < 300:
            oran += 0.3
        elif 300 <= self.derinlik:
            oran += 0

        if 0 <= self.sure < 10:
            oran += 0.2
        elif 10 <= self.sure < 20:
            oran += 0.7
        elif 20 <= self.sure < 25:
            oran += 1.1
        elif 25 <= self.sure < 30:
            oran +=  1.5   
        elif 30 <= self.sure < 35:
            oran += 1.8
        elif 35 <= self.sure < 40:
            oran += 2.1
        elif 40 <= self.sure < 45:
            oran += 2.3                     
        elif 45 <= self.sure < 50:
            oran += 2.6
        elif 50 <= self.sure:
            oran += 3


        if(self.siddet <= 6.7):
            oran = oran / 3.75
        if(self.siddet <= 6.5):
            oran = oran / 4.25
        if(self.siddet <= 6.3):
            oran = oran / 5 
        if(self.siddet <= 6.1):
            oran = oran / 6
        if(self.siddet <= 5.9):
            oran = oran / 7

        if(oran <= 0.2 and self.derinlik <= 10):
            oran = oran / 4

        return oran


        istanbul_latitude_range = (40.8027, 41.1691)
        random_latitude = random.uniform(istanbul_latitude_range[0], istanbul_latitude_range[1])
        return random_latitude
    
    def randomEnlem(self):
        istanbul_latitude_range = (40.8027, 41.1691)
        random_latitude = random.uniform(istanbul_latitude_range[0], istanbul_latitude_range[1])
        return random_latitude

    def randomBoylam(self):
        istanbul_longitude_range = (28.6324, 29.2265)
        random_longitude = random.uniform(istanbul_longitude_range[0], istanbul_longitude_range[1])
        return random_longitude

    def haritaOlustur(self):
        istanbul_map = folium.Map(location=[self.enlem, self.boylam], zoom_start=12)

        # Rastgele noktayı işaretle
        folium.Marker(location=[self.enlem, self.boylam], popup='Deprem Noktası').add_to(istanbul_map)

        # Haritayı göster
        istanbul_map.save('random_point_map.html')  # Haritayı bir HTML dosyasına kaydet

class Rapor():
    def __init__(self, ilce, binaSayisi, yikilanBinaSayisi, depremSiddeti, depremUzakligi, depremSuresi, depremDerinlik, deprem):
        self.ilce = ilce
        self.binaSayisi = binaSayisi
        self.yikilanBinaSayisi = yikilanBinaSayisi
        self.depremSiddeti = depremSiddeti
        self.depremUzakligi = depremUzakligi
        self.depremSuresi = depremSuresi
        self.depremDerinlik = depremDerinlik
        self.deprem = deprem

class ExcelRapor():
    def __init__(self, enlem, boylam, binaSayisi, yikilanBinaSayisi, deprem):
        self.enlem = enlem
        self.boylam = boylam
        self.binaSayisi = binaSayisi
        self.yikilanBinaSayisi = int(yikilanBinaSayisi*0.2)
        self.hasarliBinaSayisi = int(yikilanBinaSayisi*0.8)
        self.depremSiddeti = deprem.siddet
        self.depremSuresi = deprem.sure
        self.depremDerinlik = deprem.derinlik


ExcelRaporListesi = []
takipSayac = 0

for i in range(100):
    tekDepremBinaSayisi = 0
    tekDepremYikilanBinaSayisi = 0

    # yıkılan bina sayısı = orta hasarlı bina sayısı /4 yapılacak
    deprem = Deprem(7.5,10,30)

    with open('/Users/onurs/Desktop/binaBilgisi.txt', 'r') as dosya:
        # Dosya ile ilgili işlemleri gerçekleştirin
        satirlar = dosya.readlines()[1:]

    binaListesi = []
    raporListesi = []

    # Okunan satırları işleme almak
    for satir in satirlar:

        yikilanBinaSayisi = 0
        binaSayisi = 0

        # Satırı boşluklara göre ayırma
        parcalar = satir.strip().split('/')

        # Parçaların sayısını kontrol etme
        if len(parcalar) == 6:
            # Parçalardan istediğiniz bilgileri alabilirsiniz
            ilce = parcalar[0].strip()
            binaSayisi_2000Oncesi = int(parcalar[1].strip())
            binaSayisi_2000Sonrasi = int(parcalar[2].strip())
            risk_derecesi = parcalar[3].strip()
            enlem = float(parcalar[4].strip() )
            boylam = float(parcalar[5].strip())

        for index in range(binaSayisi_2000Oncesi):
            yapiDurumu = "Yeterli" if random.random() < 0.85 else "Yetersiz"
            bina = Bina(ilce=ilce,yas="2000_Oncesi", yapi=yapiDurumu, zemin=risk_derecesi, enlem=enlem, boylam=boylam, deprem=deprem)
            binaSayisi += 1
            if bina.yikildiMi == True:
                yikilanBinaSayisi+=1
            binaListesi.append(bina)

        for index in range(binaSayisi_2000Sonrasi):
            yapiDurumu = "Yeterli" if random.random() < 0.95 else "Yetersiz"
            bina = Bina(ilce=ilce,yas="2000_Sonrasi", yapi=yapiDurumu, zemin=risk_derecesi, enlem=enlem, boylam=boylam, deprem=deprem)
            binaSayisi += 1
            if bina.yikildiMi == True:
                yikilanBinaSayisi+=1
            binaListesi.append(bina)

        rapor = Rapor(ilce,binaSayisi,yikilanBinaSayisi,deprem.siddet,bina.depremUzakligi,deprem.sure,deprem.derinlik,deprem)
        raporListesi.append(rapor)
        tekDepremBinaSayisi += binaSayisi
        tekDepremYikilanBinaSayisi += yikilanBinaSayisi
        
    excelRapor = ExcelRapor(deprem.enlem,deprem.boylam,tekDepremBinaSayisi,tekDepremYikilanBinaSayisi,deprem)
    ExcelRaporListesi.append(excelRapor)
    takipSayac += 1
    print(takipSayac, ". deprem tamamlandi! (deprem yikim oranı = ",deprem.yikimOrani ," )")
        
"""    with open('rapor.html', 'w') as html_file:
        # HTML başlık ve başlangıç etiketlerini ekle
        html_file.write('<html>\n<head>\n<title>Rapor</title>\n<link rel="stylesheet" href="style.css">\n<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">\n</head>\n<body>\n')

        # Verileri içeren tabloyu oluştur
        html_file.write('<table border="1" class="tabloRapor table-borderless">\n')
        html_file.write('<tr><th class="lead">Şehir</th><th class="lead">Bina Sayısı</th><th class="lead">Yıkılan Bina Sayısı</th><th class="lead">Deprem Şiddeti</th><th class="lead">Deprem Süresi</th><th class="lead">Deprem Derinligi</th><th class="lead">Deprem Uzaklığı</th></tr>\n')
        yikilanBinaSayisi = 0
        binaSayisi = 0
        # Tabloya verileri ekle
        for rapor in raporListesi:
            html_file.write('<tr>')
            html_file.write(f'<td>{rapor.ilce}</td>')
            html_file.write(f'<td>{rapor.binaSayisi}</td>')
            html_file.write(f'<td>{rapor.yikilanBinaSayisi}</td>')
            html_file.write(f'<td>{rapor.depremSiddeti}</td>')
            html_file.write(f'<td>{rapor.depremSuresi}</td>')
            html_file.write(f'<td>{rapor.depremDerinlik}</td>')
            html_file.write(f'<td>{int(rapor.depremUzakligi)} km</td>')
            html_file.write('</tr>\n')
            yikilanBinaSayisi += rapor.yikilanBinaSayisi 
            binaSayisi += rapor.binaSayisi


        html_file.write(f'<td></td><td>{binaSayisi}</td><td>{yikilanBinaSayisi}</td></table>\n')

        # iframe'i tablonun altına ekle
        html_file.write('<iframe class="iframeMap" src="random_point_map.html" frameborder="0"></iframe>\n')

        # HTML etiketlerini kapat
        html_file.write('</body>\n</html>')

    os.system("rapor.html")"""


# Deprem özelliklerini çıkarmak
deprem_data = {'deprem_enlem': deprem.enlem,'deprem_boylam': deprem.boylam,'bina_sayisi':binaSayisi,'yikilan_bina': int(yikilanBinaSayisi*0.2),'hasarli_bina': int(yikilanBinaSayisi*0.8),'deprem_siddeti': deprem.siddet, 'deprem_suresi': deprem.sure, 'deprem_derinligi': deprem.derinlik}

# Her bir bina nesnesinin özelliklerini bir liste olarak al
excel_listesi = [vars(excelRapor) for excelRapor in ExcelRaporListesi]

# Bina ve deprem verilerini birleştirerek genel bir DataFrame oluştur
genel_df = pd.DataFrame(excel_listesi)

# Excel dosyasına yaz
genel_df.to_excel('rapor2.xlsx', index=False, sheet_name='Bina_ve_Deprem_Ozellikleri')