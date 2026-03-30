import os
import sys 
import time
import logging
from PIL import Image,ImageDraw,ImageFont,ImageShow,ImageOps
import random
import math
#nie do predkosciomierzow
#import spidev as SPI
#from lib import LCD_1inch28
sys.path.append("..")
#tylko do predkosciomierzow
import cv2
import numpy
import obd
import multiprocessing
# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
#konfiguracja wyswietlacza
# disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=20000000,rst=RST,dc=DC,bl=BL)
# disp.Init()
# disp.clear()
# disp.bl_DutyCycle(30)
#Polaczenie OBD
connection = obd.OBD()
def polaczenie():
    print("lacze sie")
    if connection.is_connected(): 
        connection.protocol_name("ISO 14230-4 (KWP FAST)")
        return True
        
    else: return False

#wymiary zegara 1
rozmiarx1 = 500
rozmiary1 = 500
#wymiary zegara 2
rozmiarx2 = 500
rozmiary2 = 500

#Parametry dla wyswietlacza
rozmiarx = 1024
rozmiary = 600
szparax = int((rozmiarx-rozmiarx1-rozmiarx2)/2)
szparay = int((rozmiary-rozmiary1)/5)
grubosc = rozmiarx1*0.02083
Font1 = ImageFont.truetype("COMIC.TTF",int(grubosc*2.35))
predkosciomierz = Image.new("RGBA", (rozmiarx1,rozmiary1))
rysunekp = ImageDraw.Draw(predkosciomierz)
obrotomierz = Image.new("RGBA", (rozmiarx2,rozmiary2))
rysuneko = ImageDraw.Draw(obrotomierz)
#MENU
rozmiarxmenu = int(rozmiarx/4.5)
rozmiarymenu = int(rozmiary/4.5)
ikonapaliwa = Image.open("ikonapaliwa.png")
ikonaprzebieg = Image.open("ikonaprzebieg.png")
ikonainne = Image.open("ikonainne.png")
ikonaugabuga = Image.open("ugabuga.png")

final = Image.new("RGBA", (rozmiarx,rozmiary))
#maska tla zegara
size = (int(rozmiarx1*1.002), int(rozmiary1*1.002))
mask = Image.new('L', size, 0)
draw = ImageDraw.Draw(mask) 
draw.ellipse((0, 0) + size, fill=255)
#otwarcie i zmiana rozmiaru
im1 = Image.open('1.png')
im1 = im1.resize((rozmiarx1,rozmiary1))
im2 = Image.open('2.png')
im2 = im2.resize((rozmiarx1,rozmiary1))
im3 = Image.open('3.png')
im3 = im3.resize((rozmiarx1,rozmiary1))
im4 = Image.open('4.png')
im4 = im4.resize((rozmiarx1,rozmiary1))

#wyciecie
out1 = ImageOps.fit(im1, mask.size, centering=(0.5, 0.5))
out1.putalpha(mask)
out2 = ImageOps.fit(im2, mask.size, centering=(0.5, 0.5))
out2.putalpha(mask)
out3 = ImageOps.fit(im3, mask.size, centering=(0.5, 0.5))
out3.putalpha(mask)
out4 = ImageOps.fit(im4, mask.size, centering=(0.5, 0.5))
out4.putalpha(mask)



#Stworzenie obreczy predkosciomierza
def zrobobreczp(kolorobrecz):
    #wyznaczenie przedzialki
    i=0
    #ilosc skokow
    t=23
    skok = 290/t
    # skok2 = 290/t*1.07
    predkosc = 0
    while(i < t):
        kat = (i * skok + 130) * math.pi/180
        kat2 = (i * skok + 130) * math.pi/180
        x = rozmiarx1/2 + (rozmiarx1/2-2) * math.cos(kat)
        y = rozmiary1/2 + (rozmiary1/2-2) * math.sin(kat)
        x2 = rozmiarx1/2 + (rozmiarx1*0.401) * math.cos(kat)
        y2 = rozmiary1/2 + (rozmiary1*0.401) * math.sin(kat)
        x3 = rozmiarx1*0.422 + rozmiarx1*0.25 * math.cos(kat2)
        y3 = rozmiary1*0.422 + rozmiary1*0.25 * math.sin(kat2)
        x4 = rozmiarx1/2 + (rozmiarx1*0.43) * math.cos(kat) #Do mniejszych kresek
        y4 = rozmiary1/2 + (rozmiary1*0.43)* math.sin(kat)
        if (predkosc == 50):
            kolor = "red"
        else:
            kolor="blue"
        textx = (x2+x3)/2
        texty = (y2+y3)/2
        if(i % 2 == 0):
            rysunekp.line([(x,y),(x2,y2)], fill=kolor,width=int(grubosc))
            rysunekp.text((textx,texty),str(predkosc),fill=kolor, font=Font1)
        else:
            rysunekp.line([(x,y),(x4,y4)], fill=kolor,width=int(grubosc*0.8))
      
        
        predkosc +=10
        i += 1
    rysunekp.ellipse([(0,0),(rozmiarx1,rozmiary1)],outline=kolorobrecz,width=int(grubosc*1.31))

#Stworzenie tla obrotomierza

def zrobobreczo(kolorobrecz):
    #wyznaczenie przedzialki
    io=0
    #ilosc skokow
    to=9
    skoko = 241.5/to
    skok2o = 241.5/to*1.07
    obrotyw = 0
    while(io < to):
        kato = (io * skoko + 130) * math.pi/180
        kat2o = (io * skok2o + 120) * math.pi/180
        xo = rozmiarx2/2 + (rozmiarx2/2-2) * math.cos(kato)
        yo = rozmiary2/2 + (rozmiary2/2-2) * math.sin(kato)
        x2o = rozmiarx2/2 + (rozmiarx2*0.41666) * math.cos(kato)
        y2o = rozmiary2/2 + (rozmiary2*0.41666) * math.sin(kato)
        x3o = rozmiarx2*0.42666 + rozmiarx2*0.308333 * math.cos(kat2o)
        y3o = rozmiary2*0.42666 + rozmiary2*0.308333 * math.sin(kat2o)
        if (obrotyw > 6):
            koloro="red"
        else:
            koloro="blue"
        rysuneko.line([(xo,yo),(x2o,y2o)], fill=koloro,width=int(grubosc))
        textxo = (x2o+x3o)/2
        textyo = (y2o+y3o)/2
        rysuneko.text((textxo,textyo),str(obrotyw),fill=koloro, font=Font1)
        obrotyw +=1
        io += 1
    rysuneko.ellipse([(0,0),(rozmiarx1,rozmiary1)],outline=kolorobrecz,width=int(grubosc*1.33))
wysmoothowane= []
def smooth_speed(nowa, wysmoothowane, ile):
    if len(wysmoothowane) < ile:
        wysmoothowane.append(nowa)
    else:
        wysmoothowane.pop(0)
        wysmoothowane.append(nowa)
    
    WartoscWysmoothowana = sum(wysmoothowane) / len(wysmoothowane)
    return WartoscWysmoothowana
wysmoothowane2= []
def smooth_rev(nowa, wysmoothowane2, ile):
    if len(wysmoothowane2) < ile:
        wysmoothowane2.append(nowa)
    else:
        wysmoothowane2.pop(0)
        wysmoothowane2.append(nowa)
    
    WartoscWysmoothowana2 = sum(wysmoothowane2) / len(wysmoothowane2)
    return WartoscWysmoothowana2   

def renderpredkosc(aktualna, predkosciomierz2):
    rysunek2 = ImageDraw.Draw(predkosciomierz2)
    skokp = 1.26 #skok predkosci
    aktualna = smooth_speed(aktualna, wysmoothowane, 3)
    kat = (aktualna * skokp + 130) * math.pi/180
    x = rozmiarx1/2 + rozmiarx1/2 * math.cos(kat)
    y = rozmiary1/2 + rozmiary1/2 * math.sin(kat)
    #print("X=" + str(x)  + "Y=" + str(y))
    rysunek2.line([(x,y),(rozmiarx1/2,rozmiary1/2)], fill="blue",width=int(grubosc/2.5))
    
    rysunek2.ellipse([(rozmiarx1/2-grubosc,rozmiary1/2-grubosc),(rozmiarx1/2+grubosc,rozmiary1/2+grubosc)],fill="red")
    #print(aktualna)
    #do predkosciomierzow
    cv2.imshow('final', cv2.cvtColor(numpy.array(final), cv2.COLOR_RGB2BGR)) 
    cv2.waitKey(1)
    #disp.ShowImage(final)
    #print(aktualna)
def renderobroty(aktualneobroty, obroty2):
    rysuneko2 = ImageDraw.Draw(obroty2)
    skoko = 0.02683333333
    aktualneobroty = smooth_rev(aktualneobroty, wysmoothowane2, 3)
    kat = (aktualneobroty * skoko + 130) * math.pi/180
    xo = rozmiarx2/2 + rozmiarx2/2 * math.cos(kat)
    yo = rozmiary2/2 + rozmiary2/2 * math.sin(kat)
    rysuneko2.line([(xo,yo),(rozmiarx2/2,rozmiary2/2)], fill="blue",width=int(grubosc/2.5))
    rysuneko2.ellipse([(rozmiarx2/2-grubosc,rozmiary2/2-grubosc),(rozmiarx2/2+grubosc,rozmiary2/2+grubosc)],fill="red")
    

#cv2.namedWindow('final', cv2.WINDOW_NORMAL)
#cv2.setWindowProperty('final', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def otrzymywaniewartosci(tobroty,tpredkosc):
    #tobroty = connection.query(obd.commands.RPM)
    #tpredkosc = connection.query(obd.commands.SPEED)
    #wyjscieobd = [tobroty.value.magnitude, tpredkosc.value.magnitude]
    if (tobroty > 8000):
        tobroty = 0
    else:
        tobroty += 150
    if (tpredkosc > 190):
        tpredkosc = 0
    else:
        tpredkosc += 1
    wyjscieobd = [tobroty,tpredkosc]
    return wyjscieobd
    
    

def renderowaniezegarow(predkosciomierz2, obroty2,wyjscieobd):
    #renderpredkosc(random.randrange(0,190))
    renderpredkosc(wyjscieobd[1], predkosciomierz2)
    #renderobroty(random.randrange(0,8000))
    renderobroty(wyjscieobd[0], obroty2)
    final.paste(predkosciomierz, (0,0+szparay))
    warunkowekolory(wyjscieobd)
    rendermenu()
    final.paste(predkosciomierz, (0,0+szparay),mask=predkosciomierz)  
    final.paste(predkosciomierz2, (0,0+szparay), mask=predkosciomierz2)
    final.paste(obrotomierz, (rozmiarx1+2*szparax,0+szparay),mask=obrotomierz)
    final.paste(obroty2, (rozmiarx1+2*szparax,0+szparay), mask=obroty2)
    cv2.imshow('final', cv2.cvtColor(numpy.array(final), cv2.COLOR_RGB2BGR)) 
    cv2.waitKey(1)
    time.sleep(0.05)
    
def warunkowekolory(wyjscieobd):
    zmienione = 0
    if(wyjscieobd[1] > 160):
        zrobobreczp("#e64600")
        zrobobreczo("#e64600")
        final.paste(out4, (rozmiarx1+2*szparax,0+szparay),mask=mask)
        final.paste(out4, (0,0+szparay),mask=mask)
        zmienione = 1
    elif(wyjscieobd[1] > 145):
        zrobobreczp("#e6a200")
        zrobobreczo("#e6a200")
        final.paste(out3, (rozmiarx1+2*szparax,0+szparay),mask=mask)
        final.paste(out3, (0,0+szparay),mask=mask)
        zmienione = 1
    elif(wyjscieobd[1] > 125):
        zrobobreczp("#ccb600")
        zrobobreczo("#ccb600")
        final.paste(out2, (rozmiarx1+2*szparax,0+szparay),mask=mask)
        final.paste(out2, (0,0+szparay),mask=mask)
        zmienione = 1
    else:
        if(zmienione == 1):
            zrobobreczp("blue")
            zrobobreczo("blue")
            zmienione == 0 
        final.paste(out1, (rozmiarx1+2*szparax,0+szparay),mask=mask)  
        final.paste(out1, (0,0+szparay),mask=mask)  




elementy = ["Spalanie","Przebieg", "Inne Wartosci"]
elementynazwy = [ikonapaliwa,ikonaprzebieg,ikonainne]
iloscelementow = len(elementy)
iloscelementownazwy = len(elementynazwy)
wysokoscsrodek = int(rozmiarymenu-(grubosc*0.9))
szerokoscsrodek = int(rozmiarxmenu-(grubosc*0.9))
wielkoscikonay = int((wysokoscsrodek/iloscelementow)-((grubosc*0.4)))
wielkoscikonax = int((szerokoscsrodek/6))

for u in range(iloscelementownazwy):
    elementynazwy[u]= elementynazwy[u].resize((wielkoscikonax,wielkoscikonay))

def rendermenu():
    menu = Image.new("RGBA",(rozmiarxmenu,rozmiarymenu),color=0)
    menur = ImageDraw.Draw(menu)
    menur.rectangle([(0,0),(rozmiarxmenu,rozmiarymenu)],outline="blue",width=int(grubosc*0.6))
    odstep = wysokoscsrodek/iloscelementow
    Font2 = ImageFont.truetype("COMIC.TTF",int(wielkoscikonay*0.6))
    for u in range(iloscelementow):
        menur.line([(grubosc*0.9,(u*odstep)),(szerokoscsrodek,(u*odstep))],fill="blue",width=int(grubosc*0.3))
    for u in range(iloscelementownazwy):
        if u==0:
            menu.paste(elementynazwy[u],(int((grubosc*0.7)),int((grubosc*0.7))),mask=elementynazwy[u])
            wymiarypierwszego = (int((grubosc*0.9)+wielkoscikonax),int(grubosc*0.7))
            menur.text(wymiarypierwszego,text=elementy[u],font=Font2)
        else:
            menu.paste(elementynazwy[u],(int((grubosc*0.7)),int((grubosc*0.5)+(u*odstep))),mask=elementynazwy[u])
            wymiarynastepnych = (int((grubosc*0.9)+wielkoscikonax),int((grubosc*0.5)+odstep*(u)))
            menur.text(wymiarynastepnych,text=elementy[u],font=Font2)
    
    
    final.paste(menu,(int((rozmiarx/2)-rozmiarxmenu/2),int(rozmiary-rozmiarymenu)),mask=menu)


Brak = Image.new("RGBA",(rozmiarx,rozmiary),color="black")
def run():
    tobroty = 0
    tpredkosc =0
    zrobobreczp("blue")
    zrobobreczo("blue")
    predkosciomierz2 = Image.new("RGBA", (rozmiarx1,rozmiary1), (0,0,0,0))
    obroty2 = Image.new("RGBA", (rozmiarx2,rozmiary2),(0,0,0,0))
    while(True):
        if polaczenie() == False:
            print("Polaczony")
            wyjscieobd = otrzymywaniewartosci(tobroty,tpredkosc)
            thread = multiprocessing.Process(target=renderowaniezegarow, args=(predkosciomierz2, obroty2, wyjscieobd))
            if __name__ == '__main__':
                thread.start()
                thread.join()
            continue
        else:
            print("Nie Polaczony")
            rysbrak = ImageDraw.Draw(Brak)
            Font3 = ImageFont.truetype("COMIC.TTF",int(grubosc*3))
            rysbrak.text((szparax,szparay),"Brak polaczenia z autem Proba polaczenia",font=Font3)
            cv2.imshow('final', cv2.cvtColor(numpy.array(Brak), cv2.COLOR_RGB2BGR)) 
            cv2.waitKey(1)
            time.sleep(1)
run()



    
