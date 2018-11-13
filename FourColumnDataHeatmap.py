import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from numba import vectorize

#df = pd.DataFrame(pd.read_csv('all_cal_val.csv')) #this also works most of the times
df = pd.DataFrame(pd.read_csv('all_cal_val.csv'), columns=('longitude','latitude','housing_median_age','total_rooms','total_bedrooms','population','households','median_income','median_house_value'))

x_values = np.array(np.arange(0.0, 10.01, 0.25))
x_values = np.append(x_values, [15.25])

y_values = np.array(np.arange(0.0, 15001.0, 500.0))
y_values = np.append(y_values, [36000.0])

#z_values = np.linspace(0.0, 55.0, num=11+1)
z_values = np.array(np.arange(0.0, 55.01, 5.0))

#@vectorize(['float32(float32, float32, float32, float32)', 'float64(float64, float64, float64, float64)'], target='cuda')
#@vectorize(target='cuda')
def calculate_value(x_values, y_values, z_values, df):
    v_meanvalue = np.full((len(x_values),len(y_values),len(z_values)), 0)
    v_count = np.full((len(x_values),len(y_values),len(z_values)), 0)
    v_sum = np.full((len(x_values),len(y_values),len(z_values)), 0)
    for c in range(0,len(df)-1):
        x=0
        y=0
        z=0
        while x_values[x] < df['median_income'][c]:
            x=x+1
        x=x-1
        while y_values[y] < df['population'][c]:
            y=y+1
        y=y-1
        while z_values[z] < df['housing_median_age'][c]:
            z=z+1
        z=z-1
        v_count[x][y][z]+=1
        v_sum[x][y][z] = v_sum[x][y][z] + df['median_house_value'][c]
        v_meanvalue[x][y][z] = (v_sum[x][y][z]) / (v_count[x][y][z])
    return v_meanvalue

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        #ax.set_title('use scroll wheel to navigate \'housing_median_age\'')

        self.X = X
        rows, cols, self.slices = X.shape
        self.slices=self.slices-1
        self.ind = self.slices//2

        ## matplot / numpy is jumbled up when designating x, y and z axis for 3d and 2d array; so transposing
        self.im = ax.imshow(np.transpose(self.X[:, :, self.ind]))
        self.update()

    def onscroll(self, event):
        #print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        ## matplot / numpy is jumbled up when designating x, y and z axis for 3d and 2d array; so transposing
        self.im.set_data(np.transpose(self.X[:, :, self.ind]))
        ax.set_title('\nUse scroll wheel to navigate \'housing_median_age\' \n Currently showing slice of data for housing_median_age range %s' % z_tick_labels[self.ind])
        self.im.axes.figure.canvas.draw()

fig, ax = plt.subplots(1, 1)

ax.set_xlabel('median_income')
#x_tick_labels = np.append([' '], [ '{0:5.2f} - {1:5.2f}'.format(*bin) for bin in  zip(np.array(x_values)[:-1], np.array(x_values)[1:])])
x_tick_labels = [ '{0:.2f} - {1:.2f}'.format(*bin) for bin in  zip(np.array(x_values)[:-1], np.array(x_values)[1:])]
ax.set_xticks(np.arange(len(x_values)-1))
ax.set_xticklabels(x_tick_labels)
#plt.setp(ax.get_xticklabels(), rotation=90, ha="right", rotation_mode="anchor")
plt.setp(ax.get_xticklabels(), rotation=90)
#fig.autofmt_xdate()

ax.set_ylabel('population')
#y_tick_labels = np.append([' '], [ '{0} - {1}'.format(*bin) for bin in  zip(np.array(y_values)[:-1], np.array(y_values)[1:])])
y_tick_labels = [ '{0} - {1}'.format(*bin) for bin in  zip(np.array(y_values)[:-1], np.array(y_values)[1:])]
ax.set_yticks(np.arange(len(y_values)-1))
ax.set_yticklabels(y_tick_labels)

#z_tick_labels = np.append([' '], [ '{0} - {1}'.format(*bin) for bin in  zip(np.array(z_values)[:-1], np.array(z_values)[1:])])
z_tick_labels = [ '{0} - {1}'.format(*bin) for bin in  zip(np.array(z_values)[:-1], np.array(z_values)[1:])]

#X = np.array(v_meanvalue)
#cv_vec = np.vectorize(calculate_value, otypes=[np.ndarray])
#ValueError: operands could not be broadcast together with shapes (42,) (32,) (12,) (17000,9)
X = np.array(calculate_value(x_values, y_values, z_values, df))
#X = cv_vec(x_values, y_values, z_values, df)
tracker = IndexTracker(ax, X)

fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.gca().invert_yaxis() #so that 0 of y axis starts from bottom
plt.ylim(-0.5, len(y_values)-1.5) #so that no blanck space at the end of y axis
plt.xlim(-0.5, len(x_values)-1.5) #so that no blanck space at the end of y axis
cbar = ax.figure.colorbar(tracker.im, ax=ax)
cbar.ax.set_ylabel(ylabel="median_house_value", rotation=-90, va="bottom")
plt.tight_layout() #so that labels text does not overlap
plt.show()