__author__ = 'Radek'

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
# key = RSA.generate(1024)
#
# privHandle = open('private_key.dat', 'wb')
# privHandle.write(key.exportKey())
# privHandle.close()
#
# pubHandle = open('public_key.dat', 'wb')
# pubHandle.write(key.publickey().exportKey())
# pubHandle.close()


mess = "dupa dupa dupa i kamieni kupa"
print(mess)
key = open('public_key.dat', "r").read()
rsakey = RSA.importKey(key)
rsakey = PKCS1_OAEP.new(rsakey)
encrypted = rsakey.encrypt(mess)


print(encrypted)
