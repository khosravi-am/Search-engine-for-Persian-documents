from term import Term
from math import sqrt
from docTerm import DocTerm

class Index:

    def __init__(self) -> None:
        self.__term_id = 0
        self.__index = dict()
        self.__lenth = dict()
        self.__score = dict()
        pass

    def get_index(self):
        return self.__index
    
    def insert_index(self,word: str,doc_id,position,url):
        self.__lenth[doc_id]=0
        self.__score[doc_id]= 0
        if word not in self.__index.keys(): 
            self.__index[word]= Term(self.__term_id,doc_id,position,url)
            self.__term_id +=1
        else:
            self.__index[word].insert_posting(doc_id,position,url)


    def calculate_tfIDF(self,nDocs):
        for term in self.__index.values():
            term.calculate_tfIDF(nDocs,self.__lenth)
        for docID in self.__lenth.keys():
            self.__lenth[docID]= sqrt(self.__lenth[docID])

    def create_champion_list(self):
        for term in self.__index.values():
            term.set_champion()
    
    def get_respons(self,query_tokens):
        self.__score = dict.fromkeys(self.__score, 0)
        for term in query_tokens:
            if term in self.__index.keys():
                self.__index[term].calculate_score(self.__lenth,self.__score)
        return self.__score


    def print_index(self):
    # to print all index set k = len(self.__index) and m = 0
        i=0
        k = 3
        m = 100
        l = len(self.__index) -m
        for j,i in ( self.__index.items()):
            if i<k or i>=l :
                if i<k:
                    print(i,' maximum:\n')
                    
                    print(j,end ="\n"),
                    i.printpost()
                else:
                    print()
                    print(m,' minimum:\n')
                    print(j,end =" "),
                    i.printpost()
                    m -=1
            i+=1


    def sort_index(self):
        a = sorted(self.__index.items(),key=lambda x:x[1].docRepet,reverse=True)
        self.__index= dict(a)

    def set_url(self,url,id):
        list(self.__index.values())[-1].set_url(url,id)
    

    def get_url(self,id):
        return list(self.__index.values())[-1].get_url(id)
        
