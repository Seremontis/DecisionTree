import math


class DecisionTree:
    def __init__(self,src):
        self.lista=None
        self.countCol=0
        if isinstance(src, str):
            self.lista=[]
            self.countCol=self.readFileAndMaxCount(src)
        else:
            self.lista=src
            self.countCol=len(self.lista[0])
        self.countLista=len(self.lista)
        self.wystapieniaAll=self.countOccurence(self.countCol,self.lista)
        self.prawdopodobienstwa=self.countProbablity(self.countCol,self.wystapieniaAll)
        self.entropia=self.entropyResult(self.prawdopodobienstwa) #Info(T)
        self.gains=self.collectInfoFunction(self.wystapieniaAll) #GainRadio(n,T)
        
   
    """wczytywanie pliku i max liczba wierszy"""
    def readFileAndMaxCount(self,src):
        lenCol=0
        file=open(src,"r")  
        for line in file.readlines():
            row=line.rstrip().split(",")
            if(lenCol<len(row)):
                lenCol=len(row)
            self.lista.append(row)
        file.close()
        return lenCol
    
    """liczenie wystapien"""
    def countOccurence(self,countColumn,countTable,flaga=False):
        listOccur=[]    
        if(flaga):
            listOccur=self.wystapieniaAll[:]
            for i in range(len(self.wystapieniaAll)):
                listOccur[i]=listOccur[i].fromkeys(listOccur[i],0)
        else:
            for el in range(countColumn):
                listOccur.append([])
        
        for record in countTable:   
            i=0
            for element in record:
                if(len(listOccur[i])==0):
                    listOccur[i]={}
                    listOccur[i][element]=1
                elif(element in listOccur[i]):   
                    listOccur[i][element]+=1
                else:      
                    listOccur[i][element]=1
                i+=1
        return listOccur
    
    """liczenie prawdopobobienstwa dla decyzji"""
    def countProbablity(self,countColumn,countTable):
        probability=[]
        for el in range(countColumn):
            probability.append([])
            
        i=0
        for el in countTable:
            probability[i]={}
            suma=sum(countTable[i].values())
            for wynik in el:
                probability[i][wynik]=countTable[i][wynik]/suma
            i+=1
        return probability
    
    
    """Entropie"""
    """liczenie prawdopobobienstwa dla atrybutow"""
    """lub splitInfo"""
    def entropyAttribute(self,maxGroup=None):
        tab=[]
        for i in range(len(maxGroup)):       
            dicRes=0
            for el in maxGroup[i].keys():
                ulamek=maxGroup[i][el]/self.wystapieniaAll[i][el]
                log=0
                if ulamek!=0 and ulamek!=1:               
                    log=ulamek*math.log2(ulamek)
                    log2=(1-ulamek)*math.log2(1-ulamek)
                    log+=log2
                    log*=-1    
                dicRes+=(self.wystapieniaAll[i][el]/self.countLista)*log
            tab.append(dicRes)
        return tab
    
    """Zrownowazony przyrost informacji"""
    def compute(self):
        tab=[]
        for i in range(len(self.wystapieniaAll)):       
            dicRes=0
            for el in self.wystapieniaAll[i].keys():          
                ulamek=self.wystapieniaAll[i][el]/self.countLista
                log=0
                if ulamek!=0 and ulamek!=1:               
                    log=math.log2(ulamek)
                    log*=-1
                dicRes+=ulamek*log
            tab.append(dicRes)
        return tab
    
    """entropia dla klasy decyzyjnej"""
    def entropyResult(self,probability): 
        entrophy=[]
        for el in probability:
            entro=0
            for val in el.values():
                try:
                    entro+=val*math.log2(val)
                except:
                    entro+=0
            entro*=-1
            entrophy.append(entro)
        return entrophy[len(entrophy)-1]
    
    
    """zbieranie entropi dla atrybutow wartosci"""
    def collectInfoFunction(self,occur):
        maxOccurInGroup=[]
        countFilterVal=[] #liczba wystapien w danej podgrupie poszeczgolnych elementow
        for key in occur[len(occur)-1].keys():
            filtrResult=list(filter(lambda x: key in x[len(x)-1], self.lista))  
            wal=self.countOccurence(self.countCol,filtrResult,True)
            tmp=wal[:]
            countFilterVal.append(tmp) 
        for k in range(len(countFilterVal[0])):
            value=[]
            for w in range(len(countFilterVal)):           
               value.append(countFilterVal[w][k])
            maxOccurInGroup.append(self.CompareDic(value))   
        entroAttr=self.entropyAttribute(maxOccurInGroup) #Info(n, T)
        gainTab=self.growInf(entroAttr)  #Gain(n,T)
        splitInfo=self.compute()#SplitInfo(n,T)
        return self.constInformation(gainTab,splitInfo)
       
    
    """Funkcje dotyczące obliczania informacji kosztowej danych""" 
    """Szukanie max wartosci dla pojedynczych wartosci z kolumn"""    
    def CompareDic(self,lista):
        outList=lista[0]
        for row in lista:    
            for element in row.keys():
                if(outList[element]<row[element]):
                    outList[element]=row[element]
        return outList
    
    """Przyrost informacji"""
    def growInf(self,tab):
        for i in range(len(tab)-1):
            tab[i]=self.entropia-tab[i]
        return tab
        
           
    """Zrównoważony przyrost informacji"""
    def constInformation(self,gains,splitInfo):
        gainRadio=[]
        #print(gains)
        #print(splitInfo)
        for i in range(len(gains)-1):
            try:
                gainRadio.append(gains[i]/splitInfo[i])
            except ZeroDivisionError:
                gainRadio.append(0)
                
        return gainRadio
    
    



