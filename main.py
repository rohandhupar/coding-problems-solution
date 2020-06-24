import pandas as pd
import click
from data_cleaning import data_wrangling
from pos_mapping import pos_tagging_mapping
from etl_pipeline import etl_mapping
# from rule_engine import engine
from rule_engine_mod import engine 
import time
@click.command()
@click.option("--filename", prompt="pls enter the file name")
@click.option("--nsl_rules", prompt="pls enter the file name for grammar rules")
@click.option("--rule_engine", prompt="pls enter the file name for rule engine")

def main(filename, nsl_rules,rule_engine):
    start_time = time.time()
    df=data_wrangling.file_preprocess(filename)
    df=pos_tagging_mapping.grammar_dict_map(df,nsl_rules)
    df=etl_mapping.data_transformation(df)
    df=engine.rules(df,rule_engine)
    input_file_changed=df[df[["Single_operand","Numerator","Denominator"]].isnull().all(axis=1)]
    input_file_changed.to_excel(filename)
    output_file_changed= df[df[["Single_operand","Numerator","Denominator"]].notna().any(axis=1)]
    output_file_changed.to_csv("output_file.csv")
    print("\n","total number of rows: ",df.shape[0],"\n")
    print("input file still left with :",input_file_changed.shape[0]," number of rows","\n")
    print("output on number of rows :",output_file_changed.shape[0],"\n")
    print('{0:.2f}'.format((time.time() - start_time)/60),"mins")
if __name__ == "__main__":
    main(
 
    )