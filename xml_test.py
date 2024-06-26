#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 15:26:08 2022

@author: jonny

https://docs.python.org/3/library/xml.etree.elementtree.html
https://www.youtube.com/watch?v=1JblVElt5K0
https://stackoverflow.com/questions/18796280/how-do-i-set-attributes-for-an-xml-element-with-python

Komplett instruktion om add element
https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-elementtree-to-pretty-print-to-an-xml-file
"""

# import pandas as pd
import random
import xml.etree.ElementTree as ET

class XML_Wictionary(object):
    """
    The class XML_Wictionary handles the xml-files and -trees that keep all 
    words and links to information files etc. The class is imported by the 
    class Wictionary and used by the main program to find words in the
    xml-tree. There can only be one instance of this class per language
    """
    def __init__(self, language, Debug=False):
        """
        Initialize the instance of the class and load the corresponing
        xml-file into an xml-tree strcuture in memory.        
        """
        self.language = language
        self.debug = Debug
        
        self.data_file = './' + self.language + '/Wictionary.xml'
        self.tree = ET.parse(self.data_file)
        self.root = self.tree.getroot()
        self.postfix_noun = self.root.findall('./postfix')[0].find('used').text \
                                                                        == 'yes'

    def xml_tree2file(self):
        """
        Write the tree to the corresponding XML-file. This can be done at
        any time to avoid that any data is lost in case of sudden or unexpected
        closing of the main program
        """
        self.tree.write(self.data_file, encoding="UTF-8", xml_declaration=True)
    
    def size_ofDictionary(self):
        """
        

        Returns
        -------
        The number of words in the dictionary as an integer

        """
        return(len(self.root.findall('./word')))
        
        
    def addElement(self, element):
        """
        Add an element to the xml tree in a "pretty print" format so that 
        the element is written to the xml file using the method from 
        "https://stackoverflow.com/questions/28813876/how-do-i-get-pythons-
                                    elementtree-to-pretty-print-to-an-xml-file"
        This keeps the xml-file in a readable format with correct tabbing etc.

        Parameters
        ----------
        element : python dictionary
            element: {'lemma': 'fiets, 'tag':'NOUN', 'swedish': 'cykel', ...}

        Returns
        -------
        None.

        """
        addElement = ET.Element("word")             # Make a new 'word' element
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
        self.root[-1].tail = "\n\t" # Edit the previous element's tail, so that our  
        self.root.append(addElement) # new element is properly aligned/formatted
        
    
    def elements2dictionary(self, elements):
        """
        elements is a list of elements in the xml tree. Each element is 
        extracted into a dictionary that is returned to the caller


        Parameters
        ----------
        elements : list of elements
            elements = [element1, element2, ...]

        Returns
        -------
        dict_list : list of python dictionaies
            dict_list = [dictionary1, dictionary2, ...]

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
    
    def update_element_from_dict(self, word_dictionary):
        """
        Updates one word element in the XML tree based on the
        unique time stamp that can never be changed or updated

        Parameters
        ----------
        dictionary_input : TYPE dictionary
            DESCRIPTION.

        Returns
        -------
        None.

        """
        index_to_find = word_dictionary.get('index', '')
        elements = self.root.findall('./word')
        
        for element in elements:
            if index_to_find == element.find('index').text:
                for child in element:
                    if child.tag != 'index' and child.tag != 'counter':                 
                        child.text = word_dictionary[child.tag]                    
        
        
    def find_gender_xref(self):
        """
        Returns the cross reference table/list for the gender vs. article
        Nederlands: maskulinum, feminimu = de; neutrum = het
        Romanian: maskulinum, neutrum = un; femininum = o
        ....
        """
        elements = self.root.findall('./gender_article')
        
        return((self.elements2dictionary(elements))[0])
        
    def find_verb_list_items(self):
        """
        Returns the list of items to  list for a verb as defined by the
        part in the XML-dictionary file
        ....
        """
        elements = self.root.findall('./verb_listing')
        
        return((self.elements2dictionary(elements))[0])
    
    def get_postfix(self):
        """
        

        Returns
        -------
        True if the language uses postfix notation for the nouns such as in
        Swedish and Romanian languages where the gender is an ending to the 
        noun rather than ...

        """
        post_fix = self.root.findall('./postfix')[0].find('used').text == 'yes'
        print(post_fix)
        return(post_fix)
    
    def find_info_files(self):
        """
        Returns a dictionary with the keys and links to the different info
        files as specified in the XML-dictionary file. There is only one such
        element in the XML-file, hence the ...[0]
        """
        elements = self.root.findall('./info_files')
        
        return((self.elements2dictionary(elements))[0])

    def find_lemma(self, lemma, tag='*'):
        """
        'find_lemma' will traverse all <word> elements in the tree to find
        all perfect matches to the word. It searches for the word among the
        foreign language lemmas.
        Returns a list of (tree) elements
        """
        elements = self.root.findall('./word')
        # print('Searched words: ', len(elements))
        found_elements = []
        for child in elements:
            if lemma == child.find('lemma').text:
                if tag == '*':
                    found_elements.append(child)
                    if self.debug == True:
                        print(child.find('lemma').text)
                elif tag == child.find('tag').text:
                    found_elements.append(child)
                    if self.debug == True:
                        print(child.find('lemma').text)
                else:
                    pass
        
        return(found_elements)

    def find_word(self, search_word):
        """
        'Find_word' will traverse all <word> elements in the tree to find
        all possible matches (not only perfect match) to the word. It searches
        for the word in swedish as well as the foreign language
        Returns a list of (tree) elements
        """
        elements = self.root.findall('./word')
        print('Searched words: ', len(elements))
        found_elements = []
        for child in elements:
            added = False
            lemma = child.find('lemma').text
            swedish = child.find('swedish').text
            if lemma != None:
                if lemma.find(search_word) != -1:
                    found_elements.append(child)
                    added = True
                    if self.debug == True:
                        print(lemma)
            if swedish != None and added == False:
                if swedish.find(search_word) != -1:
                    found_elements.append(child)
                    if self.debug == True:
                        print(swedish)
            
        return(found_elements)
        
    def find_random_words(self, nr_words, search_tag='*'):
        """
        Pick a number of random word elements from the xml-tree and
        return them as a list of dictionaries. Make sure that both
        'lemma' and 'swedish' exist for word test
        """
        elements = self.root.findall('./word')
        print('Searched words: ', len(elements))
        
        if search_tag == '*':
            found_elements = elements
        else:
            found_elements = []
            for child in elements:
                tag = child.find('tag').text
                if tag != None:
                    if tag.find(search_tag) != -1 :
                        found_elements.append(child)
                        if self.debug == True:
                            print(child.find('lemma').text)
                            
        random_elements = []
        dict_size = len(found_elements)
        
        nr_to_test = min(nr_words, dict_size)
        already_taken = []
        x = 1
        while x <= nr_to_test:
            test_entry = random.randint(1, dict_size - 1)
            while test_entry in already_taken:
                test_entry = random.randint(1, dict_size - 1)
            child = found_elements[test_entry]    
            lemma = child.find('lemma').text
            swedish = child.find('swedish').text
            tag = child.find('tag').text
            if lemma != None and swedish != None and tag !='PUNCT':
                x += 1
                random_elements.append(child)
                already_taken.append(test_entry)
                if self.debug == True:
                        print('{}: {}'.format(lemma, swedish))
                        
        return(self.elements2dictionary(random_elements)) 
        
        
    def find_template(self, search_tag):
        """
        Find the template that corresponds to a certain tag  
        and return it as a list of dictionaries with just one
        element in the list
        
        """
        elements = self.root.findall('./template')
        # print('Number of templates: ', len(elements))
        if search_tag == '*':
            template_list = elements
        else:
            template_list = []
            for template in elements:
                tag = template.find('tag').text
                if tag == search_tag:
                    template_list.append(template)
                           
        return(self.elements2dictionary(template_list)) 
        
    def searchWord(self, word):
        """
        """
        found_elements = self.find_word(word)

        return(self.elements2dictionary(found_elements))
        
    def find_tag(self, search_tag):
        """
        'find_tag' traverses all <word> elements in the tree to find
        all possible items with tag =  'search_tag' in the word. 
        
        Returns a list of (tree) elements

        Parameters
        ----------
        search_tag : string
            All words withe a certain tag (ordklass) will be returned. If
            search-tag == '*' all words will be returned.

        Returns
        -------
        None.

        """
        # def get_lemma(word):
        #     return(word.find('lemma').text)
        
        elements = self.root.findall('./word')
        print('Number of words: ', len(elements))
        
        if search_tag == '*':
            found_elements = elements
        else:
            found_elements = []
            for child in elements:
                tag = child.find('tag').text
                if tag != None:
                    if tag.find(search_tag) != -1 :
                        found_elements.append(child)
                        if self.debug == True:
                            print(child.find('lemma').text)
                            
        print('Number of words found: ', len(found_elements))
        # found_elements.sort(reverse=False, key=get_lemma)
        
        return(self.elements2dictionary(found_elements))

    

if __name__=='__main__':
    """
    Beginning of main code for 
    """
    
    print('Place holder for main program')
        
        
   