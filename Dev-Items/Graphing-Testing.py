import matplotlib.pyplot as plt
import Recommendation as RC
import Database as DB

conn = DB.create_connection()
RC.train_fromlibrary()
Library = DB.report_library(conn)
Titles = list()
Tags = list()
for title in Library:
   Titles.append(title[1])
   Tags.append(DB.get_seriestags(conn, title[0]))
#print(Titles, Tags)
Titles10 = list()
Ratings10 = list()
for i in range(10):
    Titles10.append(Titles[i])
    Ratings10.append(RC.predict_rating(Tags[i])[1])
#print(Titles10, Ratings10)

plt.rcdefaults()
plt.rcParams.update({'figure.autolayout': True})
plt.style.use('seaborn-muted')
fig, ax = plt.subplots()
ax.barh(Titles10, Ratings10)
labels = ax.get_yticklabels()
plt.setp(labels, horizontalalignment='left', position = (.03, 0))
#print(plt.getp(labels))
ax.set_xlabel('Probability')
ax.set_title('Manga recommendations')

plt.show()

'''
['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
'''