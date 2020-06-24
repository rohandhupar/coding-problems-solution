import pandas as pd 
from collections import defaultdict
import gc
import re
class engine():
    def check_for_blacklist(self,sentence):
        black_list = ['percentage ', 'number ', 'total ', 'average ', 'gross ', 'net ']
        for item in black_list:
            if item in sentence:
                return True
        return False
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
        operand1 = defaultdict(list)
        blacklist=engine()

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
            elif 'number of ' in k:
                idx=k.index('number of ')
                if idx==0:
                    sub_string=k.split("number of ")[-1]
                    if 'of ' in sub_string:
                        idx_1=sub_string.index('of ')
                        if idx_1!=-1:
                            output='total '+sub_string[idx+3:]
                        else:
                            output='total '+k.split("number of ")[-1]
                            operand1[k].append(output)
            elif 'total ' in k:
                idx=k.index('total ')
                if idx==0:
                    output='total '+k.split("total ")[-1]
                    operand1[k].append(output)
            elif 'gross ' in k:
                idx=k.index('gross ')
                if idx==0:
                    output='total '+k.split("gross ")[-1]
                    operand1[k].append(output)
            elif 'net ' in k:
                idx=k.index('net ')
                if idx==0:
                    sub_string=k.split("net ")[-1]
                    sub_string_checker=blacklist.check_for_blacklist(sub_string)
                    if sub_string_checker==False:
                        output='total '+sub_string
                        operand1[k].append(output)
                

            # elif "total of "  in k:   
        gc.collect()
        operand1 = dict(operand1)
        numerator = dict(numerator)
        denominator = dict(denominator)
        dataframe["Numerator"] = dataframe["Measures"].map(numerator)
        dataframe["Denominator"] = dataframe["Measures"].map(denominator)
        dataframe["operand1"] = dataframe["Measures"].map(operand1)
        dataframe=dataframe[["Measures","operand1","Numerator","Denominator"]]
        dataframe.columns=["Measures","Single operand","Numerator","Denominator"]
        
        return dataframe