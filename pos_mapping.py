import pandas as pd
import numpy as np
from collections import defaultdict
import gc
import textacy
import spacy
from collections import defaultdict
import json

class pos_tagging_mapping:
    @staticmethod
    def grammar_dict_map(dataframe, nsl_rules):
        """reads the dataframe and loading spacy model and using grammar rules with regex return nouns and verb dictionary

        Args:
            dataframe (pd.Dataframe): dataframe retuned from cleaning
            nsl_rules (json_file): NSL grammar rules

        Returns:
             dataframe (pd.Dataframe) : dataframe (nouns and verbs chunks)
        """
        
        f = open(nsl_rules)
        data = json.load(f)
        pattern = data["verb_pattern"]

        nlp = spacy.load("en_core_web_sm")
        gc.collect()
        verbs = defaultdict(list)
        nouns = defaultdict(list)
        for i in dataframe["Measures"]:
            if "percentage of" in i :
                doc = nlp(i)
                about_talk_text = i
                verb_pattern = [pattern]
                about_talk_doc = textacy.make_spacy_doc(about_talk_text, lang="en_core_web_sm")
                verb_phrases = textacy.extract.matches(about_talk_doc, verb_pattern) 
                for chunk_verb in verb_phrases:
                    verbs[i].append(chunk_verb)
                for chunk_noun in doc.noun_chunks:
                    nouns[i].append(chunk_noun)
            else : 
                pass
        nouns = dict(nouns)
        verbs = dict(verbs)
        dataframe["Nouns_chunks"] = dataframe["Measures"].map(nouns)
        dataframe["Verbs_chunks"] = dataframe["Measures"].map(verbs)

        return dataframe