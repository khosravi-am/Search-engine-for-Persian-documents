from math import log10 as log

class DocTerm:

    __document_id: int
    __document_url: str
    __tf_idf: int

    def __init__(self,doc_id,position,url) -> None:
        self.__document_id=doc_id
        self.__term_repet=1
        self.position=[]
        self.__tf_idf = 0
        self.__document_url=url
        self.position.append(position)


    def set_tfIdf(self,docRepet,nDocs):
        self.__tf_idf= (1 + log(self.__term_repet)) * log(nDocs/docRepet)
        return self.__tf_idf

    def get_tfIdf(self):
        return self.__tf_idf


    def insert_position(self,position):
        self.__term_repet+=1
        self.position.append(position)

    def printDoc(self):
        print("document ",self.__document_id," , term repet ",self.__term_repet,'positoin: ',
              self.position,' doc url:\n',self.get_url(),'\ntfidf: ',self.get_tfIdf(),
            )

    def set_url(self,url):
        self.__document_url=url

    def get_url(self):
        return self.__document_url