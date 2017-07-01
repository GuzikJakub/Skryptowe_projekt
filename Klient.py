__author__ = 'guzik_000'

import socket
import sys
import time
import hashlib
import random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Klient(object):
    def __init__(self):
        self.Komisja1_Address = ("127.0.0.1", 30001)
        self.PKW_Address = ("127.0.0.1", 40002)
        self.Komisja1_Socket = socket.socket()
        self.PKW_Socket = socket.socket()
        #self.Bob_Server_Name = "Bob_Server"
        self.login = ""
        self.Pierwsza_decyzja()
        #self.Druga_decyzja("79c6b3")

    def hasz_nonce(self, login, nonce):
        zmienna = login+nonce
        hash = hashlib.sha224(zmienna).hexdigest()
        return hash


    def Pierwsza_decyzja(self):
        '''

        :return:
        '''
        self.Komisja1_Socket.connect(self.Komisja1_Address)
        # info = raw_input("podaj tekst")

        mail = raw_input("Podaj mail: ")
        self.Komisja1_Socket.send(mail)
        odpowiedz = self.Komisja1_Socket.recv(120)
        if odpowiedz == "True":
            print("Jestes uprawniony do glosowania. Sprawdz maila.")
            print(mail)
            nonce2 = raw_input("Podaj PIN: ")
            hash = self.hasz_nonce(mail, nonce2)
            self.Komisja1_Socket.send(hash)
            upr = self.Komisja1_Socket.recv(120)
            if upr == "OK":
                self.Komisja1_Socket.close()
                self.Druga_decyzja(str(nonce2))
            else:
                print("Nie masz uprawnienia glosowania.")
                self.Komisja1_Socket.close()
        else:
            print("Nie jestes uprawniony do glosowania")

    def generuj_glosy(self, tab, PIN):
        napis2 = []

        for i in range(0,len(tab)-1):
            napis = PIN+self.create_nonce()+"@"
            for j in range(0,len(tab)-1):
                if i==j:
                    napis += tab[j]+"#X#"
                else:
                    napis += tab[j] +"#0#"
            napis2.append(napis)
        return self.to_string(napis2)

    def to_string(self, tab):
        string = ""
        for i in range(0,len(tab)):
            string += tab[i]+"$"
        return string

    def create_nonce(self):
        '''

        :return:
        '''
        czas = str(time.time())+str(random.random())
        hash_time =  hashlib.sha224(czas).hexdigest()
        nonce = ""
        for i in range(0,len(hash_time)):
            if i%10== 0:
                nonce+=hash_time[i]

        return nonce

    def generate_key(self):
        czas = str(time.time())
        hash_time =  hashlib.sha224(czas).hexdigest()+str(random.random())
        nonce = ""
        for i in range(0,len(hash_time)):
            if i%3== 0:
                nonce+=hash_time[i]
        if len(nonce) == 23:
            nonce += "0"
        return nonce

    def encript_data(self, mess, key):
        obj = AES.new(str(key), AES.MODE_CBC, 'This is an IV456')
        while len(mess)%16 != 0:
            mess += '0'
        ciphertext = obj.encrypt(mess)
        return ciphertext

    def encript_keys(self, public_key, my_key):
        rsakey = RSA.importKey(public_key)
        rsakey = PKCS1_OAEP.new(rsakey)
        encrypted = rsakey.encrypt(my_key)
        return encrypted

    def decrypt_data_AES(self, mess, key):
        obj2 = AES.new(key, AES.MODE_CBC, 'This is an IV456')
        return obj2.decrypt(mess)

    def menu(self):
        mess = "Na Kogo glosujesz? \n"
        mess+= "1-WDI\n"
        mess+= "2-ASD\n"
        mess+= "3-TJA\n"
        odp = raw_input(mess)
        return odp

    def glosuj_na_WDI(self,karty):
        tab = karty.split("$")
        for i in range(0,len(tab)): #najwyzej -1
            tab3 = tab[i].split("@")
            tab2 = tab3[1].split("#")
            for j in range(0,len(tab2)):
                if str(tab2[j]) == "WDI":
                    if str(tab2[j+1]) == "X":
                        return tab[i]

    def glosuj_na_ASD(self,karty):
        tab = karty.split("$")
        for i in range(0,len(tab)): #najwyzej -1
            tab3 = tab[i].split("@")
            tab2 = tab3[1].split("#")
            for j in range(0,len(tab2)):
                if str(tab2[j]) == "ASD":
                    if str(tab2[j+1]) == "X":
                        return tab[i]

    def glosuj_na_TJA(self,karty):
        tab = karty.split("$")
        for i in range(0,len(tab)): #najwyzej -1
            tab3 = tab[i].split("@")
            tab2 = tab3[1].split("#")
            for j in range(0,len(tab2)):
                if str(tab2[j]) == "TJA":
                    if str(tab2[j+1]) == "X":
                        return tab[i]

    def Druga_decyzja(self, PIN):
        self.PKW_Socket.connect(self.PKW_Address)
        tab = self.PKW_Socket.recv(120)
        tablica = tab.split("$")
        napis = self.generuj_glosy(tablica,PIN)
        # print self.generate_key()
        key = self.generate_key()
        #print(len(key))
        #print key
        lala = self.encript_data(napis, key)
        self.PKW_Socket.send(lala)
        numer = self.PKW_Socket.recv(120) #potem tablica
        public_key = self.PKW_Socket.recv(480)
        en_key = self.encript_keys(public_key, key)
        self.PKW_Socket.send(en_key)
        odp = self.PKW_Socket.recv(120)
        karty_moje = self.PKW_Socket.recv(512)
        karty_moje2 = self.decrypt_data_AES(karty_moje, key)
        menu_odp = self.menu()
        if str(menu_odp) == "1":
            karta_WDI = self.glosuj_na_WDI(karty_moje2)
            wyslij_WDI = self.encript_keys(public_key, karta_WDI)
            self.PKW_Socket.send(wyslij_WDI)
            self.PKW_Socket.send("1")
        elif str(menu_odp) == "2":
            karta_ASD = self.glosuj_na_ASD(karty_moje2)
            wyslij_ASD = self.encript_keys(public_key, karta_ASD)
            self.PKW_Socket.send(wyslij_ASD)
            self.PKW_Socket.send("2")
        elif str(menu_odp) == "3":
            karta_TJA = self.glosuj_na_TJA(karty_moje2)
            wyslij_TJA = self.encript_keys(public_key, karta_TJA)
            self.PKW_Socket.send(wyslij_TJA)
            self.PKW_Socket.send("3")
        else:
            print("Zlyw wybor")
        odpowiedz_ostateczna = self.PKW_Socket.recv(120)
        print(odpowiedz_ostateczna)
        self.PKW_Socket.close()





kli = Klient()
