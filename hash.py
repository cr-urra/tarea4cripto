import bcrypt as bc
from elgamal.elgamal import Elgamal, PublicKey, CipherText
import socket
from time import time, sleep

def counter(x):
    for i in range(0, len(x)):
        if x[i] == ':':
            return i+1

archivo = open("cracks/hash1id0dic2", "r")
archivo2 = open("cracks/hash2id10dic2", "r")
archivo3 = open("cracks/hash3id10dic2", "r")
archivo4 = open("cracks/hash4id1000dic2", "r")
archivo5 = open("cracks/hash5id1800dic2", "r")

port = 50124
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("127.0.0.1",port))
s.listen(1)
client, addr = s.accept()

texts = []
texts.append(archivo.readlines())
texts.append(archivo2.readlines())
texts.append(archivo3.readlines())
texts.append(archivo4.readlines())
texts.append(archivo5.readlines())
passwords = [[],[],[],[],[]]

print('Esperando llave publica...')
p = client.recv(1024)
p = int(p.decode("UTF-8"))
sleep(1)
g = client.recv(1024)
g = int(g.decode("UTF-8"))
sleep(1)
y = client.recv(1024)
y = int(y.decode("UTF-8"))
sleep(1)
pb = PublicKey(p,g,y)
file = open("hashes/bcrypts", "w")
file3 = open("hashes/ciphers", "w")
file4 = open("passwords", "w")

for i in range(0,len(texts)):
    for j in range(0, len(texts[i])):
        line = texts[i][j]
        if i == 0:
            passwords[i].append(line[33:len(line)].strip('\n'))
        elif i == 1:
            passwords[i].append(line[50:len(line)].strip('\n'))
        elif i == 2:
            passwords[i].append(line[50:len(line)].strip('\n'))
        elif i == 3:
            passwords[i].append(line[33:len(line)].strip('\n'))
        elif i == 4:
            aux = counter(line)
            passwords[i].append(line[aux:len(line)].strip('\n'))
        file4.writelines(passwords[i][len(passwords[i])-1]+"\n")

file4.close()

for i in range(0, len(passwords)):
    file2 = open("reportes/bcrypts"+str(i+1), "w")
    start_time = time()
    for j in range(0,len(passwords[i])):
        hashed = bc.hashpw(passwords[i][j].encode('utf-8'), bc.gensalt())
        file.writelines(hashed.decode('utf-8')+"\n")
        print("Hash "+str(j+1)+": ", hashed.decode('utf-8'))
    elapsed_time = time() - start_time
    file2.writelines("Elapsed time: %0.10f seconds." % elapsed_time)
    file2.close()

file.close()
bcpt = open("hashes/bcrypts", "r")
btext = bcpt.readlines()

for i in range(0,len(btext)):
    line = btext[i]
    ct = Elgamal.encrypt(line.encode('utf-8'), pb)
    cipher = CipherText.get(ct)
    file3.writelines(str(cipher[0])+"\n")
    file3.writelines(str(cipher[1])+"\n")
    print("Cifrado asimetrico "+str(i+1)+" listo")

archivo.close()
archivo2.close()
archivo3.close()
archivo4.close()
archivo5.close()
file3.close()

asymetrics = open("hashes/ciphers", "r")
text = asymetrics.readlines()
le = len(text)
for i in range(0,le):
    print(i+1, "de", le, "cifrados enviados")
    sleep(0.1)
    client.send(text[i].encode('utf-8'))
    if i+1 == le:
        sleep(0.1)
        client.send("ok".encode('utf-8'))
sleep(3)
client.close()
s.close()