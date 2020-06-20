import pandas as pd
import numpy as np
import textacy
import spacy
from collections import defaultdict
import gc
import click
import json


class nsl_Grammar_rule_engine:
    def file_preprocess(self, file_name):
        """
        read the file and preprocess it 
        
        @params file name : takes file name
        
        @return : dataframe
        """
        df = pd.read_excel(file_name)
        new_df = df.copy()
        new_df = new_df.replace(np.nan, "", regex=True)
        new_df.replace(",", "_", regex=True, inplace=True)
        return new_df

    def grammar_dict_map(self, dataframe, nsl_rules, operation):
        """
        reads the dataframe and loading spacy model and using grammar rules with regex return nouns and verb dictionary
        
        @params dataframe : dataframe (preprocessed)
        @params nsl_rules : file name for nls grammar rules 
        @operation        : mathematical operation over which nsl rules will be applied
        
        @return dataframe : dataframe (nouns and verbs chunks) 
        """
        f = open(nsl_rules)
        data = json.load(f)
        pattern = data["verb_pattern"]

        nlp = spacy.load("en_core_web_sm")
        gc.collect()
        verbs = defaultdict(list)
        for i in dataframe["Measures"]:
            about_talk_text = i
            verb_pattern = [pattern]
            about_talk_doc = textacy.make_spacy_doc(about_talk_text, lang="en_core_web_sm")
            verb_phrases = textacy.extract.matches(about_talk_doc, verb_pattern) ### pos_regex_matches 
            for chunk in verb_phrases:
                verbs[i].append(chunk)
        nouns = defaultdict(list)
        for i in dataframe["Measures"]:
            doc = nlp(i)
            for chunk in doc.noun_chunks:
                nouns[i].append(chunk)
        nouns = dict(nouns)
        verbs = dict(verbs)
        dataframe["Nouns_chunks"] = dataframe["Measures"].map(nouns)
        dataframe["Verbs_chunks"] = dataframe["Measures"].map(verbs)

        return dataframe

    def data_transformation(self, dataframe):
        """
        reads the dataframe and transformed the grammar chunks so that they can parse into rule engine
        
        @params dataframe : takes dataframe consists of nouns and verbs chunks and transforms
                            their data structure from list of tuples to list.
        
        @return dataframe : cleanned and preprocessed dataframe  
        """
        nouns = defaultdict(list)
        for i, j in zip(dataframe["Measures"], dataframe["Nouns_chunks"]):
            for k in j[1:]:
                nouns[i].append(str(k))
        nouns = dict(nouns)
        dataframe["Nouns_chunks"] = dataframe["Measures"].map(nouns)
        verbs = defaultdict(list)
        for i, j in zip(dataframe["Measures"], dataframe["Verbs_chunks"]):
            if str(j) != "nan":
                for k in j:
                    verbs[i].append(k[0])
        verbs = dict(verbs)
        dataframe["Verbs_chunks"] = dataframe["Measures"].map(verbs)

        gc.collect()
        return dataframe

    def rule_engine(self, dataframe):
        """
        reads the dataframe and use rule engine to form numerator and denominator 
        
        @params dataframe : reads the dataframe 
        
        @returns dataframe : consists of numerator & denominator dataframe  
        """
        numerator = defaultdict(list)
        denominator = defaultdict(list)

        for k, i, j in zip(
            dataframe["Measures"], dataframe["Nouns_chunks"], dataframe["Verbs_chunks"]
        ):
            if str(j) != "nan":
                numerator[k].append(str(i[0]))
                denominator[k].append("Total number of " + str(j[0]))
            #             print("numerator: ",str(i[0])+" "+str(j[0])," " +"denominator: ","Total number"+" "+str(i[0]))
            else:
                if len(i) == 1:
                    if len(i[0].split()) != 1:
                        numerator[k].append(str(i[0].split()[0]) + " " + str(i[0].split()[1]))
                        denominator[k].append("Total number of " + str(i[0].split()))
                elif len(i) == 2:
                    numerator[k].append(str(i[0]))
                    denominator[k].append("Total number of " + str(i[1]))
                elif len(i) >= 3:
                    if "percentage" in i:
                        i.remove("percentage")
                        numerator[k].append(str(i[0]))
                        denominator[k].append("Total number of " + str(i[1]))
                    else:
                        right_hand_index = len(i) // 2
                        numerator[k].append(" ".join(i[:]))
                        denominator[k].append(" ".join(i[right_hand_index:]))
        gc.collect()
        numerator = dict(numerator)
        denominator = dict(denominator)
        dataframe["Numerator"] = dataframe["Measures"].map(numerator)
        dataframe["Denominator"] = dataframe["Measures"].map(denominator)
        return dataframe


@click.command()
@click.option("--filename", prompt="pls enter the file name")
@click.option("--nsl_rules", prompt="pls enter the file name for rules")
@click.option(
    "--operation",
    prompt="enter the mathematical operation according to that nsl grammar rules will be selected",
)
def main(filename, nsl_rules, operation):
    rule_engine_components = nsl_Grammar_rule_engine()
    df = rule_engine_components.file_preprocess(filename)
    df = rule_engine_components.grammar_dict_map(df, nsl_rules, operation)
    df = rule_engine_components.data_transformation(df)
    df = rule_engine_components.rule_engine(df)
    df.to_csv("nsl_operands.csv")


if __name__ == "__main__":
    main()
