import subprocess

bashCommand = []
bashCommand.append("hashcat -a 0 -m 0 -w 4 --force archivosDrive/Hashes/archivo_1 archivosDrive/diccionarios/diccionario_2.dict")
bashCommand.append("hashcat -a 0 -m 10 -w 4 --force archivosDrive/Hashes/archivo_2 archivosDrive/diccionarios/diccionario_2.dict")
bashCommand.append("hashcat -a 0 -m 10 -w 4 --force archivosDrive/Hashes/archivo_3 archivosDrive/diccionarios/diccionario_2.dict")
bashCommand.append("hashcat -a 0 -m 1000 -w 4 --force archivosDrive/Hashes/archivo_4 archivosDrive/diccionarios/diccionario_2.dict")
bashCommand.append("hashcat -a 0 -m 1800 -w 4 --force archivosDrive/Hashes/archivo_5 archivosDrive/diccionarios/diccionario_2.dict")

for i in range(0,len(bashCommand)):
    file = open("reportes/report"+str(i+1), "w")
    process = subprocess.Popen(bashCommand[i].split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output.decode('utf-8'))
    file.writelines(output.decode('utf-8'))
    file.close()

        




