#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont
import obd
import random
from obd import OBDStatus
obd.logger.setLevel(obd.logging.DEBUG)
ports = obd.scan_serial()      # return list of valid USB or RF ports
print(ports) 
sys.path.append(".")
sys.path.append("/home/pi/zegary")
import threading
# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
disp = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device),spi_freq=20000000,rst=RST,dc=DC,bl=BL)
disp.Init()
disp.clear()
disp.bl_DutyCycle(30)
wskaznik = Image.open('wskaznikpaliwa.png')	
wskaznik2 = Image.open('wskaznikpaliwa2.png')
# from obd import OBDCommand, Unit
# from obd.utils import bytes_to_int
# from obd.protocols import ECU
# def obliczenie(messages):
#     d = messages[0].data
#     d = d[2:]
#     v = bytes_to_int(d) / 4.0
#     return v*100/255
# komendapaliwo = OBDCommand("Stan_Paliwa", "Stan Paliwa W procentach", b"22002F", 4, obliczanie, ECU.ALL) #jest opcja ze nie 35FE3 tylko 22002F albo 221155 w chuj prawdopodobne chat gpt sie zgadza i w sumie reszta tez ze mode 22 a pid 002F (2 pierwsze=mode reszta to pid)
#https://docs.google.com/spreadsheets/d/1HgWCnosdRqZYoWHEl7ylAxjxv4UFVeisWiR7gcr8H6I/edit#gid=0
#Lista pid GM
#connection.supported_commands.add(komendapaliwo)
# def polaczenie():
#     global connection
#     print("lacze sie")
#     connection = obd.OBD()
#     if connection.status() == OBDStatus.CAR_CONNECTED: return True
#     else: return False

    
def paliwko():  
#     if polaczenie() == True: 
#         # paliwo = connection.query(obd.commands.FUEL_LEVEL)
#         paliwo = connection.query(komendapaliwo)
#         print("Nie polaczono z autem")
#     else:      
        # while polaczenie() == False:
        #     print("Nie udane polaczenie")
        #     brak = Image.new("RGB", (disp.width, disp.height), "BLACK")
        #     rys = ImageDraw.Draw(brak)
        #     Font1 = ImageFont.truetype("COMIC.TTF",30)
        #     rys.text((5, 90), "Brak polaczenia\n z autem", fill= "WHITE", font=Font1)
        #     disp.ShowImage(brak)
        #     time.sleep(2)
    paliwo = random.randint(0,100)
    if paliwo < 15: kolor = [200, 48, 35]  
    if paliwo >= 15: kolor = [201, 84, 0]
    if paliwo >= 30: kolor = [168, 107, 0]
    if paliwo >= 50: kolor = [131, 123, 0]
    if paliwo >= 70: kolor = [91, 133, 0]
    if paliwo >= 90 : kolor = [30,139,30]
    image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)
    time.sleep(0.2)
    draw.line([(120, 226),(120, 226-212*paliwo*0.01)], fill = (kolor[0],kolor[1],kolor[2]),width = 58)
    if paliwo < 15: 
        image1.paste(wskaznik2, (0, 0), mask=wskaznik2)
    else:
        image1.paste(wskaznik, (0, 0), mask=wskaznik)
    procent = Image.new("RGBA", (disp.width, disp.height), (255, 0,0,0))
    Font1 = ImageFont.truetype("COMIC.TTF",35)
    procentd = ImageDraw.Draw(procent)
    procentd.text((168, 93), str(paliwo) , fill = (kolor[0],kolor[1],kolor[2]),font=Font1)
    image1.paste(procent, (0,0), mask=procent)
    disp.ShowImage(image1)

# t1 = threading.Thread(target=paliwko())
# t2 = threading.Thread(targe=temperatura())
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
    
while True:
    paliwko()
    
    
    
