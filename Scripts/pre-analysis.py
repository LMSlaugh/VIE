import pandas as pd
import numpy as np
import seaborn as sns

#df = sns.load_dataset("iris")



sns.set(style="ticks")
fig = sns.pairplot(df, hue="species")
fig.savefig("Figures\\pairs.png", format='png', bbox_inches='tight')

stopgap = "thisisastopgap"