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