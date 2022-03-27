import sqlite3
from sqlite3 import Error

def create_connection():
    '''
    create a database connection to the SQLite database
    :return: Connection object
    '''
    conn = None
    try:
        conn = sqlite3.connect(r"mangalibrary.db")
    except Error as e:
        print(e)
    
    return conn

def create_memory_connection():
    '''
    Create a database connection to a SQLite database in memory
    :return: Connection object
    '''
    conn = None
    try:
        conn = sqlite3.connect(':memory:')
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    '''
    create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    '''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def enter_series(conn, series):
    '''
    Enter a new series into the library table
    :param conn: Connection object
    :param series: Series information-Structue: Title, Currently owned volume, and rating from 1-5
    :return: series id
    '''
    sql = '''INSERT INTO library(title,volume,rating)
              VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()
    return cur.lastrowid

def enter_trending(conn, trending):
    '''
    Enter a new series into the library table
    :param conn: Connection object
    :param trending: List of series trending series titles
    '''
    sql = '''INSERT INTO trending(title)
              VALUES(?)'''
    cur = conn.cursor()
    for title in trending:
        cur.execute(sql, (title,))
        conn.commit()

def tag_entry(conn, seriesid, tags):
    '''
    Method of entry for series tags, preventing duplicates
    :param conn: Connection object
    :param seriesid: ID for series to enter tags for
    :param tags: List of tags to enter
    '''
    for tag in tags:
        CurTags = get_seriestags(conn, seriesid)
        if tag not in CurTags:
            enter_tag(conn, (seriesid, tag))

def enter_tag(conn, tag):
    '''
    Enter a tag for a series
    :param conn: Connection object
    :param tag: Tag for a series-Structure: ID, tag
    '''
    sql = '''INSERT INTO tags(id,tag)
              VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, tag)
    conn.commit()

def update_series_volume(conn, series):
    '''
    Update volume for a series
    :param conn: Connection object
    :param series: Series to update volume on-Structure: New volume, ID
    '''
    sql = '''UPDATE library
            SET volume = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()

def update_series_rating(conn, series):
    '''
    Update rating for a series
    :param conn: Connection object
    :param series: Series to update rating on-Structure: New rating, ID
    '''
    sql = '''UPDATE library
            SET rating = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()

def report_library(conn):
    '''
    List all manga in library
    :param conn: Connection object
    :return: Library list
    '''
    sql = '''SELECT id, title, volume, rating FROM library'''
    cur = conn.cursor()
    cur.execute(sql)
    library = cur.fetchall()

    return library

def report_trending(conn):
    '''
    List all trending items retrieved
    :param conn: Connection object
    :return: Trending list
    '''
    sql = '''SELECT id, title FROM trending'''
    cur = conn.cursor()
    cur.execute(sql)
    library = cur.fetchall()

    return library

def get_seriesID(conn, series):
    '''
    Get the ID of a recorded series
    :param conn: Connection object
    :param series: Title of series
    :return: Series ID
    '''
    sql = '''SELECT id FROM library
            WHERE title = ?'''
    cur = conn.cursor()
    cur.execute(sql, (series,))
    seriesIDraw = cur.fetchall()
    seriesID = seriesIDraw[0][0]

    return int(seriesID)
    
def get_seriestags(conn, series):
    '''
    Get the tags of a recorded series
    :param conn: Connection object
    :param series: ID of the series
    :return: List of tags
    '''
    sql = '''SELECT tag FROM tags
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (series,))
    tagsraw = cur.fetchall()
    tags = list()
    for tag in tagsraw:
        tags.append(tag[0])
        
    return tags

def get_ownedseries(conn):
    '''
    Get a list of all series owned in the library
    :param conn: Connection object
    :return: List of titles
    '''
    sql = '''SELECT title FROM library'''
    cur = conn.cursor()
    cur.execute(sql)
    titlesraw = cur.fetchall()
    titles = list()
    for title in titlesraw:
        titles.append(title[0])

    return titles

def clear_tags(conn, series):
    '''
    Delete all tags for a series
    :param conn: Connection object
    :param series: Series to clear tags from-Structure: ID
    '''
    sql = '''DELETE FROM tags
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()

def clear_database(conn):
    '''
    Delete all from database
    :param conn: Connection object
    '''
    sql = '''DELETE FROM tags'''
    sql2 = '''DELETE FROM library'''
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(sql2)
    conn.commit()

def clear_rec_database(conn):
    '''
    Delete all from database
    :param conn: Connection object
    '''
    sql = '''DELETE FROM tags'''
    sql2 = '''DELETE FROM trending'''
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(sql2)
    conn.commit()

def create_rec_tables(conn):
    '''
    Creates the tables used for processing Recommendations (Should be run against create_memory_connection)
    :param conn: Connection object 
    '''
    sql_create_trending_table = '''CREATE TABLE IF NOT EXISTS trending (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL UNIQUE
                                );'''

    sql_create_tags_table = '''CREATE TABLE IF NOT EXISTS tags (
                                id integer,
                                tag text,
                                PRIMARY KEY (id, tag)
                                FOREIGN KEY (id) REFERENCES library (id)
                            );'''

    create_table(conn, sql_create_trending_table)
    create_table(conn, sql_create_tags_table)

def close_connection(conn):
    '''
    Closes an open SQLite Connection
    :param conn: Connection object
    '''
    conn.close        

def main():

    sql_create_library_table = '''CREATE TABLE IF NOT EXISTS library (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL UNIQUE,
                                    volume interger,
                                    rating interger NOT NULL
                                );'''

    sql_create_tags_table = '''CREATE TABLE IF NOT EXISTS tags (
                                id integer,
                                tag text,
                                PRIMARY KEY (id, tag)
                                FOREIGN KEY (id) REFERENCES library (id)
                            );'''

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        # create library table
        create_table(conn, sql_create_library_table)
        
        # create tags table
        create_table(conn, sql_create_tags_table)

    else:
        print('Error! cannot create the database connection.')

    conn.close

if __name__ == '__main__':
    main()