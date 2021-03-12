import sys
import re
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


#--------------------------------------------------
# plotting GPA from roary as a heatmap


def generate_clean_gene_set(GPA):
    GPA_filter = {}
    for row in GPA.itertuples():
        search = re.split(r"_\d+|\d+$", row[0])
        gene = search[0]
        if gene in GPA_filter.keys():
            GPA_filter[gene] = np.maximum(GPA_filter[gene], row[1:])
        else:
            GPA_filter[gene] = row[1:]
    return GPA_filter


def similarity_score(colA, colB):
    result = np.where(colA == colB, True, False).sum()
    perc = (result / len(colA)) * 100
    return result, perc


def plot(fp):
    gpa = pd.read_table(fp, index_col=0)
    tidy = generate_clean_gene_set(gpa)
    tidy_df = pd.DataFrame.from_dict(tidy, orient="index", columns=gpa.columns)

    df = pd.DataFrame(index=gpa.columns, columns=gpa.columns)
    df = df.fillna(value=0.0)
    for colA, colB in product(df.index, df.columns):
        if df.at[colB, colA] != 0.0:
            continue
        _, perc = similarity_score(tidy_df[colA], tidy_df[colB])
        df.at[colA, colB] = perc
        df.at[colB, colA] = perc

    sns.clustermap(df, cmap="mako")
    plt.show()


if __name__ == "__main__":
    plot(sys.argv[1])