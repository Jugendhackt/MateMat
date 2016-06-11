
# coding: utf-8

import RPi.GPIO as GPIO
import random
import io
import time
import picamera
import qrtools

#Bestätigungen
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
bestaetigung1="nein"
bestaetigung2="nein"
bestaetigung3="nein"
#Profilkram
profilnr=str(random.randint(1000, 9999))+"\n"
alter=0
name=""
profilvorname=""
profilnachname=""
profilalter=0
mate=4
qrcode=""
uses="aktiv"
einloesen="nein"
data=""

while uses=="aktiv":
    GPIO.output(16, 1)
    GPIO.output(20, 0)
    neuesprofil = raw_input("Möchtest du ein neues Mateprofil erstellen? Oder hast du schon eines?[Ja/Nein] ")
    if neuesprofil == "Ja" or neuesprofil =="ja":
        print("Deine Profilnummer lautet {}".format(profilnr))
        while bestaetigung1 != "Ja":
            name1 = raw_input("Bitte gib deinen Vornamen ein. ")
            profilvorname=name1
            name2 = raw_input("Bitte gib deinen Nachnamen ein. ")
            profilnachname=name2
            bestaetigung1=raw_input("Willst du deinen Profilnamen als {} {} bestätigen?[Ja/Nein]".format(profilvorname, profilnachname))
            if bestaetigung1=="Ja":
                print("Du hast erfolgreich deinen Namen eingegeben {} !".format(profilvorname))

        while bestaetigung2 != "Ja" or alter < 12 or alter > 80:
            alter =raw_input ("Bitte gib dein korrektes Alter an! ")
            alter=int(alter)
            if alter < 12 or alter > 80:
                print("Du bist ausserhalb der Altersbegrenzung (von 12-80) Alter: {}".format(alter))
            if alter > 12 and alter < 80:
                profilalter=alter
                bestaetigung2 = raw_input("Willst du dein Alter mit {} Jahren bestätigen?[Ja/Nein] ".format(profilalter))
                if bestaetigung2 == "Ja":
                    print("Du hast dein Alter angegeben ({} Jahre).".format(profilalter))
                    while bestaetigung3=="Ja":
                        bestaetigung3=raw_input("Möchtest du deinen Account fertigstellen? Fertigstellen[Ja]")
                        if bestaetigung3 == "Ja":
                            print("Dein Account wurde fertiggestellt! (Trink nicht so viel!)")
                        else:
                            print ("Fülle das Formular erneut aus!")
    if neuesprofil=="dev":
        print("Willkommen im Developermodus")
        profilvorname="Developer"
        profilnachname="X"
        profilalter=14
        mate=100
        profilnr=1
        profilnummer=int(profilnr)
        einloesen =raw_input("Willst du den QRCode testen?[Ja]")
    
    if neuesprofil == "Nein" or neuesprofil == "nein" or einloesen =="ja" or einloesen=="Ja":
        profilnummer =raw_input("Wenn du deine Anmeldedaten sehen willst, gib deine Profilnr ein! ")
        profilnummer=int(profilnummer)
        if profilnummer == profilnr:
            print("Hallo, {} du hast noch {} Mate frei!".format(profilvorname, mate))
            qrcode = raw_input("Halte dein Gerät mit dem QR-Code an den Scanner.")
            qr = qrtools.QR()
            my_file = open('my_image.jpg', 'wb')
            with picamera.PiCamera() as camera:
                camera.start_preview()
                time.sleep(5)
                camera.capture(my_file)
            qr.decode("my_image.jpg")
            data=(qr.data)[:-1]
            #print(data)
            #print(qr.data)
            if str(profilnr) == str(qr.data):
                #print("acces")
                qrcode="true"
                if mate > 0 and qrcode=="true":
                    mate=mate-1
                    print("Du bekommst eine Mateflasche und hast noch {} übrig.".format(mate))
                    GPIO.output(16, 0)
                    GPIO.output(20, 1)
                    time.sleep(5)
                    GPIO.output(16, 1)
                    GPIO.output(20, 0)
                    if mate == 0:
                        uses="inaktiv"

