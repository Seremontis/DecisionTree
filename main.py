import budowaDrzewa as compute
 

class Tree:    
    def __init__(self,path):
        tree=compute.DecisionTree(path)
        self.gain=tree.gains
        self.lista=tree.lista
            
    def test(self):
        return self.gain.index(max(self.gain))
            
    def divideTabInput(self,index):
        tab=[]
        for line in self.lista:
            if(line[index] not in tab):
                tab.append(line[index])
        devideTab=[]
        for el in tab:
             devideTab.append(list(filter(lambda x: el in x[index], self.lista)))
        return (tab,devideTab)

            
                     
class Hierarchia:
    branches=None
    value=None     
    poziom=None
    indAtrr=None
 
def konstruujDrzewo(path,lvl=0,podzial=None):
    poziom=Tree(path)
    row=Hierarchia()
    row.wartosc=podzial
    row.branches=[] 
    row.poziom=lvl
    row.indAtrr=poziom.test() 
    if(poziom.gain[row.indAtrr]>0):           
        result=poziom.divideTabInput(row.indAtrr)
        lvl+=1
        for i in range(len(result[0])):
            row.branches.append(konstruujDrzewo(result[1][i],lvl,result[0][i]))
    else:
        row.value=poziom.lista
    return row

def przesun(liczba):
    for i in range(liczba*5):
        print(" ",end="")
        
def wyswietl(dane,liczba):
    if(dane.branches != None):
        przesun(liczba)
        if(dane.wartosc and dane.branches):
            print("Poziom {0} => Wartosc {1}, index {2}".format(dane.poziom,dane.wartosc,dane.indAtrr))
        elif(dane.wartosc and len(dane.branches)==0):
            print("Poziom {0} => Wartosc {1}".format(dane.poziom,dane.wartosc))     
        else:
            print("Poziom {0} => index {1}".format(dane.poziom,dane.indAtrr))

        if(dane.value):
            for el in dane.value:                
                przesun(liczba)
                print("  ",end="")
                print(el)
        for el in dane.branches:
            wyswietl(el,liczba+1)


        
        
            
            
            
h=konstruujDrzewo(r'C:\gielda.txt')
wyswietl(h,0)