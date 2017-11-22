import sqlite3 as sql


class Database(object):
    conn = sql.connect('../../game.db')
    conn.row_factory = sql.Row

    def __init__(self):
        pass

    def def_table(self, table):
        c = self.conn.cursor()
        c.execute("PRAGMA table_info("+table+")")
        ret_table = c.fetchall()
        c.close()
        return ret_table

    def get_table(self, table):
        c = self.conn.cursor()
        c.execute("Select * from "+table+" order by id asc")
        ret_table = c.fetchall()
        c.close()
        return ret_table

    def get_one(self, query, params):
        c = self.conn.cursor()
        c.execute(query, params)
        ret_row = c.fetchone()
        c.close()
        return ret_row

    def get_row(self, table, r_id):
        return self.get_one("select * from "+table+" where id=?", r_id)

    def get_tup(self, query, params):
        row = self.get_one(query, params)
        return row[0], row[1]

    def save(self, query, params):
        c = self.conn.cursor()
        c.execute(query, params)
        c.close()
        return c.lastrowid