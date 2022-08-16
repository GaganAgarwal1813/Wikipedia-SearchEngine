import pandas as pd

df = pd.read_csv("./temp/title0.tsv", names = ["id","title"], lineterminator='\n', sep="\t", index_col=False)
print(df.head(10))