from sklearn.ensemble import RandomForestClassifier
import numpy as np
from collections import *
import math

domainlist = []
class Domain:
    def __init__(self,_name,_label):
        self.name = _name
        self.label = _label
        self.length = len(_name)
        self.number = count(_name)
        self.entropy = entropy(_name)
    def returnData(self):
        return [self.length, self.number, self.entropy]
    def returnLabel(self):
        if self.label == "notdga":
            return 0
        else:
            return 1

def initData(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line =="":
                continue
            tokens = line.split(",")
            name = tokens[0]
            label = tokens[1]
            domainlist.append(Domain(name,label))

def count(domain):
    n = 0
    for i in domain:
        if i.isdigit() == True:
            n = n + 1
    return n 

def entropy(domain):
    Map=Counter(domain)
    entropy=0.0
    for val in Map.values():
        entropy-=val/len(domain)*math.log2(val/len(domain))
    return entropy

def main():
    print("Initialize Raw Objects")
    initData("train.txt")
    #initData("gooddomaininfo")
    featureMatrix = []
    labelList = []
    print("Initialize Matrix")
    for item in domainlist: 
        featureMatrix.append(item.returnData())
        labelList.append(item.returnLabel())
    #print(featureMatrix)
    print("Begin Training")
    clf = RandomForestClassifier(random_state=0)
    clf.fit(featureMatrix,labelList)
    print("Begin Predicting")
    with open("test.txt","r") as r:
        with open("result.txt","w") as w:
            for line in r:
                line = line.strip()
                if line.startswith("#") or line =="":
                    continue
                P=clf.predict([[len(line),count(line),entropy(line)]])
                #print(P)
                if(P==[0]):
                    w.write(line+",notdga\n")
                else:
                    w.write(line+",dga\n")
    print("End")

if __name__ == '__main__':
    main()