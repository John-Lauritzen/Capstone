import Database as DB
import Recommendation as RC
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier


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

cv = StratifiedKFold(n_splits=3)

svc = svm.SVC()
nusvc = svm.NuSVC()
lsvc = svm.LinearSVC()
gnb = GaussianNB()
rfc = RandomForestClassifier()
etc = ExtraTreesClassifier()

SVC = cross_val_score(svc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv)
NSVC = cross_val_score(nusvc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv)
LSVC = cross_val_score(lsvc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv)
GNB = cross_val_score(gnb, VectorizedTags.toarray(), LibraryRatings, scoring="accuracy", cv=cv)
RFC = cross_val_score(rfc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv)
ETC = cross_val_score(etc, VectorizedTags, LibraryRatings, scoring="accuracy", cv=cv)

print("For SVC %0.2f accuracy with a standard deviation of %0.2f" % (SVC.mean(), SVC.std()))
print("For NuSVC %0.2f accuracy with a standard deviation of %0.2f" % (NSVC.mean(), NSVC.std()))
print("For LinearSVC %0.2f accuracy with a standard deviation of %0.2f" % (LSVC.mean(), LSVC.std()))
print("For Gaussian NB %0.2f accuracy with a standard deviation of %0.2f" % (GNB.mean(), GNB.std()))
print("For Random Forest Classifier %0.2f accuracy with a standard deviation of %0.2f" % (RFC.mean(), RFC.std()))
print("For Extra Trees Classifier %0.2f accuracy with a standard deviation of %0.2f" % (ETC.mean(), ETC.std()))

#SampleTags = DB.get_seriestags(conn, 3)
#RC.train_fromlibrary()
#print(RC.predict_rating(SampleTags))
