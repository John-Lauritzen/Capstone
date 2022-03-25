from asyncio.windows_events import NULL
from os import kill
from tracemalloc import stop
import Database as DB
import Query as Q

def tag_entry(conn, seriesid, tags):
    for tag in tags:
        CurTags = DB.get_seriestags(conn, seriesid)
        if tag not in CurTags:
            DB.enter_tag(conn, (seriesid, tag))

def main():
    action = ''
    action = input('Enter ISBN (or done to finish):')
    if action != 'done':
        LCtitle = Q.LCquery(action)
        if LCtitle == 0:
            print('ISBN not found')
        else:
            print(LCtitle)
            MALresults = Q.MALquery(LCtitle)
            MALtitle = MALresults[0]
            MALtags = MALresults[1:]
            KIresults = Q.KIquery(MALtitle)
            ALresults = Q.ALquery(MALtitle)
            Volume = int(input('Enter latest owned volume number:'))
            Rating = int(input('Enter rating on a scale from 1-5:'))
            conn = DB.create_connection()
            SeriesID = DB.enter_series(conn, (MALtitle, Volume, Rating))
            tag_entry(conn, SeriesID, MALtags)
            if KIresults != 0:
                tag_entry(conn, SeriesID, KIresults)
            tag_entry(conn, SeriesID, ALresults)
        main()


if __name__ == '__main__':
    main()