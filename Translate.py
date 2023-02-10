# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#from googletrans import Translator
import googletrans

class User_translate(object):
    """ 
        The class 'Verbs' handles words that are 'verbs'
    """
    def __init__(self, language , Debug=False):
        self.debug = Debug
        self.language = language
        if self.language == 'Nederlands':
            self.src_dest = 'nl'
        elif self.language == 'Romanian':
            self.src_dest = 'ro'
        else:
            self.src_dest = 'en'
        self.ext_translator = googletrans.Translator()
        
    def translate_to_swedish(self , text):
        """
        """
        return(self.ext_translator.translate( text, src=self.src_dest , 
                                                             dest='sv').text)
        
    def translate_from_swedish(self , text):
        """
        """
        return(self.ext_translator.translate( text, src='sv' , 
                                                     dest=self.src_dest).text)
   
    def Translate_menu(self):
        """
        Seach for a word in the word lists. Match criteria is partly TBD
        """
        print("Här har du tillgång till ett användargränssnitt mot ")
        print("Google Translate där svenska och nederländska är förinställt")
        print("men/och där man väljer åt vilket håll man vill översätta")
            
        def To_swedish():
            """
            Print all conjunctions in the list")
            """
            text_to_translate = input('Text: ')
            print(self.translate_to_swedish(text_to_translate))
        
        def From_swedish():
            """
            Print all conjunctions in the list")
            """
            text_to_translate = input('Text: ')
            print(self.translate_from_swedish(text_to_translate))
            
        def Help_get():
            """
            Display the help text
            """
            #self.Print_help()
        
        def sequencer(Next_option):
            options = {"f": From_swedish,
                       "t": To_swedish,
                       "?": Help_get,
                       "h": Help_get,
            }.get(Next_option, Help_get)
            return (options)()
    
        while True:
            # map the inputs to the function blocks
            print("Meny för hantering av översättningar...")
            #print(", l=skriv lista, a=lägg till,")
            Next_option= input("f=från svenska, t=till svenska, b=back\n>")
            if Next_option=="b":
                break
            current_person = sequencer(Next_option)     
        
"""
Test code that only execute as 'main'
"""
if __name__=='__main__':
    print('Run class \'User_translate\' test code')
    #print(googletrans.LANGUAGES)
    
    translator = User_translate('Nederlands')
    
    text_to_translate = 'het varken snurkt'
    result = translator.translate_to_swedish(text_to_translate)
    print(text_to_translate, ': ', result)
    
    text_to_translate = 'solen lyser'
    result = translator.translate_from_swedish(text_to_translate)
    print(text_to_translate, ': ', result)
    
    translator.Translate_menu()
    
    