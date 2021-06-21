from elgamal.elgamal import Elgamal, PublicKey, CipherText, PrivateKey
import socket
from time import sleep

pb, pv = Elgamal.newkeys(128)
p,g,y = PublicKey.get(pb)

host = '127.0.0.1'
port = 50124
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

s.send(str(p).encode('utf-8'))
sleep(1)
s.send(str(g).encode('utf-8'))
sleep(1)
s.send(str(y).encode('utf-8'))
sleep(1)

cf = []
aux = True
while(aux):
    msj = (s.recv(8192)).decode('utf-8')
    if msj == "ok":
        aux = False
    else:
        print(msj)
        cf.append(int(msj.strip('\n')))

cont = 0
a = 0
b = 0
file = open("hashes/hashsDecrypt", "w")
limit = len(cf)
for i in range(0, limit):
    cont += 1
    if cont == 1:
        a = cf[i]
    elif cont == 2:
        b = cf[i]
        ct = CipherText(a,b)
        dt =  Elgamal.decrypt(ct,pv)
        print(dt.decode('utf-8'))
        file.writelines(dt.decode('utf-8'))
        cont = 0
file.close()
s.close()
