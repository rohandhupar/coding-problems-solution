import pandas as pd 
from collections import defaultdict
import operator
import gc
import re
import json 
class engine():
    
    def expression_engine(self,values,ops):
        """
        expression evaluation engine which return evaluated string expression 

        Args:
            values (List): Text expression in list
            ops (dict): operator dictionary

        Returns:
            text: evaluated expression
        """
        new_value=""
        for i in range(1,len(values),2):
            if values[i] =="+":
                left_operand=values[i-1:i][0]
                left_operand="".join(left_operand+str(" "))
                operation=ops[values[i]]
                right_operand=values[i+1:i+2][0]
                if len(new_value)>0:
                    new_value=ops[operation](new_value,right_operand)
                else :
                    new_value=ops[operation](left_operand,right_operand)
                    
            elif values[i]=="-":
                left_operand=values[i-1:i][0]
                left_operand="".join(left_operand+str(" "))
                operation=ops[values[i]]
                right_operand=values[i+1]
                if len(new_value)>0:
                    new_value=new_value.replace(right_operand,"",1)
                else :
                    new_value=left_operand.replace(right_operand,"",1)
        return new_value
            
    
    def eval_expression(self,value):
        """
        start the engine for evaluation of string expressions and control the flow

        Args:
            value (List): text expression in list

        Returns:
            text : evaluated expression
        """
        
        ops = {"+": operator.add,"-":operator.sub}
        engine_components=engine()
        expression=engine_components.expression_engine(value,ops)
        
        return expression
    
    @staticmethod
    def rules(dataframe,rules_filename):
        """reads the dataframe and use rule engine to form numerator and denominator 
        Args:
            dataframe (pd.dataframe): reads the dataframe
            file (str) : rule engine file name (json)

        Returns:
            dataframe: consists of numerator & denominator dataframe 
        """
        # non_complex_l_1=[]
        engine_components=engine()
        rules = open(rules_filename)
        operands = open("operands.json")
        numerator = defaultdict(list)
        denominator = defaultdict(list)
        single_operand=defaultdict(list)
        rules=json.load(rules)
        operands_dict=json.load(operands)
        for k, i, j,l in zip(
            dataframe["Measures"], dataframe["Nouns_chunks"], dataframe["Verbs_chunks"],dataframe["Adjective_chunks"]
        ):  
            value1=[]
            value2=[]
            measure_value=k.split()
            if len(measure_value)>1:
                operation=measure_value[0]+" "+measure_value[1]
                operation1=measure_value[0]
            #### Single operand structure ready for the code ####
                if operation in operands_dict["operands"]["single_operands"] or operation1 in operands_dict["operands"]["single_operands"]:
                    for rule_number in rules.keys():
                        for keys in rules[rule_number].keys():
                            keys_list=keys.split(",")
                            if operation in keys_list:
                                for task_number in rules[rule_number][keys].keys():
                                    rules[rule_number][keys][task_number][0]["value1"]["measure"] = k
                                    rules[rule_number][keys][task_number][0]["value1"]["string1"] = operation
                                    numerator_json_dict=(rules[rule_number][keys][task_number][0]["value1"])
                        
                            elif operation1 in keys_list :
                                for task_number in rules[rule_number][keys].keys():
                                    rules[rule_number][keys][task_number][0]["value1"]["measure"] = k
                                    rules[rule_number][keys][task_number][0]["value1"]["string1"] = operation1
                                    numerator_json_dict=(rules[rule_number][keys][task_number][0]["value1"])
                    for x,z in numerator_json_dict.items():
                        value1.append(z)
                    single_operand[k].append(engine_components.eval_expression(value1))                                
                ############################## Single operand code execution ended #########################
                
                ############################# Multiple operand code execution started #######################
                elif operation in operands_dict["operands"]["multiple_operands"]:
                    for rule in ["rule2"]:    
                        for string_mathced in rules[rule].keys():
                            for task in rules[rule][string_mathced].keys():
                                for req,value in rules[rule][string_mathced][task][0]["value1"].items():
                                    if req == "measure":
                                        if value=="yes":
                                            rules[rule][string_mathced][task][0]["value1"]["measure"]=k
                                            print(rules[rule][string_mathced][task][0]["value1"])
                                    elif req == "rule_matched":
                                        if value=="yes":
                                            rules[rule][string_mathced][task][0]["value1"]["rule_matched"]=operation
                                    elif req == "string_after":
                                        if value =="empty":
                                            pass
                                        elif value[0] == "yes":
                                            for i in range(len(measure_value)):
                                                if measure_value[i] in value[0:]:
                                                    string_after=" ".join(measure_value[i+1:])
                                                    rules[rule][string_mathced][task][0]["value1"]["string_after"][1]=string_after
                                                else : break 
                                        continue
                                    elif req == "string_before":
                                        if value =="empty":
                                            pass
                                        elif value[0] == "yes":
                                            for i in range(len(measure_value)):
                                                if measure_value[i] in value[0:]:
                                                    string_before=" ".join(measure_value[:i])
                                                    rules[rule][string_mathced][task][0]["value1"]["string_before"][1]=string_before
                                                    
                                                else : break 
                                        continue
                                    elif req == "articles":
                                        if value =="empty":
                                            rules[rule][string_mathced][task][0]["value1"]["articles"]="empty"
                                        elif value == "yes":
                                            articles=[]
                                            if set("a","an","the").issubset(set(measure_value)):
                                                for i in ["a","an","the"]:
                                                    if i in measure_value:
                                                        articles.append(i)        
                                                rules[rule][string_mathced][task][0]["value1"]["articles"]=articles
                                            else :
                                                break
 
                                                
                                                    
                                            
                                            

                                            
                                            
                                            
                                            
                                            
                                    

                                        
                                           
                                   
                                   

                               
                           
                           
                        
                    
                    

                                                
                     
        gc.collect()
        single_operand = dict(single_operand)
        # numerator = dict(numerator)
        # denominator = dict(denominator)
        dataframe["Single_operand"] = dataframe["Measures"].map(single_operand)    
        # dataframe["Numerator"] = dataframe["Measures"].map(numerator)
        # dataframe["Denominator"] = dataframe["Measures"].map(denominator)
        
        dataframe=dataframe[["Measures","Single_operand"]]        
        return dataframe
                                     
                
                
                 
                 
                 
                 
                 
        