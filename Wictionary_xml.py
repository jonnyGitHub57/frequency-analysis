#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on Mon Jul 13 14:43:01 2020

@author: jonny
"""

#import pandas as pd
#import random
import sys
sys.path.append('../Datorlingvistik/')

# from datetime import datetime
from Translate import User_translate
from xml_test import XML_Wictionary
import webbrowser
from stanza_test import XML_statistics
import subprocess
# import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import time for the sleep method
import time
from datetime import datetime, timedelta, date
       

class Wictionary(XML_Wictionary):
    """
    The imported class XML_Wictionary gives acces to the word lists and
    methods for each language. For the frequency analysis list(s), there is
    an instanciation of the class XML_statistics
    
    """
    def __init__(self, language, Debug=False):
        self.language = language
        self.debug = Debug

        super().__init__(self.language, self.debug)
        self.translator = User_translate(self.language)        
        self.freq_analysis = XML_statistics(self.language, Debug=False)
        self.sorted_freq_data = self.freq_analysis.get_sorted_data()
        self.articles = self.find_gender_xref()
        self.verb_list_items = self.find_verb_list_items(). \
                                                get('list_items', '').split()

                                                
    def Word_lookup(self, lemma, upos):
        """
        Parameters
        ----------
        lemma : string
        upos : string                

        Returns
        -------
        formatted_word : A python dictionary with keys 'lemma', 'upos', ...
        self.elements2dictionary(elements))[0]
        """
        
        found_elements = self.find_lemma(lemma, tag=upos)
        formatted_word = {}
        if found_elements != []:
            formatted_word = (self.elements2dictionary(found_elements))[0]
        else:
            """
            The word was not found in the xml dictionary. Use Google Translate 
            to find a translation and use the known upos (tag) to add data
            """
            formatted_word['lemma'] = lemma
            formatted_word['tag'] = upos
            swedish = self.translator.translate_to_swedish(lemma)
            formatted_word['swedish'] = '*' + swedish
        return(formatted_word)
        
        

        
if __name__=='__main__':
    # Debug variables to mimit 'conditional' compile macros
    DebugMode= False
    DebugPrints= 0
    
    """
    Initialise the list of supported languages and set the default language
    to Dutch in this case
    """
    Language_list = []
    nederlands = Wictionary('Nederlands')
    romanian = Wictionary('Romanian')
    Language_list.append(nederlands)
    Language_list.append(romanian)
    
    current_language = Language_list[1] # Default language
    
    for supported in Language_list:
        size = supported.size_ofDictionary()
        print(f'{supported.language} är inlagt med {repr(size)} st entries')

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
    
    def Update_word(this_language):
        """
        

        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        word_to_search = input('Sökord: ')
        found_words = this_language.searchWord(word_to_search)
        if found_words == []:
            print('Sökordet verkar inte finns i ordlistan')
            add_word = input('Vill du lägga till ordet i ordlistan Y/n:')
            if add_word == 'Y':
                """
                Use the existing method with a user interface
                """
                Add_word(this_language, word_to_search)
        else:
            counter = 0
            for word in found_words:
                """
                Show a list of words where one can be selected for update(s)
                """
                counter += 1
                lemma = word.get('lemma')
                swedish = word.get('swedish', '')
                tag = word.get('tag', '')
                if tag == 'NOUN':
                    gender = word.get('gender', '')
                    print(f'[{counter}] {gender} {lemma}: {swedish}')
                elif tag == 'VERB':
                    print(f'[{counter}] {lemma}: (att) {swedish}')                
                else:
                    print(f'[{counter}] ({tag.lower()}) {lemma}: {swedish}')
            try:
                selection = int(input(f'Välj 1-{counter}: '))
                word_to_edit = found_words[selection -1]
                print (f'Valt ord är {word_to_edit.get("lemma")}')
                for key in word_to_edit:
                    if key != 'index' and key != 'counter':
                        current_text = word_to_edit[key]
                        get_update = input(f'{key} {current_text}: ')
                        word_to_edit[key] = get_update if get_update != '' else current_text
                
                this_language.update_element_from_dict(word_to_edit)
                print("Writing data to: ", this_language.data_file)
                this_language.xml_tree2file()
            except ValueError:
                print('Ogiltigt val!')
            except IndexError:
                print('Finns inte i listan!')
        
        return(this_language)
        
    def Edit_word(this_language):
        """
        This method MUST operate directly on the XML-tree so it will not use
        the more simple operation on a dictionary. This also means that the
        the XML file can be corrupt if handled incorrectly
        """
        #found_words = []
        word_to_search = input('Sökord: ')
        found_elements = this_language.find_word(word_to_search)
        if found_elements == []:
            print('Sökordet verkar inte finns i ordlistan')
            add_word = input('Vill du lägga till ordet i ordlistan Y/n:')
            if add_word == 'Y':
                """
                Use the existing method with a user interface
                """
                Add_word(this_language, word_to_search)
        else:
            counter = 0
            for child in found_elements:
                """
                Show a list of words where one can be selected for update(s)
                """
                counter += 1
                lemma = child.find('lemma').text
                swedish = child.find('swedish').text
                tag = child.find('tag').text
                if tag == 'NOUN':
                    gender = child.find('gender').text
                    print(f'[{counter}] {gender} {lemma}: {swedish}')
                elif tag == 'VERB':
                    print(f'[{counter}] {lemma}: (att) {swedish}')                
                else:
                    print(f'[{counter}] ({tag.lower()}) {lemma}: {swedish}')
            try:
                selection = int(input(f'Välj 1-{counter}: '))
                word_to_edit = found_elements[selection -1]
                print (f'Valt ord är {word_to_edit.find("lemma").text}')
            except ValueError:
                print('Ogiltigt val!')
            except IndexError:
                print('Finns inte i listan!')
            
            for child in word_to_edit:
                child_text = child.text if child.text != None else ''
                child_tag = child.tag
                if child_tag == 'index' or child_tag == 'counter':
                    pass
                else:
                    get_update = input(f'{child.tag} {child_text}: ')
                    child.text = get_update if get_update != '' else child_text

        
        print("Writing data to: ", this_language.data_file)
        this_language.xml_tree2file()
          
        return(this_language)
        
    def Search_word(this_language):
        """
        """
        found_words = []
        word_to_search = input('Sökord: ')
        found_words = this_language.searchWord(word_to_search)
        if found_words == []:
            print('Sökordet verkar inte finns i ordlistan')
            add_word = input('Vill du lägga till ordet i ordlistan Y/n:')
            if add_word == 'Y':
                Add_word(this_language, word_to_search)
        else:
            for word in found_words:
                lemma = word.get('lemma')
                swedish = word.get('swedish', '')
                expl = word.get('explanation', '')
                tag = word.get('tag')
                if tag == 'NOUN':
                    gender = word.get('gender', '')            
                    print(f'{gender} {lemma}: {swedish}')
                elif tag == 'VERB':
                    """
                    A verb is listed with lemma + swedish meaning 
                    and the conjugations in present form
                    """
                    print(f'{lemma}: (att) {swedish} | ', end='')
                    for item in this_language.verb_list_items:
                        print(f'{word.get(item, "")} ', end='')
                    print('')
                else:
                    """
                    All other tags have a default printing layout
                    """
                    print(f'({tag.lower()}) {lemma}: {swedish}')
          
        return(this_language)
        

    def Add_word(this_language, word_to_add=''):
        """
        User input function to add words to the dictionary based on tag.
        It will also possible to chose between tags that are suggested by Stanza.
        
        If the function is called with word_to_add == '', the user interface 
        for selecting a word will be presented, otherwise it will jump directly
        into selecting TAG.

        Parameters
        ----------
        this_language : TYPE
            Not used in this method - only for consistency.
        word_to_add : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        this_language: Not modified in this method. It is only passed through.

        """
        
        if word_to_add == '':
            print('Here is where new words are added to the dictionary.')
            print('The word is added based on its tag (ordklass)')
            input_word = input('The word to add <enter> for suggests: ')
            elements = this_language.sorted_freq_data
            filter_upos = ['PUNCT', 'X', 'PROPN', 'SYM']
            count = 1
            while input_word == '':
                i = 1
                while (i % 10) != 0 and count < len(elements):                    
                    word = elements[count]
                    upos_tag = word.find('upos').text
                    counter = int(word.find('counter').text)
                    lemma = word.find('lemma').text
                    count += 1
                    if upos_tag in filter_upos or this_language.find_lemma(lemma, upos_tag) != []:
                        pass
                    else:
                        print(f'({upos_tag.lower()}) {lemma}: {counter}')
                        i += 1
                input_word = input('The word to add or <enter> for tips: ')
        else:
            print('The word to add: {}'.format(word_to_add))
            input_word = word_to_add
        template_list = []
        template_list = this_language.find_template('*')
        
        """
        Present a list of the word classes (tags)to allow the user 
        to select the appropriate class for the new word.
        """
        i = 0
        for template in template_list:
            i +=1
            print(f'{i}: {template["tag"]} {template["explanation"]}')            
               
        print('Select tag (ordklass) 1..N or press <enter> if you')
        select = input('want the system to suggest a tag: ')        
        
        if select !='':
            input_tag = (template_list[int(select) -1])['tag']
            print('Selected tag: ', input_tag)
        else:
            input_tag = 'AUX'
        
        """
        The 'find_templates()' returns a list of templates (dictionaries) with
        more than on template when a POS tagger is used to suggest a tag. 
        Initaially, only the first template in the list will be used 
        """
        templates = this_language.find_template(input_tag)
        new_word = templates[0]
        
        for item in new_word:
            if item == 'rules':
                pass
            elif item == 'lemma':
                new_word['lemma'] = input_word
            elif item == 'tag':
                pass
            elif item == 'counter':
                new_word['counter'] = '1'
            elif item == 'index':
                new_word['index'] = str(datetime.now())
            elif item == 'definite':
                if this_language.postfix_noun == True:
                    new_word[item] = input(str(item) + ': ')
            elif item == 'swedish':
                google_suggest = this_language.translator.translate_to_swedish(input_word)
                # google_suggest = 'nisse'
                swedish = input(f'{item} ({google_suggest}): ')
                new_word[item] = google_suggest if swedish == '' else swedish
            elif item == 'gender':
                """
                Truncate femininum, maskulinum and neutrum to f, m, n
                """
                new_word[item] = (input('{}: '.format(item)))[0:1]
            else:
                new_word[item] = input(str(item) + ': ')

        for item in new_word:
            print(item + ': ' + new_word[item])
        this_language.addElement(new_word)
        
        print("Writing data to: ", this_language.data_file)
        this_language.xml_tree2file()
        
        return(this_language)
        
    def List_words(this_language):
        """
        List words from the dictionary based on tag (ordklass).
        All words can be listed using tag= 'all'
        
        """
        template_list = []
        template_list = this_language.find_template('*')
        
        """
        Present a list of the word classes to allow the user to select the
        appropriate class for the new word.
        """
        i = 0
        for template in template_list:
            i +=1
            print(f'{i}: {template["tag"]} {template["explanation"]}')            
               
        print('Select tag (ordklass) 1..N or press <enter> if you')
        select = input('want to print the whole dictionary: ')        
        
        if select !='':
            input_tag = (template_list[int(select) -1])['tag']
            print('Selected tag: ', input_tag)
        else:
            input_tag = '*'
        
        """
        The 'find_templates()' returns a list of templates (dictionaries) with
        more than on template when a POS tagger is used to suggest a tag. 
        Initaially, only the first template in the list will be used 
        """
        
        found_words = []
        found_words = this_language.find_tag(input_tag)
        print('Antal ord i list: ', len(found_words))
        
        for word in found_words:
            lemma = word.get('lemma')
            swedish = word.get('swedish', '')
            # expl = word.get('explanation', '')
            tag = word.get('tag','')
            if tag == 'NOUN':
                gender = word.get('gender', '')
                if gender == '':
                    print('{}: {}'.format(lemma, swedish))
                else:
                    print('{} {}: {}'.format(gender, lemma, swedish))
            elif tag == 'VERB':
                print('{}: (att) {} | '.format(lemma, swedish), end='')
                items_to_list = this_language.verb_list_items
                
                for item in items_to_list:
                    print('{} '.format(word.get(item, '')), end='')  
                print('')
            else:
                print('({}) {}: {}'.format(tag.lower(), lemma, swedish))
        
        return(this_language)
        
    def Word_test(this_language):
        """
        Make a test with N number of words from Swedish to the foregin
        language (Dutch or other). It is possible select a specific word class
        for the test or a mix from all classes.
        """
        template_list = []
        template_list = this_language.find_template('*')
        
        """
        Present a list of the word classes to allow the user to select the
        appropriate class for the new word.
        """
        i = 1
        for template in template_list:            
            print(f'{i}: {template["tag"]} {template["explanation"]}')   
            i +=1
               
        print('Select tag (ordklass) 1..N or press <enter> if you')
        select = input('want to use the whole dictionary: ')        
        
        if select !='':
            input_tag = (template_list[int(select) -1])['tag']
            print('Selected tag: ', input_tag)
        else:
            input_tag = '*'
            
        nr_words_to_test = int(input('Hur mångs ord vill du testa?: '))
        test_words = this_language.find_random_words(nr_words_to_test, input_tag)
        incorrect_answers = []
        """
        If the selected tag is 'VERB', the test will be more extensive with the
        different konjugations of the verb
        """
        if input_tag == 'VERB':
            test_items = ['lemma'] + this_language.verb_list_items
            print(test_items)
            for x in range(nr_words_to_test):
                print('ANtal ord kvar i testet: ', nr_words_to_test - x)
                word_in_test = test_words[x]
                lemma = word_in_test.get('lemma', '')
                swedish = word_in_test.get('swedish', '')
                explanation = word_in_test.get('explanation', '')
                synonym = word_in_test.get('synonym', '')
                if synonym != '':
                    print('{} {} (syn) {}'.format(swedish, explanation, synonym))
                else:
                    print('{} {}'.format(swedish, explanation))
                
                correct_answer = True
                for item in test_items:
                    item_to_test = word_in_test.get(item, '')
                    if item_to_test != '':
                        answer = input('{}: '.format(item))
                        if item == 'lemma' and answer =='?':
                            print('Lemma: ', item_to_test)
                        elif answer != item_to_test:
                            correct_answer = False
                        else:
                            pass
                if correct_answer == True:
                    print('Rätt svar!')
                else:
                    incorrect_answers.append(x)
                    print('Fel svar. Rätt svar: ', end='')
                    for item in test_items:
                        print('{} '.format(word_in_test.get(item, '')), end='')  
                    print('')
        else:
            """
            All other tags/word classes are tested less extensively
            than the verbs
            """
            for x in range(nr_words_to_test):
                print('Antal ord kvar i testet: ', nr_words_to_test - x)
                word_in_test = test_words[x]
                lemma = word_in_test.get('lemma', '')
                tag = word_in_test.get('tag', '')
                tag = tag.lower()
                definite = word_in_test.get('definite', '')
                swedish = word_in_test.get('swedish', '')
                explanation = word_in_test.get('explanation', '')
                synonym = word_in_test.get('synonym', '')
                if synonym != '':
                    print(f'({tag}) {swedish} {explanation} (syn) {synonym}')
                else:
                    print(f'({tag}) {swedish} {explanation}')
                answer = input('Enter word: ')
                if answer != '':
                    if word_in_test['tag'] != 'NOUN':
                        """
                        """                    
                        if answer == lemma:
                            print('Rätt svar!')
                        else:
                            print('Fel svar. Rätt svar: ', lemma)
                            incorrect_answers.append(x)
                    else:
                        """
                        Nouns in languages with postfix form i.e. a trailer in 
                        the definite form such as Romanian and the Nordic 
                        languages  can also be tested in its definite form 
                        instead fundamental of the form (the lemma)                    
                        """
                        gender = word_in_test.get('gender', '')
                        """
                        Transalte between words in the dictionary that are 
                        stored with article rather that actual gender m,n,f 
                        """
                        article = this_language.articles.get(gender, gender)
                            
                        split_answer = answer.split()
                        if len(split_answer) < 2 or gender == '':
                            """
                            STudent has answered w/o gender de/het or un/o or 
                            there is no gender stored in the dictionary
                            """
                            if split_answer[0] == lemma or split_answer[0] == definite:
                                print('Rätt svar!')
                            else:
                                print('Fel svar. Rätt svar: ', lemma)
                                incorrect_answers.append(x)                            
                        else:
                            """
                            Student has answered with gender and there is a 
                            gender for the word in the dictionary
                            """
                            if split_answer[0] == article and split_answer[1] == lemma:
                                print('Rätt svar')
                            else:
                                 print(f'Fel. Rätt svar: {article} {lemma}')
                                 incorrect_answers.append(x)
                else:
                    # Student has pressed <CR> to get help
                    incorrect_answers.append(x)
                    if word_in_test['tag'] != 'NOUN':
                        print('Fel svar. Rätt svar: ', lemma)
                    else:
                        gender = word_in_test['gender']
                        if gender == None:
                            gender = ''
                        print('Fel. Rätt svar: {} {}'.format(gender, lemma))
        """
        The results are summarized when the test is completed
        """        
        print('\r\nDu svarade fel på följande ord:')
        for x in incorrect_answers:
            incorrect = (test_words[x]).get('lemma')
            swedish = (test_words[x]).get('swedish')
            print('{}: {}'.format(incorrect, swedish))
        percent_correct = int(100 * (nr_words_to_test - len(incorrect_answers)) \
                                                    / nr_words_to_test)
        print('Andelen korrekta svar: {}%'.format(percent_correct))
        
        return(this_language)
        
        
    def Print_info(this_language):
        """
        """
        this_language.print_info()
        return(this_language)
    
    def Translate_submenu(this_language):
        """
        """
        this_language.translator.Translate_menu()
        return(this_language)
        
    def Show_info(this_language):
        """
        Show info HTML-files in the web browser
        """
        new = 2
        
        # file_dictionary = this_language.xml_functions.find_info_files()
        file_dictionary = this_language.find_info_files()
        key_list = []
        key_number = 0
        print('There are a number of files available with grammar information')
        print('Please select from the menu below')
        
        for key in file_dictionary:
            key_list.append(key)
            key_number += 1
            print('{}: {}'.format(key_number, key))
        
        selection = input('Välj 1-{} eller (s)kip: '.format(key_number))
        if selection != 's':
            try:
                url = file_dictionary.get(key_list[int(selection) -1])
                # url = "file:///home/jonny/Documents/Studier/Lingvistik/Glos_program/Romanian/Verb_exempel.html"
                print('Attempting to open info_files {} ...'.format(url))
                webbrowser.open(url,new=new)
            except:
                print('No info file available for this selection')
        
        return(this_language)
    
    def Frequency(this_language):
        """
        
        Returns
        -------
        None.

        """
        Nr_entries = 20
        
        elements = this_language.sorted_freq_data
        corpus_size = this_language.freq_analysis.number_entries()
        nr_elements = len(elements)
        print('Antal entries: {}'.format(corpus_size))
        print('Size of the frequency dictionary: ', nr_elements)
        print('The {} most frequent entries:'.format(Nr_entries))
        
        for i in range (0, Nr_entries):
            word = elements[i]
            upos_tag = word.find('upos').text
            counter = int(word.find('counter').text)
            name = word.find('lemma').text
            print('({}) {}: {}'.format(upos_tag.lower(), name, counter))
            
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
        def get_counter(word):
            return(word.find('counter').text)
        
        def find_rank(elements, index):
            for element in elements:
                if element.find('index').text == index:
                    return((elements.index(element)))
            
        
        Total_nr_entries = this_language.freq_analysis.number_entries()
        print('Totalt antal entries: ', Total_nr_entries)
        Lines_per_page = 30
        No_pages = 2
        Nr_words = 2 * No_pages * (Lines_per_page + 2)
        
        sorted_elements = this_language.freq_analysis.\
                            get_sorted_alphabetically(Nr_of_words=Nr_words)
        
        rankings = sorted_elements.copy()
        rankings.sort(reverse=False, key=get_counter)                    
        
        File_path = '/home/jonny/Documents/Studier/Lingvistik/Rumänska'
        Alpha_index = File_path + '/Bok_Frequency/' + 'alpha_index.tex'
        Rank_index = File_path + '/Bok_Frequency/' + 'rank_index.tex'
        # Main_LaTeX_file = File_path + '/Bok_Frequency/' + \
        #                                             'Frequency_analysis.tex'
        print('Creating alphabetical LaTeX file: ', Alpha_index)
        print('Creating LaTeX file sorted by rank: ', Rank_index)
        
        with open(Rank_index, 'w') as latex_output:
            latex_output.write('% !TeX spellcheck = en_US\r\n')
            latex_output.write('\t' + r'%\newpage')
            latex_output.write('\r\n\t' +
                    r'% This is a script generated file from stanza_test.py')
            latex_output.write('´r\n\t' + r'\section{Sorted by rank}')
            latex_output.write('\r\n\t* = translation by Google Translate' + r'\\')
            latex_output.write(
                        '\r\n\t' + r'% Table data from Frequency_dict.xml')
            
            """
            LaTeX table start; Two columns with hardcoded width=6,5cm
            """
        """
        Create the LaTeX file header and define the table properties for
        the alphabetically sorted list
        """
        with open(Alpha_index, 'w') as latex_output:
            latex_output.write('% !TeX spellcheck = en_US\r\n')
            latex_output.write('\t' + r'%\newpage')
            latex_output.write('\r\n\t' +
                    r'% This is a script generated file from stanza_test.py')
            latex_output.write('´r\n\t' + r'\section{Alphabetical index}')
            latex_output.write('\r\n\t* = translation by Google Translate' + r'\\')
            latex_output.write(
                        '\r\n\t' + r'% Table data from Frequency_dict.xml')
            
            """
            LaTeX table start; Two columns with hardcoded width=6,5cm
            """
            for page in range(0, No_pages):
                latex_output.write('\r\n\t' + r'\begin{tabular}{p{6,5cm}p{6,5cm}}')
                latex_output.write('\r\n\t\t' + r'\hline')
                # latex_output.write('\r\n\t\t' + 
                #     r'\multicolumn{2}{|c|}{Alphabetcial sort order}\\ \hline')
                latex_output.write('\r\n\t\t' + 
                    r'\multicolumn{2}{c}{Alphabetcial sort order}\\ \hline')
                # latex_output.write('\r\n\t\t' + r'\hline')
                #latex_output.write('\r\n\t\t' + r'Header1 & Header2\\')
                #latex_output.write('\r\n\t\t' + r'\cline{1-2}')
                latex_output.write('\r\n\t\t' + r'% Dictionary data in two columns')
                
                """
                Fill the table with lemma, swedish explanation etc. for the
                two columns of words
                """
                start_index = page * Lines_per_page
                stop_index = (page +1)* Lines_per_page
                for index1 in range (start_index, stop_index):
                    index2 = index1 + Lines_per_page + 1
                    """
                    Create left column
                    """
                    lemma = sorted_elements[index1].find('lemma').text
                    upos = sorted_elements[index1].find('upos').text
                    index = sorted_elements[index1].find('index').text
                    rank = find_rank(rankings, index)
                    word_lookup = this_language.Word_lookup(lemma, upos)                                    
                    swedish = word_lookup.get('swedish', '---')
                    col1 = rf'\textbf{{{lemma}}} {upos.lower()} {swedish} ({rank})'
                    """
                    Create right column
                    """
                    lemma = sorted_elements[index2].find('lemma').text
                    upos = sorted_elements[index2].find('upos').text
                    index = sorted_elements[index2].find('index').text
                    rank = find_rank(rankings, index)
                    word_lookup = this_language.Word_lookup(lemma, upos)
                    swedish = word_lookup.get('swedish', '---')
                    col2 = rf'\textbf{{{lemma}}} {upos.lower()} {swedish} ({rank})'                    
                    latex_output.write(f'\r\n\t\t{col1}&{col2}' + r'\\')                    
                    print('{}&{}'.format(col1, col2))
                latex_output.write('\r\n\t' + r'\end{tabular}' + '\r\n')
                latex_output.write(r'\newline'+ '\r\n')
            # latex_output.close()
            
            """
            Compile the main LaTeX document
            """
        # time.sleep(1)
        # subprocess.run(["pdflatex", "-synctex=1", "-interaction=nonstopmode", 
        #                 Main_LaTeX_file])
            
        return(this_language)    
    
    def Word_forms(this_language):
        """
        Use a combination of Google Translate and Stanza NLP to find the
        different forms of a word depending on its gender or on the gender
        of the word that it refers to e.g. the different forms of an adjective
        depending on the gender(s) of its associated noun.

        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        """
        Present a list of the word classes to allow the user to select the
        appropriate class for the new word.
        """
        template_list = this_language.find_template('*')
        
        i = 0
        for template in template_list:
            i +=1
            print(f'{i}: {template["tag"]} {template["explanation"]}')            
               
        print('Select tag (ordklass) 1..N or press <enter> if you')
        select = input('do not know the tag: ')
        input_tag = (template_list[int(select) -1])['tag']
        print(f'Selected tag: {input_tag}')
        
        return(this_language)
    
    def Get_statistics(this_language):
        """
        Get the statistics regarding the size and growth of the dictionary.
        
        Get the intire dictionary as a list of Python dictionaries. Go
        through each word and use the index field to extract date of creation.
        Use the information to create the number of words created per day

        Parameters
        ----------
        this_language : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        """
        
        """
        template_list = this_language.find_template('*')
        found_words = this_language.find_tag('*')
        
        date_list = []
        weight_list = []
        bmi_list = []
        
        for word in found_words:
            date_str = word.get('index', '')[0:10]
            date_list.append(date_str)
            
        print(date_list)
        """
        """
        format_str = "%Y-%m-%d"
        myFmt = mdates.DateFormatter(format_str)
        
        first_year = date_list[0].date().year
        latest_year = date_list[-1].date().year
        plot_end_date = date_list[-1] + timedelta(days=120)        
        
        fig, ax1 = plt.subplots()
        ax1.xaxis.set_major_formatter(myFmt)
        ax1.plot(date_list, weight_list, label='Vikt')
        # ax.plot(Target_weight, label='Målvikt')
        # ax1.axhline(y=Target_weight, color='red', label='Målvikt')
        # ax1.axhline(y=78, color='Cyan', label='BMI normal')
        ax1.set_xlim(date_list[0], plot_end_date)
        fig.autofmt_xdate()
        ax1.set_title(f'Vocabulary growth {first_year} - {latest_year}')
        ax1.set_ylabel('Ackumulated size', color='blue')
        # ax1.set_ylim(plot_low_limit, plot_hi_limit)
        ax1.legend()
        # Add a second axis to the plot
        ax2 = ax1.twinx()
        ax2.set_ylabel('Growth', color='green')
        ax2.plot(date_list, bmi_list, label='BMI', color='green')
        # ax2.set_ylim(BMI_low_limit, BMI_hi_limit)
        # ax2.set_xlim(date_list[0], target_date)
        # plt.savefig(this_person.name + '_weight.png')
        plt.savefig("WeightLoss.png")
        # plt.show()
        
        
        
    def Do_nothing(this_language):
        print("Felaktigt val")
        return(this_language)
    
    
    """
    The option dictionary holds all meny items and their associated
    funtions to call. The pointer to the functions are retrieved 
    with options.get(...) function call
    """
    options = {"a": ['Add word', Add_word],
               "z": ['Get statistics', Get_statistics],
               "i": ["Info", Show_info],
               "l": ['List words', List_words],
               "s": ['Search word', Search_word],
               "e": ['Edit word', Update_word],
               "o": ['Translate_submenu', Translate_submenu],
               "t": ['Take test', Word_test],
               "f": ['Frequency analysis', Frequency],
               "ff": ['Find word forms', Word_forms],
               "c": ['Change language', Change_language],
               "r": ['LaTeX generator', LaTeX_generator],
               "q": ['Quit', Do_nothing]}
    
    while True:
        """
        Use dictionary lookup to select next thing to do or "quit"
        Present a menu of items
        """
        print('\r\nAktuellt språk är: ', current_language.language)
        print(f'Antal ord i ordlistan är: {current_language.size_ofDictionary()}')
        size_of_frequncy_list = current_language.freq_analysis.size_ofDictionary()
        print(f'Antal ord i frekvensordlistan är:{size_of_frequncy_list}')
        print('Huvudmeny - här väljer man mellan...')
        for key in options:
            print(key + ': ' + options[key][0])
            
        Next_option = input('Val: ')
        
        if Next_option == "q":
            """
            Flush the xml tree to the xml dictionary file
            """
            for language in Language_list:

                print("Writing data to: ", language.data_file)
                language.xml_tree2file()
            break
        try:
            current_language = options.get(Next_option, Do_nothing)[1] \
                                                            (current_language)
        except:
            print('Incorrect selection')
