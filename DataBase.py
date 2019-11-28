import sqlite3
import Game


class HistoryDataBase():
    def connect(self):
        self.con = sqlite3.connect('historydb.db')

    def add_item(self, attemps=0, complexity='Легкий', time=0):
        cur = self.con.cursor()
        cur.execute('''INSERT INTO history_table VALUES (?, ?, ?)''', (attemps, complexity, time,))
        self.con.commit()
    
    def get_all(self):
        cur = self.con.cursor()
        cur.execute('''SELECT * FROM history_table''')
        return cur
    
    def get_rows_count(self):
        cur = self.con.cursor()
        return cur.execute('''SELECT COUNT(*) FROM history_table''').fetchone()[0]
    
    def action_of_clear_history(self):
        cur = self.con.cursor()
        cur.execute('''DELETE FROM history_table''')
        self.con.commit()

    
    def close(self):
        self.con.close()