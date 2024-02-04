from docTerm import DocTerm
from math import log10 as log

class Term:
    
    
    def __init__(self,term_id,doc_id,position,url) -> None:
        self.__n_champion = 1
        self.docRepet = 1
        self.tf_term = 1
        self.__K_number = 100
        self.__term_id=str(term_id)
        self.__repetition=1
        self.__postingsList = dict()
        self.champion_lists = dict()
        self.__postingsList[str(doc_id)]= DocTerm(doc_id,position,url)


    def calculate_tfIDF(self,nDocs,lenth):
        self.tf_term = (self.tf_term + log(self.__repetition)) * log(nDocs/self.docRepet)
        for docID in self.__postingsList.keys():
            lenth[docID]= lenth[docID] + pow(self.__postingsList[docID].set_tfIdf(self.docRepet,nDocs),2)

    def calculate_score(self,lenth,score):
        for docID in self.champion_lists.keys():
            score[docID]= score[docID] + self.tf_term * self.__postingsList[docID].get_tfIdf()/lenth[docID]       

    def set_champion(self):
        for docID in self.__postingsList.keys():
            if(self.__postingsList[docID].get_tfIdf() > self.__n_champion):
                self.champion_lists[docID]= self.__postingsList[docID]
        lenth = len(self.champion_lists)
        if (self.docRepet > self.__K_number  and lenth < self.__K_number ):
            self.__n_champion = self.__n_champion * 0.8
            self.set_champion()
        else:
            return
    

    def getID(self):
        return self.__term_id
    
    def getTerm(self):
        return self.__term
    
    def get_repet(self):
        return self.__repetition
    
    def __repet(self):
        self.__repetition += 1

    def insert_posting(self,doc_id,position,url):
        self.__repet()
        if str(doc_id) in self.__postingsList.keys():
            self.__postingsList[str(doc_id)].insert_position(position)
        else:
            self.__postingsList[str(doc_id)]= DocTerm(doc_id,position,url)
            self.docRepet +=1

    def set_url(self,url,id):
        self.__postingsList[str(id)].set_url(url)
        
    def get_url(self,id):
        return self.__postingsList[str(id)].get_url()
        

    def printpost(self):
        print("repet: ",self.__repetition,",num of docs: ",self.docRepet," , postings: ")
        for i in self.__postingsList.values():
            print(i,': ')
            i.printDoc()





