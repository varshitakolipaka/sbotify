import sqlite3


class DB:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path)
        self.cur = self.db.cursor()

    def run_query(self, query):
        self.cur.execute(query)
        return [i[0] for i in self.cur.description], self.cur.fetchall()


sbotify_db = DB('playlist.db')
sbotify_db.cur.execute('''
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

sbotify_db.cur.execute('''
INSERT INTO Playlists(playlist_name, playlist_id)
VALUES
    ('poo','1'),
    ('boo','2'),
    ('voo','3'),
    ('coo','4'),
    ('doo','5'),
    ('soo','6'),
    ('qoo','7')
''')
# sbotify_db.cur.execute('''
# CREATE TABLE Members (member_id VARCHAR, set_playlist VARCHAR)''')
# sbotify_db.cur.execute('''
# CREATE TABLE Playlists (playlist_name VARCHAR, playlist_id VARCHAR)''')

# MEMBERS TABLE


def check_member(member_id):
    col, res = sbotify_db.run_query(f'''
    SELECT EXISTS(SELECT DISTINCT * FROM Members WHERE member_id='{member_id}')''')
    flag = res[0][0]
    return flag


flag1 = check_member('678')
# print(flag1)


def update_set_playlist(member_id, playlist_id):
    sbotify_db.cur.execute(f'''
    UPDATE Members SET set_playlist = '{playlist_id}' WHERE member_id='{member_id}'
     ''')


# PLAYLIST TABLE
# check if playlist exists
def check_playlist(playlist_name):
    col, res = sbotify_db.run_query(f'''
    SELECT EXISTS(SELECT DISTINCT * FROM Playlists WHERE playlist_name='{playlist_name}')''')
    flag = res[0][0]
    return flag


def return_playlist_id(playlist_name):
    if check_playlist(playlist_name) == 1:
        col, res = sbotify_db.run_query(f'''
        SELECT playlist_id FROM Playlists WHERE playlist_name='{playlist_name}'
        ''')
        return res[0][0]
    else:
        return None


flag2 = return_playlist_id('doo')
# def create_playlist
print(flag2)
# Printing the tbale contents
col, res = sbotify_db.run_query("SELECT * FROM Members")
print(res)
col, res = sbotify_db.run_query("SELECT * FROM Playlists")
print(res)

# sbotify_db.db.commit()
