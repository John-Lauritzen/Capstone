from contextlib import nullcontext
import Query as Q
import Database as DB

LCtitle = Q.LCquery('9781648279331')
print(LCtitle)
MALresults = Q.MALquery(LCtitle)
MALtitle = MALresults[0]
MALtags = MALresults[1:]
print(MALtitle)
KIresults = Q.KIquery(MALtitle)
ALresults = Q.ALquery(MALtitle)
print(MALtags)
print(KIresults)
print(ALresults)
