import pandas as pd
import numpy as np
from collections import defaultdict
import gc

class data_wrangling:
    @staticmethod
    def file_preprocess(filename): 
        """
        read the file and preprocess it

        Args:
            file_name (str): takes file name

        Returns:
           dataframe (pd.dataframe) : cleanned dataframe
        """
        df = pd.read_excel(filename,sheet_name="Single_Operator")
        new_df = df.copy()
        new_df = new_df.replace(np.nan, "", regex=True)
        new_df.replace(",", "_", regex=True, inplace=True)
        return new_df
        