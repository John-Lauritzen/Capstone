import Database as DB
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer

clf = svm.NuSVC(probability=True)
vectorizer = CountVectorizer()

def prepare_data(tags, rating):
    '''
    Format tags and rating of a series for use in ML training
    :param tags: List of tags for the series
    :param rating: Series rating on a scale from 1-5
    :return: Combined tags[0] and high(1) or low(0) rating[1] in a list
    '''
    if rating >= 3:
        Rating = 1
    else:
        Rating = 0
    Tags = ' '.join(tags)
    return Tags, Rating

def train_fromlibrary():
    '''
    Takes the full current library and trains the classifier using it.
    '''
    conn = DB.create_connection()
    Library = DB.report_library(conn)
    LibraryTags = list()
    LibraryRatings = list()
    for series in Library:
        Formed = prepare_data(DB.get_seriestags(conn, series[0]), series[3])
        LibraryRatings.append(Formed[1])
        LibraryTags.append(Formed[0])

    VectorizedTags = vectorizer.fit_transform(LibraryTags)

    clf.fit(VectorizedTags, LibraryRatings)

def predict_rating(tags):
    '''
    Provides prediction on if a series with the specific tags would receive a high or low rating
    :param tags: List of tags for the series
    :return: Prediction of low(0) or high(1) rating along with Probability values
    '''
    FormedTags = prepare_data(tags, 0)
    VectoredTags = vectorizer.transform([FormedTags[0]])
    Prediction = clf.predict(VectoredTags)
    Probability = clf.predict_proba(VectoredTags)
    if Prediction == 1:
        return Prediction, Probability[0][1]
    else:
        return Prediction, Probability[0][0]

