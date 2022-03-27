import Query as Q
import Database as DB
import Recommendation as RC

'''LCtitle = Q.LCquery('9781648279331')
print(LCtitle)
MALresults = Q.MALquery(LCtitle)
MALtitle = MALresults[0]
MALtags = MALresults[1:]
print(MALtitle)
KIresults = Q.KIquery(MALtitle)
ALresults = Q.ALquery(MALtitle)
print(MALtags)
print(KIresults)
print(ALresults)'''

'''conn = DB.create_connection()

print(DB.get_ownedseries(conn))'''

Trending = Q.get_trending()

conn = DB.create_memory_connection()
DB.create_rec_tables(conn)
DB.enter_trending(conn, Trending)
TrendingList = DB.report_trending(conn)
for title in TrendingList:
    MALresults = Q.MALquery(title[1])
    MALtitle = MALresults[0]
    MALtags = MALresults[1:]
    KIresults = Q.KIquery(MALtitle)
    ALresults = Q.ALquery(title[1])
    DB.tag_entry(conn, title[0], MALtags)
    if KIresults != 0:
        DB.tag_entry(conn, title[0], KIresults)
    if ALresults != 0:
        DB.tag_entry(conn, title[0], ALresults)

RC.train_fromlibrary()

for title in TrendingList:
    Tags = DB.get_seriestags(conn, title[0])
    print(title[1], RC.predict_rating(Tags))

