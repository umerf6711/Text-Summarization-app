# -*- coding: utf-8 -*-

import streamlit as st

from spacy import displacy

import collections.abc
collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

#NLP gensim
from gensim.summarization import summarize

#Sumy packages 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

#NLTK Packages 
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize

#Web Scrapping Packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

#Function for Web Scraping 
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


#Fuctionforsumy
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result


#Function for NLTK 
def nltk_summarizer(docx):
    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(docx) 
    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1
       
    sentences = sent_tokenize(docx) 
    sentenceValue = dict() 
   
    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 
                    
    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 
        
    average = int(sumValues / len(sentenceValue)) 
    
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.5 * average)): 
            summary += " " + sentence 
    return summary 
    


def main():
    
    st.title("Text Summarizer App")
    
    activities = ["Summarize Via Text", "Summazrize via URL"]
    choice = st.sidebar.selectbox("Select Activity", activities)
    
    if choice == 'Summarize Via Text':
        st.subheader("Summary using NLP")
        raw_text = st.text_area("Enter Text Here","Type here")
        summary_choice = st.selectbox("Summary Choice" , ["Gensim","Sumy Lex rank","NLTK"])
        if st.button("Summarize Via Text"):
            if summary_choice == 'Gensim':
                summary_result = summarize(raw_text)
                
            elif summary_choice == 'Sumy Lex rank':
                summary_result = sumy_summarizer(raw_text)
                
            elif summary_choice == 'NLTK':
                summary_result = nltk_summarizer(raw_text)
                
            
            st.write(summary_result)
            
            
    if choice == 'Summazrize via URL':
        st.subheader("Summarize Your URL")
        raw_url = st.text_input("Enter URL","Type Here")
        if st.button("Summarize"):
            result = get_text(raw_url)
            #st.write(result)
            st.subheader("Summarized Text")
            docx = sumy_summarizer(result)
            
            
            
            html = docx.replace("\n\n" , "\n")
            st.markdown(html,unsafe_allow_html=True)
            
            
            
           # if raw_url != "Type Here":
            #    result = get_text(raw_url)
             #   st.write(result)
              #  summary_docx = sumy_summarizer(result)
               # html = displacy.render(summary_docx,style='ent')
                #html = html.replace("\n\n" , "\n")
                #st.markdown(html,unsafe_allow_html=True)
                
                
        
    
    
    
    
    
if __name__ == '__main__':
    main()