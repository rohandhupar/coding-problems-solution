class nsl_grammar_engine()


def file_preprocess(file_name):
    """
    read the file and preprocess it 
    
    @params file name : takes file name
    
    @return : dataframe
    """
    df = pd.read_excel(file_name)
    new_df=df.copy()
    new_df = new_df.replace(np.nan,'', regex = True)
    new_df.replace(',','_', regex=True, inplace=True)
    new_df=new_df[0:30]
    
    return new_df

def grammar_dict_map(dataframe):
    """
    read the dataframe and loading spacy model and using grammar rules with regex return nouns and verb dictionary
    
    @params dataframe : dataframe (preprocessed)
    
    @return dataframe : dataframe (nouns and verbs chunks) 
    """ 
    nlp = spacy.load("en_core_web_sm")
    gc.collect()
    verbs=defaultdict(list)
    for i in dataframe["Measures"]:
        about_talk_text =i
        pattern = r'(<VERB>?<ADV>*<VERB>+)'
        about_talk_doc = textacy.make_spacy_doc(about_talk_text,lang='en_core_web_sm')
        verb_phrases = textacy.extract.pos_regex_matches(about_talk_doc, pattern)
        for chunk in verb_phrases:
            verbs[i].append(chunk)    
    nouns=defaultdict(list)
    for i in dataframe["Measures"]:
        doc = nlp(i)
        for chunk in doc.noun_chunks:
            nouns[i].append(chunk)          
    nouns=dict(nouns)
    verbs=dict(verbs)
    dataframe["Nouns_chunks"]=dataframe["Measures"].map(nouns)
    dataframe["Verbs_chunks"]=dataframe["Measures"].map(verbs)
    
    return dataframe 

def data_transformation(dataframe):
    """
    @params dataframe : takes dataframe consists of nouns and verbs chunks and transforms
                        their data structure from list of tuples to list.
    
    @return dataframe : cleanned and preprocessed dataframe  
    """
    nouns=defaultdict(list)
    for i,j in zip(dataframe["Measures"],dataframe["Nouns_chunks"]):
        for k in j[1:]:
            nouns[i].append(str(k))
    nouns=dict(nouns)
    new_df["Nouns_chunks"]=dataframe["Measures"].map(nouns)    
    verbs=defaultdict(list)
    for i,j in zip(dataframe["Measures"],dataframe["Verbs_chunks"]):
        if str(j)!="nan":
            for k in j:
                verbs[i].append(k[0])
    verbs=dict(verbs)
    dataframe["Verbs_chunks"]=dataframe["Measures"].map(verbs)
    
    gc.collect()
    return dataframe






def rule_engine()
    numerator=defaultdict(list)
    denominator=defaultdict(list)
    
    for k,i,j in zip(new_df["Measures"],new_df["Nouns_chunks"],new_df["Verbs_chunks"]):
        if str(j)!="nan":
            numerator[k].append(str(i[0]))
            denominator[k].append("Total number of "+str(j[0]))
            print(k,":",":","numerator: ",str(i[0])+" "+str(j[0])," " +"denominator: ","Total number"+" "+str(i[0]))
        else :
            if len(i)==1:
                numerator[k].append(str(i[0].split()[0])+" "+str(i[0].split()[1]))
                denominator[k].append("Total number of "+str(i[0].split()[1]))
            elif len(i)==2:
                numerator[k].append(str(i[0]))
                denominator[k].append("Total number of "+str(i[1]))
            elif len(i)>=3:
                if "percentage" in i :
                    i=list(i)
                    i=i.remove("percentage")
                    print(i)
                    numerator[k].append(str(i[0]))
                    denominator[k].append("Total number of",str(i[1]))
                else : 
                    right_hand_index=len(i)//2
                    numerator[k].append(" ".join(i[:]))
                    denominator[k].append(" ".join(i[right_hand_index:]))
    gc.collect()
    numerator=dict(numerator)
    denominator=dict(denominator)
    new_df["Numerator"]=new_df["Measures"].map(numerator)
    new_df["Denominator"]=new_df["Measures"].map(denominator)
    df=df.append(new_df)
    return df