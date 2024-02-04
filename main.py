import json
import hazm
from index import Index
import time
import pickle
import string


source_data = open('IR_data_news_12k.json')
documents = json.load(source_data)
source_data.close()
documents= dict(documents)
num_of_documents = len(documents)

BAD_WORDS = {'رسید#رس','کرده','البته','خاطرنشان','بوده','بار','چون','حتی','ضمن','ولی','چه','همچنین',
             'همین','او','روز','کار','دو','باشید#باش','باشگاه','یا','کمیسیون','همه','نیز','شورای',
             'امروز','مورد','انقلاب','حضور','ادامه','داد','عنوان','لیگ','اگر','افزود#افزا','انجام',
             'رفت#رو','اظهار','کرد#کن',"شد#شو","داشت#دار","تیم","کشور","بود#است","گفت#گو","بازی",
             "یک","داد#ده","باید","وی","مجلس","اسلامی","گرفت#گیر","مردم","توانست#توان","دولت","سال",
             "بازیکن","#هست","قرار",'و','از','به','با','بر','برای','که','در','این','هر','را','پیام',
             'پیش','پس','است','داشت','هم','دیگر','شده','گزارش','خبرنگار','ورزشی','فارس','خبرگزاری',
             'اما','انتهای','آنها','آن','من','ما','تو','کند','تا','اینکه','خود','انت',
            }

punctuations = r')(}{:؟!،؛»«.٪٬*'
punctuations = '[' + punctuations + string.punctuation + ']'
PATERN = (punctuations,"")

lemmitizer = hazm.Lemmatizer()
normalizer = hazm.Normalizer()
sentence_tokenizer = hazm.SentenceTokenizer()
tokenizer = hazm.WordTokenizer()
index = Index() 


normalizer.diacritics_patterns.append(PATERN)
tokens =[]
emailstack = []




def lemmatize_insert_dict():

    for i in range(len(tokens)):
        if (len(tokens[i])>0):
            doc_id = tokens[i].pop(0)
            doc_url = tokens[i].pop(0)
            position=0
            for word in tokens[i]:
                word=lemmitizer.lemmatize(word)
                if(word not in BAD_WORDS ):
                    index.insert_index(word,doc_id,position,doc_url)
                position +=1
            
        else :              # for multi thread
            i = i - 1


def replace_emails_link_id(document: str):
    
    tokens = document.split(' ')
    for i in range(len(tokens)):
        word = tokens[i]
        if (tokenizer.email_pattern.match(word) or tokenizer.link_pattern.match(word) or tokenizer.id_pattern.match(word)):
            emailstack.append(word)
            tokens[i] = 'EMAILIDLINK'

    document = " ".join(tokens)
    return document


def re_emails_link_id(tokens:[]):
    for i in range(len(tokens)):
        if 'EMAILIDLINK' in tokens[i]:
            tokens[i] = emailstack.pop(0)
    return tokens

def check_email_link_id(document):
    if (tokenizer.email_pattern.search(document) or tokenizer.link_pattern.search(document) or tokenizer.id_pattern.search(document)):
        return True
    else:
        return False

def normalize():
    for doc_id in documents.keys():
        # if int(doc_id) == 970 :
            sentences = []
            repl=0

            document = documents[doc_id]['content']
            if check_email_link_id(document):
                document = replace_emails_link_id(document)
                repl +=1            
            document = normalizer.normalize(document)
            sentences.extend(sentence_tokenizer.tokenize(document))
            
            tokens.append([doc_id,documents[str(doc_id)]['url']])

            for sentence in sentences:
                tokens[-1].extend(tokenizer.tokenize(sentence))

            if repl :
                tokens[-1] = re_emails_link_id(tokens[-1])

       
        # else:
        #     break
        # elif(int(doc_id) > 970):
        #         break

def tokenize_query(query: str):
    repl = 0
    if check_email_link_id(query):
        query = replace_emails_link_id(query)
        repl+=1
    
    query = normalizer.normalize(query)
    query_tokens = tokenizer.tokenize(query)
    
    if repl:
        query_tokens = re_emails_link_id(query_tokens)
    
    i =0
    while (i < len(query_tokens)):
        if query_tokens[i] in BAD_WORDS:
            query_tokens.pop(i)
        i +=1

    return query_tokens
    

def print_respons(score: dict(),query_tokens:[]):
    i=0
    for docID in score.keys():
        if i<20:
            print('docID: ',docID,'title: ',documents[docID]['title'])
            document = normalizer.normalize(documents[docID]['content'])
            document = document.split(' ')
            for query_token in query_tokens:
                if query_token in index.get_index().keys() and docID in index.get_index()[query_token].champion_lists.keys():
                    doc = index.get_index()[query_token].champion_lists[docID]
            
            # print a part of the document that contains the word query 
                    j = doc.position[0] - 10
                    k = j*1.5
                    d = 0
                    while (j < int(k) and j < len(document)):
                        if (query_token == document[j]):
                            d =1 
                        print(document[j],end=' ')   
                        j +=1
                        if j == int (k) and d ==0:
                            k = k + 7
                    break
            

            print('\ndocument url:  ',documents[docID]['url'])
            print('\n')
        i+=1

def get_query(index: Index,query):
    timer=int(time.time_ns())

    query_tokens = tokenize_query(query)
    score = dict(index.get_respons(query_tokens))
    score = dict(sorted(score.items(),key=lambda x:x[1],reverse=True))

    print_respons(score,query_tokens)

    print('response time: ',(time.time_ns()-timer)/pow(10,9))


def save():
    dest_file = 'index.pkl'

    with open(dest_file, 'wb') as file:
        pickle.dump(index, file)
        print(f'Object successfully saved to "{dest_file}"')
    file.close()


def load():
    src_file = 'index.pkl'
    
    file = open(src_file, 'rb')
    with open(src_file, "rb") as file:
        index = pickle.load(file)
    
    file.close()
    return index

print('building index ...')
timer=int(time.time_ns())
normalize()
lemmatize_insert_dict()
index.sort_index()
index.calculate_tfIDF(num_of_documents)
index.create_champion_list()
save()
# index.print_index()

print('time of index building and save: ',int((time.time_ns()-timer)/pow(10,9)))






index = load()
# index.print_index()
while(1):
    print("\nwrite 'exit' to get out")
    query = input('enter query: ')
    if (query == 'exit'):
        exit()
    get_query(index,query)