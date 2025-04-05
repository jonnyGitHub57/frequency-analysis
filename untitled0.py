# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:31:45 2025

@author: jonny
"""

import stanza
import spacey_stanza
from spacy_stanza import StanzaLanguage

snlp = stanza.Pipeline(lang="ro")
nlp = StanzaLanguage(snlp)

doc = nlp("Această propoziție este în limba română.")
for token in doc:
    print(token.text, token.lemma_, token.pos_)
