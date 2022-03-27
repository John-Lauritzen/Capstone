import Database as DB
import Query as Q

def main():
    action = ''
    action = input('Enter ISBN (or done to finish):')
    if action != 'done':
        LCtitle = Q.LCquery(action)
        if LCtitle == 0:
            print('ISBN not found')
            ConfirmedTitle = input('Enter the title of the series:')
        else:
            print(LCtitle)
            ValidTitle = input('Is this the correct title? (y or n):')
            if ValidTitle == 'y':
                ConfirmedTitle = LCtitle
            elif ValidTitle == 'n':
                ConfirmedTitle = input('Enter the title of the series:')
            else:
                print('Invalid input, trying original title.')
                ConfirmedTitle = LCtitle
        MALresults = Q.MALquery(ConfirmedTitle)
        MALtitle = MALresults[0]
        MALtags = MALresults[1:]
        KIresults = Q.KIquery(MALtitle)
        ALresults = Q.ALquery(ConfirmedTitle)
        Volume = int(input('Enter latest owned volume number:'))
        Rating = int(input('Enter rating on a scale from 1-5:'))
        conn = DB.create_connection()
        SeriesID = DB.enter_series(conn, (MALtitle, Volume, Rating))
        DB.tag_entry(conn, SeriesID, MALtags)
        if KIresults != 0:
            DB.tag_entry(conn, SeriesID, KIresults)
        DB.tag_entry(conn, SeriesID, ALresults)
        main()


if __name__ == '__main__':
    main()