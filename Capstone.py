import Database as DB
import Query as Q
import Recommendation as RC
import pandas as P
import matplotlib.pyplot as plt

ValidMenu = (1, 2, 3, 4, 5, 6)
LibraryHeaders = ['ID', 'Title', 'Volume', 'Ranking']
RecommendationHeaders = ['Series', 'Probability']

def main():
    conn = DB.create_connection()
    print('Welcome to the Manga Library Management System')
    print('Please select from the following options:')
    print('1. Report the current content of the library')
    print('2. Add series to the library')
    print('3. Update the latest volume for a series')
    print('4. Update the rating for a series')
    print('5. Get recommendations based of of the library')
    print('6. Exit')
    Menu = int(input('Please enter the number for an action: '))
    if Menu not in ValidMenu:
        print('Please make a valid selection')
        main()
    elif Menu == 1:
        Library = P.DataFrame(DB.report_library(conn), columns= LibraryHeaders)
        LL = len(Library)
        Lindex = 0
        LLimit = 10
        while LL > 0:
            print(Library.iloc[Lindex:LLimit])
            input('Press enter to continue')
            LL -= 10
            Lindex += 10
            LLimit += 10
        main()
    elif Menu == 2:
        data_entry(conn)
    elif Menu == 3:
        id = input('Enter series ID:')
        volume = input('Enter latest owned volume:')
        DB.update_series_volume(conn, (volume, id))
        print('Series updated.')
        main()
    elif Menu == 4:
        id = input('Enter series ID:')
        rating = input('Enter the new rating:')
        DB.update_series_rating(conn, (rating, id))
        print('Series updated.')
        main()
    elif Menu == 5:
        Recommendations = RC.get_recommendations()
        Titles = list()
        Probability = list()
        for title in Recommendations:
            if title[1] >= 0.7:
                Titles.append(title[0])
                Probability.append(title[1])
        plt.rcdefaults()
        plt.rcParams.update({'figure.autolayout': True})
        plt.style.use('seaborn-muted')
        fig, ax = plt.subplots()
        ax.barh(Titles, Probability)
        labels = ax.get_yticklabels()
        plt.setp(labels, horizontalalignment='left')
        ax.set_xlabel('Probability')
        ax.set_title('Manga recommendations')
        plt.show()
        main()
    elif Menu == 6:
        print('Goodbye and happy reading!')


def data_entry(conn):
    '''
    Process to enter new manga into the library with user input.
    :param conn: Connection object
    '''
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
        SeriesID = DB.enter_series(conn, (MALtitle, Volume, Rating))
        DB.tag_entry(conn, SeriesID, MALtags)
        if KIresults != 0:
            DB.tag_entry(conn, SeriesID, KIresults)
        DB.tag_entry(conn, SeriesID, ALresults)
        data_entry(conn)
    else:
        main()
        

if __name__ == '__main__':
    main()