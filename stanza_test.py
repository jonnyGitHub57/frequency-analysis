#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://medium.com/analytics-vidhya/how-to-easily-extract-text-from-any-pdf-
with-python-fc6efd1dedbe

https://stanfordnlp.github.io/stanza/data_objects.html

https://universaldependencies.org/u/pos/

Created on Fri Jan 21 04:47:28 2022

@author: jonny
"""

import sys # Needed by stanza to download files
import os
import pdfplumber
import easygui
import re
import stanza
import time
from datetime import datetime
import xml.etree.ElementTree as ET


"""
Experiments with the stanza 'doc' format and methods

https://mmsankosho.com/en/nlp-for-learners-parsing-with-stanza/

"""

class XML_statistics(object):
    """
    """
    def __init__(self, language='Nederlands', Debug=False):
        """
        """
        self.language = language
        self.debug = Debug
        # self.data_file = './Wictionary_{}.xml'.format(self.language)
        self.data_file = './' + self.language + '/Frequency_dict.xml'
        self.log_file = './' + self.language + '/stanza_logfile.txt'
        self.language_code = {'Nederlands': 'nl', 'Romanian': 'ro'} \
                                                        .get(language, 'ro')
        # self.tree = ET.parse('nl_dictionary.xml')
        self.tree = ET.parse(self.data_file)
        self.root = self.tree.getroot()
        """
        Create a translation table from the xml-file information. There must be 
        at least one but only one of them will be used anyway.
        """
        transl_table = self.root.findall('./transl_table')
        intab  = transl_table[0].find('intab').text
        outtab = transl_table[0].find('outtab').text
        self.transtab = str.maketrans(intab, outtab)
        print(f'Translation table ({self.language_code}): {self.transtab}')
    
        
        
    def size_ofDictionary(self):
        """
        Count all words in the tree
        """
        return(len(self.root.findall('./word')))
    
    def number_entries(self):
        elements = self.root.findall('./word')
        counter = 0
        for word in elements:
            counter += int(word.find('counter').text)
        
        return(counter)
        
    def xml_tree2file(self):
        """
        Write the tree to the correct XML-file 
        """
        self.tree.write(self.data_file, encoding="UTF-8", 
                                                xml_declaration=True)
        
    def addElement(self, element, header='word'):
        """
        Add an element to the xml tree in a "pretty print" format so that 
        the element is written to the xml file using the method from 
        "https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-
                                    elementtree-to-pretty-print-to-an-xml-file"
        Parameters:
            element: a dictionaries e.g. {'lemma': 'fiets, 'tag':'NOUN'
                                                  , 'swedish': 'cykel', ...}
        """
        addElement = ET.Element(header)             # Make a new 'word' element
        addElement.tail = "\n"                      # Edit the element's tail
        addElement.text = "\n\t\t"                  # Edit the element's text
        count = len(element)
        for key in element:
            element[key] = str(element[key])    # Must be string(s)
            newData = ET.SubElement(addElement, key)
            count -= 1
            if count == 0:
                newData.tail = "\n\t"       
            else:
                newData.tail = "\n\t\t"
            newData.text = element[key]
        self.root[-1].tail = "\n\t" # Edit the previous element's tail, so that our new 
        self.root.append(addElement) # element is properly aligned/formatted
        
    def elements2dictionary(self, elements):
        """
        elements is a list of elements in the xml tree. Each element is 
        extracted into a dictionary that is returned to the caller
        Parameter: elements = [element1, element2, ...]
        Return: element_list = [dictionary1, dictionary2, ...]
        """
        dict_list = []
        
        for element in elements:
            element_to_dict = {}
            for child in element:
                child_text = child.text
                if child_text == None:
                    child_text = ''
                if self.debug == True:
                    print(child.tag + ': ' + child_text)
                element_to_dict[child.tag] = child_text
            dict_list.append(element_to_dict)
        
        return(dict_list)
    
    def find_in_tree(self, lemma, upos, item='word'):
        """
        'find_in_statistics' will traverse all <stat_word> elements in the 
        tree to findall perfect matches to the word. It searches for the word 
        among the foreign language lemmas.
        Returns a list of statistic word elements
        """
        elements = self.root.findall('./{}'.format(item))
        # print('Searched words: ', len(elements))
        found_elements = []
        for child in elements:
            if lemma == child.find('lemma').text and \
                        upos == child.find('upos').text:
                found_elements.append(child)
                if self.debug == True:
                    print(child.find('lemma').text)
        
        return(found_elements)
    
    
    def find_file_in_tree(self, file_name='*'):
        elements = self.root.findall('./source_file')
        if file_name == '*':
            found_elements = elements
        else:
            found_elements = []
            for child in elements:
                used_file = child.find('filename').text
                if used_file.find(file_name) != -1:
                # if file_name == child.find('filename').text:
                    found_elements.append(child)
        
        return(found_elements)
        
    
    def get_sorted_data(self):
        """
        get_sorted_data returns the elements in the xml-tree sorted in falling 
        order i.e. with the most frequent words in the beginning of the list.
        
        Returns: 
        -------
        elements: a sorted list of elements

        """
        elements = self.root.findall('word')
       
        def get_counter(word):
            return(int(word.find('counter').text))

        elements.sort(reverse=True, key=get_counter)
        
        return(elements)
    
    def get_sorted_alphabetically(self, Nr_of_words=100):
        """
        

        Returns
        -------
        None.

        """
        elements = self.get_sorted_data()
        
        print('Antal element : ', len(elements))
        
        # useful_upos = ['NOUN', 'ADJ', 'VERB', 'CCONJ', 'ADV', 'ADP']
        filter_upos = ['PUNCT', 'X', 'PROPN', 'SYM']
       
        def get_lemma(word):
            return(word.find('lemma').text)

        useful_elements = []
        for element in elements:
            if element.find('upos').text in filter_upos:
                pass
            else:
                useful_elements.append(element)
                
        print('Antal fitrerade element: ', len(useful_elements))
        print('Antal beställda ord: ', Nr_of_words)
        
        elements = useful_elements[0 : Nr_of_words]
        elements.sort(reverse=False, key=get_lemma)
        
        return(elements)
    
   
if __name__=='__main__':
    """
    Beginning of main code for 
    """
    Language_list = []
    romanian = XML_statistics(language='Romanian', Debug=False)
    Language_list.append(romanian)
    
    current_language = Language_list[0] # Default language
    for supported in Language_list:
        size = supported.size_ofDictionary()
        print(f'{supported.language} är inlagt med {repr(size)} st entries')
    
    # print('Size of dictionary: ', romanian.size_ofDictionary())
    
    sample_file = './Sample_files_ro/RUMK01JanssonEk.pdf'
    Debug_print = True
    Debug_mode = True
    
    """
    initialize Dutch neural pipeline
    """
    stanza.download(romanian.language) # download Romanian model
    nlp = stanza.Pipeline(romanian.language, logging_level='INFO')
    # nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
    
    def Analyze_file(this_language):
        """
        

        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        def tag_text_file(file_to_tag, category):
            """
            Run page-by-page through the Stanza pipeline for text analysis
            The stanza 'doc format' is converted to a N-size list  
            of dictionaries where N = number of sentences in the text, 

            Parameters
            ----------
            file_to_tag : TYPE
                DESCRIPTION.

            Returns
            -------
            None.

            """
            print('Run POS tagging on file: ', file_to_tag)
            
            with open(file_to_tag, 'r') as text_file:
                for line in text_file:
                    print('.', end='')
                    sys.stdout.flush()
                    doc = nlp(line)
                    doc_dict = doc.to_dict()
                    
                    sent_index = 0
                    nr_entries = 0
                    for sent in doc.sentences:
                        word_index = 0
                        for word in sent.words:
                            upos = word.upos
                            lemma = word.lemma
                            """
                            Use the translation table to replace special
                            characters such as T-cedilla to T-comma etc.
                            """
                            new_lemma = lemma.translate(this_language.transtab)
                            element = this_language.find_in_tree(new_lemma, upos)
                            if element == []:
                                dict_to_add = doc_dict[sent_index][word_index]
                                dict_to_add['lemma'] = new_lemma
                                dict_to_add['counter'] = '1'
                                dict_to_add['category'] = '1'
                                dict_to_add['index'] = str(datetime.now())
                                this_language.addElement(dict_to_add)
                            else:
                                """
                                Assume that the list of found words only holds
                                one hit. Update the counter for the word in the
                                xml-file
                                """
                                for child in element[0]:
                                    if child.tag == 'counter':
                                        child.text = str(int(child.text) + 1)
                            
                            word_index += 1
                        nr_entries += word_index
                        sent_index +=1  
                print('\r\nFinished\r\n')
                        
        """
        Ask the user for a file to analyze
        """
        file_in_use = False
        
        source_file = easygui.fileopenbox()
        """
        Strip away the path and search the xml-file for previous use of
        the selected file (name).
        """
        file_name, file_ext = os.path.splitext(source_file)
        full_path, file_name = os.path.split(source_file)
        head, category = os.path.split(full_path)
        print(f'File {file_name} has the extension {file_ext}')
        
        if file_ext.lower() == '.txt' or file_ext.lower() == '.pdf':
            found_files = this_language.find_file_in_tree(file_name)
            if found_files == []:
                file_in_use = False
            else:
                file_in_use = (input('File in use. Use anyway Y/n: ') != 'Y')
            
            if file_in_use:
                pass
            else:
                """
                Add the file name to the list of used files in the XML-file
                and analyze the file. Pdf-files get the text body extracted
                before running POS-tagging
                """
                
                source_file_dict = {'filename': source_file}                
                start_time = time.time()
                entries_before = romanian.number_entries()
                
                if file_ext == '.txt':
                    print(f'Adding {file_name} to the xml-file')
                    this_language.addElement(source_file_dict, header='source_file')
                    tag_text_file(source_file, category)
                else:
                    print('Analyzing pdf-file: ', file_name)            
                    pdf_file = pdfplumber.open(source_file)
                    totalpages = len(pdf_file.pages)
                    print("Antal sidor i dokumentet", totalpages)
                    print('Skip ill formatted pages in the document?')
                    skip_pages = input('Enter comma separated list or <CR>: ')
                    if skip_pages != '':
                        skip_list = re.split(r"[,.?!]", skip_pages)
                        print('skippa sidorna: {}'.format(', '.join(skip_list)))
                        remove_pages = [(eval(i) -1) for i in skip_list]
                    else: 
                        remove_pages = []
                    """
                    Create file information to add to the xml-file
                    """
                    source_file_dict['No_pdf_pages'] = str(totalpages)
                    print(f'Adding {file_name} to the xml-file')
                    this_language.addElement(source_file_dict, header='source_file')
                    # Remove characters that do not belong to words
                    remove_chars = ':,;[]0123456789'
        
                    with open('datafile.txt', 'w') as text_file:
                        for i in range(0 ,totalpages):
                            if i in remove_pages:
                                continue
                            pageobj = pdf_file.pages[i]
                            page_text = pageobj.extract_text()
                            """
                            Page-by-page: Replace or delete unwanted characters and 
                            numericals and update the text file as a logging function
                            """
                            page_text = page_text.replace('(cid:239)', 'i')
                            page_text = page_text.replace('(cid:21)', 'i')
                            page_text = page_text.translate({ord(i): None for i in 
                                                                     remove_chars})
                            # page_text = page_text.replace({ord(i): None for i in remove_chars})            
                            text_file.write(f'Page number: {i + 1} **************\r\n')
                            text_file.write(page_text)
                            print(f'Page nr: {i + 1}\r\n')
                    text_file.close()
                    pdf_file.close()
                    tag_text_file('datafile.txt', category)
                    
                """
                Summarize the analysis and print the N most frequent entries
                Add info the log file
                """
                end_time = time.time()
                entries_after = romanian.number_entries()
                entries_added = entries_after - entries_before
                elapsed_time = round(end_time - start_time)
                Nr_entries = 20
                print('Antal entries: {}'.format(entries_after))
                print('The {} most frequent entries:'.format(Nr_entries))
                elements = romanian.get_sorted_data()
                for i in range (0, Nr_entries):
                    word = elements[i]
                    counter = int(word.find('counter').text)
                    name = word.find('lemma').text
                    print('{}: {}'.format(name, counter))
                print(f'The analysis took: {elapsed_time} seconds')
                print(f'Number of added entries: {entries_added}')
                print(f'Updating XML data file {this_language.data_file}')
                this_language.xml_tree2file()
                
                with open(this_language.log_file, 'a') as my_logfile:
                    my_logfile.write('\r\n*******************************\r\n')
                    my_logfile.write(f'File: {source_file}\r\n')
                    my_logfile.write(f'Number of added entries: {entries_added}\r\n')
                    my_logfile.write(f'Elapsed time: {elapsed_time} seconds\r\n')
                    
        else:
            print('The file format is not supported')
            
        return(this_language)

    
    def Analyze_sentence(this_language):
        """
        Analyses a single sentence using stanza NLP        

        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        this_language

        """
        sentence_to_analyze = input('Input sentence: ')
        
        doc = nlp(sentence_to_analyze)
        print(doc)
        
        return(this_language)
            
    def Change_language(this_language):
        """
        Select a new language from the list of supported languages
        """
        print ('Aktuellt språk är ' + this_language.language)
        print('Välj språk:')
        for index in range (0, len(Language_list)):
            print('[' + str(index + 1) + '] ' + Language_list[index].language)
        correct_input = False
        while correct_input == False:
            try:
                new_language = int(input(f'Välj 1- {len(Language_list)}:'))
                this_language = Language_list[new_language - 1]
                correct_input = True
                break
            except ValueError:
                print('Ogiltigt val!')
            except IndexError:
                print('Finns inte i listan! Försök igen')
        print ('Valt språk är ' + this_language.language)
        return(this_language)
    
    def List_files(this_language):
        """
        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        list_of_files = this_language.find_file_in_tree(file_name='*')
        for item in list_of_files:
            print(item.find('filename').text)
        
        return(this_language)
        
    def Print_alphabetically(this_language):
        """
        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        print('List all words alphabetically')
        sorted_elements = this_language.get_sorted_alphabetically()
        
        for word in sorted_elements:
            print(word.find('lemma').text)
        return(this_language)
    
    def LaTeX_generator(this_language):
        """
        

        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        sorted_elements = this_language.get_sorted_alphabetically(Nr_of_words=110)
        
        Lines_per_page = 49
        File_path = '/home/jonny/Documents/Studier/Lingvistik/Rumänska'
        Alpha_index = File_path + '/Bok_Frequency/' + 'alpha_index.tex'
        print('Creating LaTeX file: ', Alpha_index)
        with open(Alpha_index, 'w') as latex_output:
            latex_output.write('% !TeX spellcheck = en_US\r\n')
            latex_output.write('\t' + r'%\newpage')
            latex_output.write('\r\n\t' +
                    r'% This is an script generated file from stanza_test.py')
            latex_output.write('´r\n\t' + r'\section{Alphabetical index}')
            latex_output.write(
                        '\r\n\t' + r'% Table data from Frequency_dict.xml')
            latex_output.write('\r\n\t' + r'\begin{tabular}{|p{7cm}|p{7cm}}')
            latex_output.write('\r\n\t\t' + r'\hline')
            latex_output.write('\r\n\t\t' + 
                                   r'\multicolumn{2}{|c|}{Bla bla}\\   \hline')
            # latex_output.write('\r\n\t\t' + r'\hline')
            latex_output.write('\r\n\t\t' + r'Header1 & Header2\\')
            latex_output.write('\r\n\t\t' + r'\cline{1-2}')
            latex_output.write('\r\n\t\t' + r'% Dictionary data in two columns')
            for i in range (0, Lines_per_page):
                col1 = sorted_elements[i].find('lemma').text
                col2 = sorted_elements[i + Lines_per_page +1].find('lemma').text
                latex_output.write('\r\n\t\t' + str(col1) + '& ' + str(col2) + r'\\')
                print('{}&{}'.format(col1, col2))
            
        return(this_language)
    
    def Do_nothing(this_language):
        print("Felaktigt val")
        return(this_language)
    
    """
    The option dictionary holds all meny items and their associated
    funtions to call. The pointer to the functions are retrieved 
    with options.get(...) function call
    """
    options = {"a": ['Analyse pdf- or text file', Analyze_file],
               "s": ['Analyze single sentence', Analyze_sentence],
               "f": ['List files', List_files],
               "c": ['Change language', Change_language],
               "p": ['Print alpha', Print_alphabetically],
               "l": ['LaTeX report', LaTeX_generator],
               "q": ['Quit', Do_nothing]}
    
    while True:
        """
        Use dictionary lookup to select next thing to do or "quit"
        Present a menu of items
        """
        print('\r\nAktuellt språk är: ', current_language.language)
        print('Antal ord i ordlistan är: {}'.format(
                            current_language.size_ofDictionary()))
        print('Corpus size: {}'.format(current_language.number_entries()))
        print('Huvudmeny - här väljer man mellan...')
        for key in options:
            print(key + ': ' + options[key][0])
            
        Next_option=input('Val: ')
        
        if Next_option == "q":
            """
            Flush the xml tree to the xml dictionary file
            """
            for language in Language_list:
                print("Writing data to: ", language.data_file)
                language.xml_tree2file()
            break
        try:
            # options.get(Next_option, Do_nothing)[1](current_language)
            current_language = options.get(Next_option, Do_nothing)[1] \
                                                            (current_language)
        except:
            print('Incorrect selection')        

    