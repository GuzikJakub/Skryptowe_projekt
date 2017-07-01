__author__ = 'Radek'

import smtplib
import socket
import thread
import hashlib
import time
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES

tablica_przedmiotow = ["WDI", "ASD", "TJA"]
def get_public_key():
    key = open('public_key.dat', "r").read()
    return key

def decrypt_data_AES(mess, key):
    obj2 = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    return obj2.decrypt(mess)


def decrypt_data(message):
    key = open('private_key.dat', "r").read()
    rsakey = RSA.importKey(key)
    rsakey = PKCS1_OAEP.new(rsakey)
    decrypted = rsakey.decrypt(message)
    return decrypted


def to_string(tab):
    string = ""
    for i in range(0,len(tab)):
        string += tab[i]+"$"
    return string

def take_id(nonce):
    id = ""
    for i in range (0,6):
        id += nonce[i]
    return id

def check_id(nonce):
    id = ""
    for i in range (0,6):
        id += nonce[i]
    myFile = open('uprawnieni.dat', 'r')
    for line in myFile:
        tmp = line.split('#')
        if id == tmp[0]:
            return True
    return False

def check_one_X(karta):
    tab = karta.split("#")
    glos = 0
    for i in range (0, len(tab)-1):
        if tab[i+1] == "X":
            glos += 1
        i += 1
    if glos == 1:
        return True
    else:
        return False

def find_by_name(my_table):
    if len(my_table)!=len(tablica_przedmiotow):
        return False

    # my_table[1] = "BD"
    count = 0;
    for i in range(0,len(tablica_przedmiotow)):
        for j in range(0,len(my_table)):
            if tablica_przedmiotow[i] == my_table[j]:
                count+=1;

    # print("dlugosc"+ str(count))
    if count == len(tablica_przedmiotow):
        return True
    return False


def check_name_vote(karta):
    tab = karta.split("#")
    tab2 = []
    for i in range (0,len(tab)-1):
        if i%2 == 0:
            tab2.append(tab[i])
    #tablica 2 przechowuje same przedmioty np[wdi,wmd, tja]
    # print("dlugosc "+str(len(tab2)))
    odp = find_by_name(tab2)#sprawdza czy nazwy sa ok

    if odp == True:
        return True
    return False

def check_cart(karty):
    # print(karty)
    tab = karty.split("$")
    for i in range (0, len(tab)-1):
        tab1 = tab[i].split("@")
        odp = check_id(tab1[0])
        if odp == True:
            odp2 = check_one_X(tab1[1])#sprawdza czy jeden x na karcie
            if odp2 == True:
                odp3 = check_name_vote(tab1[1])
                if odp3 == True:
                    print("dobra karta")
                else:
                    return False
            else:
                return False
        else:
            return False
    return True

def generate_key():
    czas = str(time.time())
    hash_time =  hashlib.sha224(czas).hexdigest()+str(random.random())
    nonce = ""
    for i in range(0,len(hash_time)):
        if i%3== 0:
            nonce+=hash_time[i]
    if len(nonce) == 23:
        nonce += "0"
    return nonce

def encript_data(mess, key):
    obj = AES.new(str(key), AES.MODE_CBC, 'This is an IV456')
    while len(mess)%16 != 0:
        mess += '0'
    ciphertext = obj.encrypt(mess)
    return ciphertext

def co_5_wyraz_hasza(mess):
    nonce = ""
    for i in range(0,len(mess)):
        if i%5== 0:
            nonce+=mess[i]
    return nonce

def podpisz_karte(karta):
    hash_time =  hashlib.sha224(karta).hexdigest()
    id = take_id(karta)
    nonce = co_5_wyraz_hasza(hash_time)
    klucz = generuj_haslo(id)
    lala = encript_data(nonce,klucz)
    karta += str(lala)
    return karta


def generuj_haslo(id):
    myFile = open('hasla.dat', 'a')
    newhaslo = generate_key()
    myFile.write(id+"#"+newhaslo)
    myFile.close()
    return newhaslo

def podpisz_to(karty):
    podpisane_karty = ""
    kart = karty.split("$")
    id = take_id(karty)
    for i in range (0,len(kart)-1):
        podpisane_karty += str(podpisz_karte(kart[i]))+"$"
    myFile = open('hasla.dat', 'a')
    myFile.write("#\n")
    myFile.close()
    return podpisane_karty

def check_end_kart(karta, nr):
    kart =  karta.split("@")
    id = take_id(kart[0])
    numer = int(nr)
    myFile = open('hasla.dat', 'r')
    for line in myFile:
        tab = line.split("#")
        if id == tab[0]:
            odkoduj = tab[numer]
            myFile.close()
            return True
        else:
            return False

def daj_karte_do_urny(karta):
    kart =  karta.split("@")
    id = take_id(kart[0])
    moja_karta = id+"#"
    kartka = kart[1].split("#")
    for i in range(0,len(kartka)-1):
        moja_karta += kartka[i]+"#"
    print(moja_karta)
    return moja_karta

def wrzuc_do_urny(kartka):
    kart = kartka.split("#")
    id = kart[0]
    k=0
    myFile3 = open('uprawnieni.dat').readlines()
    myFile2 = open('uprawnieni.dat', 'w')
    for s in myFile3:
        id2 = s.split("#")
        if id2[0] == id:
            if str(id2[1]) == "True":
                k += 1
                myFile2.write(s.replace(id+"#True#", id+"#True#"))
            else:
	            myFile2.write(s.replace(id+"#", id+"#True#"))
        else:
            myFile2.write(s.replace(id+"#", id+"#True#"))
    myFile2.close()
    if k == 0:
        myFile = open('urna.dat', 'a')
        myFile.write(kartka+"\n")
        myFile.close()
        myFile4 = open('hasla.dat', 'w')
        myFile4.write("\n")
        myFile4.close()
        print("Dodane Karte")
    else:
        return False

def odkoduj_to(karta, klucz):
    kart = karta.split("#")
    print(kart[6])
    print(klucz)
    a = decrypt_data_AES(kart[6], klucz)
    print a

def obsluga(klient):
    '''
    :param klient:
    :return:
    '''
    klient.sock.send(to_string(tablica_przedmiotow))
    lala = klient.sock.recv(240)
    klient.sock.send(str(0))
    klient.sock.send(get_public_key())
    en_key = klient.sock.recv(240)
    en_key2 = decrypt_data(en_key)
    kart = decrypt_data_AES(lala, en_key2)
    check = check_cart(kart)
    if check == True:
        klient.sock.send("poprawne karty")
        karty = podpisz_to(kart)
        karty_wyslij = encript_data(karty,en_key2)
        klient.sock.send(karty_wyslij)
        karta_odebrana = klient.sock.recv(512)
        numer_kod = klient.sock.recv(120)
        odkodowana_karta = decrypt_data(karta_odebrana)
        # print odkodowana_karta
        odkodowanie_AES = check_end_kart(odkodowana_karta, numer_kod)
        # print(odkodowanie_AES)
        # odkoduj_to(odkodowana_karta,odkodowanie_AES)
        do_urny = daj_karte_do_urny(odkodowana_karta)
        x = wrzuc_do_urny(do_urny)
        if str(x) == "False":
            klient.sock.send("Nie oszukuj misiu!")
        else:
            klient.sock.send("Udalo sie zaglosowac poprawnie")
    else:
        klient.sock.send("Oszustwo nie poplaca :(")



class clientObject(object):
    def __init__(self, clientInfo):
        self.sock = clientInfo[0]
        self.address = clientInfo[1]
        self.split_tab = []
        self.klucz_sesji = ""
    def update(self, message):
        self.sock.send(message)

class Server(object):
    def __init__(self):
        """


        :type self: object
        :rtype : object
        """
        self.Name = "PKW"
        self.HOST = 'localhost'
        self.PORT = 40002
        self.ADDRESS = (self.HOST,self.PORT)
        self.running = True
        self.serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#rodzina ipv4
        self.serverSock.bind(self.ADDRESS)#bind take 1 argument
        self.serverSock.listen(10)

        while self.running:
            clientInfo = self.serverSock.accept()
            print("Client connected from {}.".format(clientInfo[1]))
            thread.start_new_thread(obsluga,(clientObject(clientInfo),))

        self.serverSock.close()
        print("- end -")

ser = Server()

