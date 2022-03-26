import Database as DB
import Recommendation as RC
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import StratifiedKFold, cross_val_score


conn = DB.create_connection()
Library = DB.report_library(conn)
LibraryTags = list()
LibraryRatings = list()
for series in Library:
    formed = RC.prepare_data(DB.get_seriestags(conn, series[0]), series[3])
    LibraryRatings.append(formed[1])
    LibraryTags.append(formed[0])

#print(LibraryTags)

vectorizer = CountVectorizer()
VectorizedTags = vectorizer.fit_transform(LibraryTags)
vectorizer2 = CountVectorizer(analyzer='word', ngram_range=(2, 2))
VectorizedTags2 = vectorizer2.fit_transform(LibraryTags)

cv = StratifiedKFold(n_splits=3)

svc = svm.SVC()
nusvc = svm.NuSVC()
lsvc = svm.LinearSVC()


#print('SVC: ', cross_val_score(svc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv))
#print('SVC V2: ', cross_val_score(svc, VectorizedTags2, LibraryRatings, scoring="accuracy", cv=cv))
#print('NuSVC: ', cross_val_score(nusvc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv))
#print('NuSVC V2: ', cross_val_score(nusvc, VectorizedTags2, LibraryRatings, scoring="accuracy", cv=cv))
#print('Linear SVC: ', cross_val_score(lsvc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv))
#print('Linear SVC V2: ', cross_val_score(lsvc, VectorizedTags2, LibraryRatings, scoring="accuracy", cv=cv))

SampleTags = DB.get_seriestags(conn, 3)
RC.train_fromlibrary()
print(RC.predict_rating(SampleTags))
