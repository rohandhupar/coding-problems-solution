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
        engine_components=engine()
        rules = open(rules_filename)
        operands = open("operands.json")
        numerator = defaultdict(list)
        denominator = defaultdict(list)
        single_operand=defaultdict(list)
        exception="percentage of"
        exception1="total"
        rules=json.load(rules)
        operands=json.load(operands)
        for k, i, j,l in zip(
            dataframe["Measures"], dataframe["Nouns_chunks"], dataframe["Verbs_chunks"],dataframe["Adjective_chunks"]
        ):  
            value1=[]
            value2=[]
            measure_value=k.split()
            if len(measure_value)>1:
                operation=measure_value[0]+" "+measure_value[1]
                operation1=measure_value[0]
                if operation in operands["single_operands"] or operation1 in operands["single_operands"]:
                    if operation in rules["string_match"]:
                        rules['string_match'][operation][0]["value1"]["measure"] = k
                        numerator_json_dict=(rules["string_match"][operation][0]["value1"])
                        for x,z in numerator_json_dict.items():
                            value1.append(z)
                        single_operand[k].append(engine_components.eval_expression(value1))
                    elif operation1 in rules["string_match"]:
                        rules['string_match'][operation1][0]["value1"]["measure"] = k
                        numerator_json_dict=(rules["string_match"][operation1][0]["value1"])
                        for x,z in numerator_json_dict.items():
                            value1.append(z)
                        single_operand[k].append(engine_components.eval_expression(value1))
                        
                                           
                    # if operation in file["string_match"] and operation!=exception:
                        # if str(l)!="nan" :
                        #     file['string_match'][operation][0]["value1"]["measure"] = k
                        #     file['string_match'][operation][0]["value2"]["measure"] = k
                        #     file['string_match'][operation][0]["value2"]["measure"] = l
                        #     numerator_json_dict=(file["string_match"][operation][0]["value1"])
                        #     denominator_json_dict=(file["string_match"][operation][0]["value2"])
                        #     for x,z in numerator_json_dict.items():
                        #         value1.append(z)
                        #     for x,z in denominator_json_dict.items():
                        #         value2.append(z)
                        #     numerator[k].append(engine_components.eval_expression(value1))
                        #     denominator[k].append(engine_components.eval_expression(value2))
                        
                        # file['string_match'][operation][0]["value1"]["measure"] = k
                        # numerator_json_dict=(file["string_match"][operation][0]["value1"])
                        # for x,z in numerator_json_dict.items():
                        #     value1.append(z)
                        # single_operand[k].append(engine_components.eval_expression(value1))
                            
                        # else : 
                        #     numerator[k].append("not found adjective in denoinator no sense in making numerator ")
                        #     denominator[k].append("not found adjective")
                    else : single_operand[k].append("operation is missing or erro is json")
                else : single_operand[k].append("string not matched with single operands list")
                    
            else :
                single_operand[k].append("rule is not in json or something is missing")
                numerator[k].append("rule is not in json or something is missing")
                denominator[k].append("rule is not in json or something is missing")
                
        gc.collect()
        single_operand = dict(single_operand)
        numerator = dict(numerator)
        denominator = dict(denominator)
        dataframe["Single_operand"] = dataframe["Measures"].map(single_operand)    
        dataframe["Numerator"] = dataframe["Measures"].map(numerator)
        dataframe["Denominator"] = dataframe["Measures"].map(denominator)
        
        dataframe=dataframe[["Measures","Single_operand","Numerator","Denominator"]]        
        return dataframe
                                     
                
                
                 
                 
                 
                 
                 
        