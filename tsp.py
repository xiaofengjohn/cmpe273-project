
from  collections import defaultdict
from time import clock

class TSP:
    dArray = [[]]   
    length = 0    
    lengthOfLength = 0   
    allzero = ""   
    biggest =""  
    cityList =[]   
    store = defaultdict(float)    
    notExist = "unexist"  
    finalRoad = notExist    
    finalCityFlow = ""    
    mininal = notExist    
    
    def __init__(self, disArray):
        if (self.check(disArray)):
            self.dArray = disArray  
            self.length = len(disArray)  
            self.lengthOfLength = len((str(self.length - 1) + ""))  
            zeroLength = 0
            while zeroLength < (self.length * self.lengthOfLength):  
                self.allzero += str(0)  
                zeroLength = len(self.allzero)
            i = self.length
            while(i > 0):  
                self.biggest += self.toLengthOfLength(i - 1) 
                i -= 1

            start=clock()

            self.allFlow()  
             
            self.initstoreMap()  
            self.DP(self.length - 2)
            finish = clock()
   #         print("TSP functions running time: " + str(finish-start) + "seconds")
            
    def check(self, dArray):  
        if (len(dArray) < 3):  
            print("The number of visiting places is less than 2. Could directly count the cost!")  
            return False
        row = len(dArray)
        i = 0
        while (i < row):
            if (row != len(dArray[i])):
                print("matrix length is NOT correct!")
                return False
            i += 1
        i = 0
        while (i < row):
            if (not self.oneZero(dArray[i], i)):
                print("Error, the matrix value is NOT correct!")
                return False
            i += 1
        return True
        
    def oneZero(self, dArray, i): 
        numOfZero = 0
        
        for  d in dArray:  
            if (d == 0.0): 
                numOfZero += 1  

        if (numOfZero == 1 and (dArray[i] == 0)): 
            return True 
        else :  
            return False

    def toLengthOfLength(self, i):  
        returnString = str(i);  
        while (len(returnString) < self.lengthOfLength):  
            returnString = str(0) + returnString
        return returnString
        
    def allFlow(self):  
        while (not (self.biggest == self.allzero)): 
            self.allzero = self.addone(self.allzero) 
            if (self.oneFlow(self.allzero)):  
                self.cityList.append(self.allzero)
                
    def addone(self, string):  
        listString = []
        i = 0
        while(i < (self.length * self.lengthOfLength)):
            listString.append(string[i: i + self.lengthOfLength])
            i += self.lengthOfLength
        i = (self.length - 1)
        while(i > -1):
            last = int(listString[i])
            if (last == (self.length - 1)):  
                last = 0  
                strLast = self.toLengthOfLength(last)  
                listString[i] = strLast  
            else :
                last += 1  
                strLast = self.toLengthOfLength(last)  
                listString[i] = strLast  
                break
            i -= 1
        ret = ""  
        for s in listString:  
            ret += s
        return ret
        
    def oneFlow(self, string):  
        listString = []
        i = 0
        while(i < (self.length * self.lengthOfLength)):
            listString.append(string[i: i + self.lengthOfLength])
            i += self.lengthOfLength
          
        #If there is the same string then false  
        i = 0
        while(i < (self.length - 1)):
            j = i + 1
            while(j < self.length):
                if (listString[i * self.lengthOfLength] == listString[j * self.lengthOfLength]):
                    return False
                j += 1
            i += 1
        
        #if it is the value on the matrix diagonal, then false
        i = 0
        while(i < len(listString)):
            if(int(listString[i]) == i):
                return False
            i += 1
         
        # make sure every city has been traveled  
        map = defaultdict(int)
        i = 0
        while(i < self.length):
            map[i] = int(string[i:i+self.lengthOfLength])
            i += self.lengthOfLength
         
        allcity = 0  
        i = 0
        while(True):
            i = map[i]
            allcity += 1
            if (i == 0):
                break
          
        if (allcity < self.length):  
            return False  
            
        return True
        
    def initstoreMap(self): 
          
        # 
        i = 0
        while(i < self.length - 1):
            self.store[self.toLengthOfLength(i)] = self.dArray[self.length - 1][i]
            i += 1
        
        #
        i = 0
        while(i < self.length):
            if(i == self.length -2):
                i += 1
                continue
            j = 0
            while(j < self.length - 1):
                if(i == j):
                    j += 1
                    continue
                self.store[self.toLengthOfLength(i) + self.toLengthOfLength(j)] = self.dArray[self.length - 2][i] + self.store[self.toLengthOfLength(j)]
                j += 1
            i += 1
        
    def DP(self, temp): 
        if (len(self.cityList) == 1):  
            self.finalRoad = self.cityList[0]  
            self.thePrint(self.cityList[0]);  
            self.minimal = str(self.store[self.cityList[0]]) + "";  
            return;  
        
        i = 0
        while(i < (len(self.cityList) - 1)):
            nextOne = i + 1
            if(self.cityList[i][0:temp * self.lengthOfLength] == self.cityList[nextOne][0:temp * self.lengthOfLength]):
                iValue = 0.0
                nextValue = 0.0
                
                iValue = self.dArray[temp][int(self.cityList[i][temp:(temp + self.lengthOfLength)])] + self.store[self.cityList[i][(temp +1) * self.lengthOfLength:]]
                nextValue = self.dArray[temp][int(self.cityList[nextOne][temp:(temp + self.lengthOfLength)])] + self.store[self.cityList[nextOne][(temp +1)*self.lengthOfLength:]]
                
                self.store[self.cityList[i][temp * self.lengthOfLength:]] = iValue  
                self.store[self.cityList[nextOne][temp * self.lengthOfLength:]] = nextValue
                
                if (iValue >= nextValue):  
                    self.cityList.pop(i) 
                else:  
                    self.cityList.pop(nextOne)  
                i -= 1
            i += 1
            
        self.DP(temp - 1)
        
    def thePrint(self, string):  
        map = defaultdict(int)
        i = 0
        while(i < self.length):
            map[i] = int(string[i:i+self.lengthOfLength])
            i  += self.lengthOfLength
         
        cityFlow = self.toLengthOfLength(0)
        i = 0
        while(True):
            i = map[i]  
            cityFlow += self.toLengthOfLength(i);  
            if (i == 0):  
                break  
        
        i = 0
        while(i < self.length + 1):
            if (i < self.length):  
                self.finalCityFlow += cityFlow[i: i + self.lengthOfLength] + "->"  
            else:
                self.finalCityFlow += cityFlow[i: i + self.lengthOfLength]
            i += self.lengthOfLength
        
    def getFinalCityFlow(self):  
        if ("" == self.finalCityFlow):  
            return self.notExist;  
     
        return self.finalCityFlow  
    

if __name__ == '__main__':
#    multilist = [[0 for col in range(6)] for row in range(6)]
##    cityArray = [[0, 2, 1, 3, 4, 5, 5, 6],  
##            [1, 0, 4, 4, 2, 5, 5, 6],  
##            [5, 4, 0, 2, 2, 6, 5, 6],  
##            [5, 2, 2, 0, 3, 2, 5, 6],  
##            [4, 2, 4, 2, 0, 3, 5, 6],  
##            [4, 2, 4, 2, 3, 0, 5, 6],  
##            [4, 2, 4, 2, 4, 3, 0, 6],  
##            [4, 2, 4, 2, 8, 3, 5, 0]]
    cityArray = [[0,10,20,30,40,50],
                 [12,0,18,30,25,21],
                 [23,19,0,5,10,15],
                 [34,32,4,0,8,16],
                 [45,27,11,10,0,18],
                 [56,22,16,20,12,0]]
    ff = TSP(cityArray);
    print ("cities order is: " + ff.getFinalCityFlow())
