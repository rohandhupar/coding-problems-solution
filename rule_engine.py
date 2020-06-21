import pandas as pd 
from collections import defaultdict
import gc
import re
class engine():
    @staticmethod
    def rules(dataframe):
        """reads the dataframe and use rule engine to form numerator and denominator 
        Args:
            dataframe (pd.dataframe): reads the dataframe

        Returns:
            dataframe: consists of numerator & denominator dataframe 
        """
        numerator = defaultdict(list)
        denominator = defaultdict(list)

        for k, i, j in zip(
            dataframe["Measures"], dataframe["Nouns_chunks"], dataframe["Verbs_chunks"]
        ):  
            if "percentage of" in k:
                if isinstance(i,list) or isinstance(j,list):
                    if str(i)!="nan" or str(j)!="nan":
                        if str(j) != "nan" and str(i)!="nan":
                            numerator[k].append(str(i[0])+" "+str(j[0]))
                            denominator[k].append("Total number of " + str(i[0]))
                        else:
                            if isinstance(i,list):
                                if len(i) == 1 :
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
            # elif "number of " in k:
                
            # elif "total of "  in k:   
        gc.collect()
        numerator = dict(numerator)
        denominator = dict(denominator)
        dataframe["Numerator"] = dataframe["Measures"].map(numerator)
        dataframe["Denominator"] = dataframe["Measures"].map(denominator)
        
        return dataframe