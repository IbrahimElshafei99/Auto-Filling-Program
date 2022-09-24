import tkinter 
from tkinter import *
import nltk
#nltk.download() 
from nltk.tokenize import word_tokenize,sent_tokenize
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk.util import ngrams
#pip install tabulate
from tabulate import tabulate

def corpus():
    #### Get corpus has more than 200000 words
    nltk.corpus.gutenberg.fileids()
    Corpus= nltk.corpus.gutenberg.words('edgeworth-parents.txt')
    len(Corpus)
    #print(Corpus[1500:1600])
    
    #### Remove special characters
    string.punctuation = string.punctuation +'“'+'”'+'-'+'’'+'‘'+'—'+'."'+',"'+'?"'+'--"'
    string.punctuation = string.punctuation.replace('.', '')
    CorpusWordsList=[]
    for word in Corpus:
        if word not in string.punctuation:
            CorpusWordsList.append(word)
            
    len(CorpusWordsList)
    #### Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens=[]
    for word in CorpusWordsList:
        if word.lower() not in stop_words:
            filtered_tokens.append(word)
            
    len(filtered_tokens) 
    ##### Get bigrams from the corpus
    bigrams=[]
    for index in  range(len(filtered_tokens)):
        if index==len(filtered_tokens)-1:
            break
        tupleOfBigrams=(filtered_tokens[index], filtered_tokens[index+1])
        bigrams.append(tupleOfBigrams)
    
    len(bigrams)
    #print(bigrams[-4:-1])
    return bigrams

#### Update the listbox
def update(data):
    LBox.delete(0, END)
    typed=entry.get()
    if typed !='':
        for item in data:
            string1=item[0]+' '+item[1][:2]
            string2=item[0]+' '+item[1]
            if typed.lower() in string1.lower() or typed.lower() == string2.lower():
                LBox.insert(END, item)
            
#### Fill the entry box by listbox clicked
def fillout(e):
    entry.delete(0, END) #delete anything in entry box
    entry.insert(0, LBox.get(ACTIVE)) #add the item clicked from listbox to entry box

#### Check if entry box is in listbox    
def check(e):
    typed=entry.get() 
    if typed=='':
        data=Bigrams
    else:
        data=[]
        for item in Bigrams:
            string=''
            for j in item:
                string+=j+' '
            if typed.lower() in string.lower():
                data.append(item)
                
    update(data)

root= Tk()
root.title('Auto Filling')
root.minsize(500,300)

label1=Label(text='Write here...', font=14)
label1.pack(pady=15)

entry=Entry(width=28, font=20)
entry.pack()

LBox=Listbox(width=40)
LBox.pack(pady=10)

Bigrams=corpus()
len(Bigrams)
#### Pass Bigrams list to update
update(Bigrams)

#### Create binding on the listbox with click
LBox.bind('<<ListboxSelect>>', fillout)
#### Create binding on the entry box with anything typed
entry.bind('<KeyRelease>', check)


root.mainloop()

#### Create bigram an unigram dictionary to get bigram probability
def createBigramDict(bigramList):
    bigramCounts = {}
    unigramCounts = {}
    
    for biTuple in bigramList:
        if biTuple in bigramCounts:
            bigramCounts[biTuple] +=1
        else:
            bigramCounts[biTuple] =1
        
        if biTuple[0] in unigramCounts:
            unigramCounts[biTuple[0]] +=1
        else:
            unigramCounts[biTuple[0]] =1
            
        if biTuple[1] in unigramCounts:
            unigramCounts[biTuple[1]] +=1
        else:
            unigramCounts[biTuple[1]] =1
            
    return bigramCounts, unigramCounts

BigramCounts, UnigramCounts = createBigramDict(Bigrams)

#### Create probability dictionary and matrix of bigram and its probability
def bigramProb(bigramList, bigramCounts, unigramCounts):
    prob={}
    table=[]
    for biTuple in bigramList:
        word1 = biTuple[0]
        word2 = biTuple[1]
        prob[biTuple] = (bigramCounts.get(biTuple))/(unigramCounts.get(word1))
       
    for bigram in bigramList:
        row=[]
        row.append(bigram)
        row.append(bigramCounts[bigram])
        row.append(prob[bigram])
        table.append(row)
    return table
    
Table=bigramProb(Bigrams, BigramCounts, UnigramCounts)      

#### Create table and print it in file
col_names=['Bigram', 'Count', 'Probability']
#TABLE=tabulate(Table, headers=col_names, tablefmt="fancy_grid")
#print(TABLE)
with open('bigramProb.txt', 'w') as f:
    f.write(tabulate(Table, headers=col_names))
f.close

