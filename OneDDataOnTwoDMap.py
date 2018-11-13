import pandas as pd
import geopandas
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib import cm
from collections import OrderedDict

#df = pd.DataFrame(pd.read_csv('ggl.csv'))
df = pd.DataFrame(pd.read_csv('cal_val.csv'))
df['Coordinates'] = list(zip(df.longitude, df.latitude))
df['Coordinates'] = df['Coordinates'].apply(Point)
gdf = geopandas.GeoDataFrame(df, geometry='Coordinates')
print(gdf.head())

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black')
#gdf.plot(column='population', ax=ax, cmap=plt.get_cmap('cool'), vmin=500, vmax=5000)
gdf.plot(column='median_house_value', ax=ax, cmap=plt.get_cmap('coolwarm'))
plt.show()