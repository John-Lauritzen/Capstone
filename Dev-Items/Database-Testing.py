import Database as DB

conn = DB.create_connection()

DB.clear_database(conn)

Series = ('Overlord', 8, 5)
SeriesID = DB.enter_series(conn, Series)
Tag1 = (SeriesID, 'Isekai')
Tag2 = (SeriesID, 'Game')
DB.enter_tag(conn, Tag1)
DB.enter_tag(conn, Tag2)
    
SeriesUpdate = (9, 1)
DB.update_series_volume(conn, SeriesUpdate)

Series = ('Berserk', 9, 4)
SeriesID = DB.enter_series(conn, Series)
Tag1 = (SeriesID, 'Fantasy')
Tag2 = (SeriesID, 'Revenge')
DB.enter_tag(conn, Tag1)
DB.enter_tag(conn, Tag2)

print(DB.report_library(conn))
SeriesID = DB.get_seriesID(conn, ('Overlord'))
print(DB.get_seriestags(conn, SeriesID))