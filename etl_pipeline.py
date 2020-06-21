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