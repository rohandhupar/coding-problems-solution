import pandas as pd
from collections import defaultdict
import gc

class etl_mapping:
    @staticmethod
    def data_transformation(dataframe):
        """reads the dataframe and transformed the grammar chunks so that they can parse into rule engine


        Args:
            dataframe (pd.dataframe): takes dataframe consists of nouns and verbs chunks and transforms
                                their data structure from list of tuples to list.

        Returns:
            dataframe (pd.dataframe): cleanned and preprocessed dataframe
        """
        nouns = defaultdict(list)
        verbs = defaultdict(list)
        for i,j,k in zip(dataframe["Measures"],dataframe["Nouns_chunks"],dataframe["Verbs_chunks"]):
            if "percentage of" in i:
                for z in j[1:]:
                    nouns[i].append(str(z))
                if str(k) != "nan":
                    for h in k:
                        verbs[i].append(h[0])
            else :
                pass 
        nouns = dict(nouns)
        verbs = dict(verbs)
        dataframe["Nouns_chunks"] = dataframe["Measures"].map(nouns)
        dataframe["Verbs_chunks"] = dataframe["Measures"].map(verbs)

        gc.collect()
        return dataframe