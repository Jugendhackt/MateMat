#coding: utf-8

import RPi.GPIO as GPIO
import random
import io
import time
import uuid
import json

import os
import os.path

import picamera
import qrtools


GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

class AutomatNutzer(object):
    def __init__(self): 
        self._uuid = str(uuid.uuid4()) 
        self.mateAnzahl = 50 # Da wir ja keinen Sensor haben um die Flaschen zu zählen!
        self.jsonDump = {
        "mateAnzahl": self.mateAnzahl,
        "accounts": []
        }
    
    def setName(self):
        self.firstName = raw_input("[?] Bitte gib deinen Vornamen ein! ")
        self.lastName = raw_input("[?] Bitte gib deinen Nachnamen ein! ")
        
        hasName = raw_input("[?] Ist das dein Name: {} {} [j/n]".format(self.firstName, self.lastName))
        hasName = hasName.lower()
        
        
        if hasName == 'n':
            self.setName()
        elif hasName == 'j':
            return [self.firstName, self.lastName]

    def setAge(self):
        self.age = int(raw_input ("[?] Bitte gib dein korrektes Alter an! "))

        if self.age <= 12:
            print("[-] Du bist leider zu jung")
            return

        else:
            hasAge = raw_input("[?] Bist du wirklich {} Jahre alt? [j/n] ".format(self.age))
            hasAge = hasAge.lower()

            if hasAge == "j":
                print("[*] Dein Account wurde fertiggestellt! (Trink nicht so viel!)")
                return self.age
            else:
                print ("[-] Fülle das Formular erneut aus!")
                self.main()

    def writeJson(self, jsonDict):
        if os.path.isfile("./userDatabase.json") == False:
            with open("userDatabase.json", 'a'):
                os.utime("userDatabase.json", None)
            with open("userDatabase.json", 'w') as jsonFile:
                jsonFile.write('[]') #creating json!

        with open('userDatabase.json','r') as jsonFile:
            data = json.load(jsonFile)
            data.append(jsonDict)

    def main(self):
        while self.mateAnzahl > 0:
            GPIO.output(16, 1)
            GPIO.output(20, 0)

            newProfile = raw_input("[?] Möchtest du ein neues Mate-Profil erstellen? [j/n] ")
            newProfile = newProfile.lower()

            if newProfile == "j":
                # Warum auch immer man den Namen für einen Mate Automaten braucht...
                names = self.setName()
                self.jsonDump["accounts"].append({'uuid':self._uuid,'age':self.setAge(),'firstName': names[0], 'lastName': names[1] })
                jsonDict = json.dumps(self.jsonDump)

                print("[*] Deine UUID lautet {}".format(self._uuid))
                
                self.writeJson(jsonDict)

            elif newProfile == "n":
                profilnummer =raw_input("[?] Gebe deine UUID zum einloggen ein!")

                if profilnummer == self._uuid:
                    print("[*] Hallo, {}! Im Automaten befinden sich gerade {} Flaschen Mate!".format(self.firstName, self.mateAnzahl))
                    print("[*] Halte dein Gerät mit dem QR-Code an den Scanner.")

                    qr = qrtools.QR()
                    my_file = open('my_image.jpg', 'wb')
                    with picamera.PiCamera() as camera:
                        camera.start_preview()
                        time.sleep(5)
                        camera.capture(my_file)
                    qr.decode("my_image.jpg")
                    data = (qr.data)[:-1]

                    if self._uuid == str(qr.data):
                        if self.mateAnzahl > 0:
                            self.mateAnzahl -= 1
                            print("[*] Der Automat hat noch {} Flaschen Mate übrig.".format(self.mateAnzahl))
                            
                            GPIO.output(16, 0)
                            GPIO.output(20, 1)
                            
                            time.sleep(5)
                            
                            GPIO.output(16, 1)
                            GPIO.output(20, 0)
                    else:
                        print("[-] Der QR-Code wurde nicht richtig erkannt oder ist fehlerhaft.")

automat = AutomatNutzer()
automat.main()