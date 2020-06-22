import pandas as pd
import click
from data_cleaning import data_wrangling
from pos_mapping import pos_tagging_mapping
from etl_pipeline import etl_mapping
from rule_engine import engine
import time
@click.command()
@click.option("--filename", prompt="pls enter the file name")
@click.option("--nsl_rules", prompt="pls enter the file name for rules")
def main(filename, nsl_rules):
    start_time = time.time()
    df=data_wrangling.file_preprocess(filename)
    df=pos_tagging_mapping.grammar_dict_map(df,nsl_rules)
    df=etl_mapping.data_transformation(df)
    df=engine.rules(df)
    df.to_csv("nsl_operands.csv")
    print('{0:.2f}'.format((time.time() - start_time)/60),"mins")
if __name__ == "__main__":
    main(
 
    )