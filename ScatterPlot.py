import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
df = pd.DataFrame(pd.read_csv('all_cal_val.csv'), columns=('longitude','latitude','housing_median_age','total_rooms','total_bedrooms','population','households','median_income','median_house_value'))
print(df.corr())
scatter_matrix(df)
plt.show()
