__author__ = 'guziq_000'

import smtplib
import socket
import thread
import hashlib
import time


def create_nonce():
    '''

    :return:
    '''
    czas = str(time.time())
    hash_time =  hashlib.sha224(czas).hexdigest()
    nonce = ""
    for i in range(0,len(hash_time)):
        if i%10== 0:
            nonce+=hash_time[i]

    return nonce


def find_login_in_file(path_file,login):
    '''

    :param path_file:
    :param login:
    :return:
    '''
    tmp_split = []
    myFile = open(path_file,'r')
    for line in myFile:
        tmp_split = line.split("#")
        print(tmp_split[1])
        if login == tmp_split[0]:
            if tmp_split[1] == "True":
                myFile.close()
                return False
            else:
                myFile.close()
                return True
    myFile.close()
    return False

def send_mail(login, nonce):
    gmail_user = "guzikq@gmail.com"
    gmail_pwd = "" #tutaj należy wpisać hasło do maila, jest to moja skrzynka dlatego zostało to usunięte :)
    FROM = 'guzikq@gmail.com'
    TO = [login]
    SUBJECT = "Kod PIN do konta"
    TEXT = "Twoj kod do logowania: "+nonce

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()

def hasz_nonce(login, nonce):
    zmienna = login+nonce
    hash = hashlib.sha224(zmienna).hexdigest()
    return hash

def mail(path_file,login):
    myFile = open(path_file).readlines()
    myFile2 = open(path_file, 'w')
    for s in myFile:
	    myFile2.write(s.replace(login+"#", login+"#True#"))
    myFile2.close()

def add_nonce(path_file, nonce):
    myFile = open(path_file, "a")
    myFile.write(nonce+"#\n")
    myFile.close()


def obsluga(klient):
    '''

    :return:
    '''
    uprawniony = klient.sock.recv(120)
    flag = find_login_in_file('maile.dat', uprawniony)
    if flag == True:
        klient.sock.send("True")
        nonce = create_nonce()
        send_mail(uprawniony, nonce)
        odp = klient.sock.recv(120)
        odp2 = hasz_nonce(uprawniony,nonce)
        if odp == odp2:
            mail('maile.dat', uprawniony)
            add_nonce('uprawnieni.dat', nonce)
            klient.sock.send("OK")
        else:
            klient.sock.send("False")
    else:
        klient.sock.send("False")




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
        self.Name = "Bob_serwer"
        self.HOST = 'localhost'
        self.PORT = 30001
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