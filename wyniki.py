__author__ = 'guzik_000'

def uprawnieni():
    myFile = open('maile.dat','r')
    cunter = 0
    for line in myFile:
        cunter+=1
    return cunter


def licz_glosy():
    '''

    :return:wyniki glosowania
    '''
    glosy_wdi = 0
    glosy_asd=0
    glosy_tja = 0

    wynik = "\n\n"

    myFile = open('urna.dat','r')
    for line in myFile:
        tmp_tab = line.split('#')
        for i in range(0,len(tmp_tab)):
            if tmp_tab[i] =="X":
                cur = tmp_tab[i-1]
                if cur == "WDI":
                    glosy_wdi+=1
                elif cur=="ASD":
                    glosy_asd+=1
                elif cur == "TJA":
                    glosy_tja+=1
        wynik+=tmp_tab[0]+" "+cur+"\n"

    myFile.close()
    wyniki = "WDI: "+str(glosy_wdi)+"\nASD: "+str(glosy_asd)+"\nTJA: "+str(glosy_tja)
    print (wyniki)
    # print (wynik)
    return glosy_tja+glosy_asd+glosy_wdi





zaglosowanych =licz_glosy()
uprawnionych = uprawnieni()

fr = float(zaglosowanych)/float(uprawnionych)
fr = round(fr,4)
fr = fr*100
# print(zaglosowanych)
# print(uprawnionych)

print("\nfrekwencja = "+str(fr)+"%")