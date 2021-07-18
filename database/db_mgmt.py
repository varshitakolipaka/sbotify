import sqlite3


class DB:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path)
        self.cur = self.db.cursor()

    def run_query(self, query):
        self.cur.execute(query)
        return [i[0] for i in self.cur.description], self.cur.fetchall()


playlist_db = DB('playlist.db')
# playlist_db.cur.execute('''
# CREATE TABLE Members (member_id VARCHAR, set_playlist VARCHAR)''')
playlist_db.cur.execute('''
INSERT INTO Members(member_id, set_playlist)
VALUES
    ('012','o'),
    ('123','a'),
    ('234','b'),
    ('234','c'),
    ('345','d'),
    ('456','e'),
    ('567','f'),
    ('678','g')
''')
def check_member(member_id):
    col, res = playlist_db.run_query(f'''
    SELECT EXISTS(SELECT DISTINCT * FROM Members WHERE member_id='{member_id}')''')
    flag = res[0][0]
    return flag
flag1=check_member('678')
print(flag1)
def update_set_playlist(member):
    col, res = playlist_db.run_query(f'''
    UPDATE Members SET set_playlist = '{playlist_name}' WHERE member_id='{member_id}'
     ''')

update_set_playlist = 

# col, res = playlist_db.run_query("SELECT * FROM Members")
# print(res)

# playlist_db.db.commit()
