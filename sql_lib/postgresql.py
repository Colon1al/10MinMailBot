import psycopg2 as pgsql
 
def connect(dbname, user, password, address):
    """

    """
    conn = pgsql.connect(dbname='database', user='db_user', 
                            password='mypassword', host='localhost')
    cursor = conn.cursor()
    return (conn, cursor)