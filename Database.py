import sqlite3
from sqlite3 import Error

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(r"mangalibrary.db")
        print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def enter_series(conn, series):
    """
    Enter a new series into the library table
    :param conn: Connection object
    :param series: Series information-Structue: Title, Currently owned volume, and rating from 1-5
    :return: series id
    """
    sql = ''' INSERT INTO library(title,volume,rating)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()
    return cur.lastrowid

def enter_tag(conn, tag):
    """
    Enter a tag for a series
    :param conn: Connection object
    :param tag: Tag for a series-Structure: ID, tag
    """
    sql = ''' INSERT INTO tags(id,tag)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, tag)
    conn.commit()

def update_series_volume(conn, series):
    """
    Update volume for a series
    :param conn: Connection object
    :param series: Series to update volume on-Structure: New volume, ID
    """
    sql = ''' UPDATE library
            SET volume = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()

def update_series_rating(conn, series):
    """
    Update rating for a series
    :param conn: Connection object
    :param series: Series to update rating on-Structure: New rating, ID
    """
    sql = ''' UPDATE library
            SET rating = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()

def clear_tags(conn, series):
    """
    Delete all tags for a series
    :param conn: Connection object
    :param series: Series to clear tags from-Structure: ID
    """
    sql = ''' DELETE FROM tags
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, series)
    conn.commit()

def clear_database(conn):
    """
    Delete all from database
    :param conn: Connection object
    """
    sql = ''' DELETE FROM tags'''
    sql2 = '''DELETE FROM library'''
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(sql2)
    conn.commit()    

def main():

    sql_create_library_table = """ CREATE TABLE IF NOT EXISTS library (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL UNIQUE,
                                        volume interger,
                                        rating interger NOT NULL
                                    ); """

    sql_create_tags_table = """CREATE TABLE IF NOT EXISTS tags (
                                    id integer,
                                    tag text,
                                    PRIMARY KEY (id, tag)
                                    FOREIGN KEY (id) REFERENCES library (id)
                                );"""

    # create a database connection
    conn = create_connection()

    # create tables
    if conn is not None:
        # create library table
        create_table(conn, sql_create_library_table)
        
        # create tags table
        create_table(conn, sql_create_tags_table)

    else:
        print("Error! cannot create the database connection.")

    conn.close

if __name__ == '__main__':
    main()