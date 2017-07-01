__author__ = 'guzik_000'

def na_kogo(kto):
    myFile = open('urna.dat', 'r')
    for line in myFile:
        tmp_tab = line.split('#')
        for i in range(0,len(tmp_tab)):
            if str(tmp_tab[0]) == str(kto):
                if tmp_tab[i] =="X":
                    cur = tmp_tab[i-1]
                    if cur == "WDI":
                        print("Glosowales na WDI")
                    elif cur=="ASD":
                        print("Glosowales na ASD")
                    elif cur == "TJA":
                        print("Glosowales na TJA")
                    else:
                        print("Nie mamy Twojego glosu")
    myFile.close()
kto = raw_input("Podaj swoj PIN: ")
print(na_kogo(kto))