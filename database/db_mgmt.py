import sqlite3


class DB:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path)
        self.cur = self.db.cursor()

    def run_query(self, query):
        self.cur.execute(query)
        return [i[0] for i in self.cur.description], self.cur.fetchall()
    def make_tables(self):
        self.cur.execute('''
        CREATE TABLE Members(member_id TEXT, set_playlist TEXT)
        ''')
        self.cur.execute('''
        CREATE TABLE Playlists(playlist_name TEXT, playlist_id TEXT, created_by TEXT)
        ''')
        self.db.commit()

    def insert_members(self, member_id):
        self.cur.execute(f'''
    INSERT INTO Members(member_id, set_playlist) VALUES ('{member_id}', '0')
    ''')

    def insert_playlist(self, playlist_name, playlist_id, member_id):
        self.cur.execute(f'''
        INSERT INTO Playlists VALUES ('{playlist_name}','{playlist_id}','{member_id}')
        ''')

    def return_set_playlists(self, member_id):
        if self.check_member(member_id) == 1:
            col, res = self.run_query(f'''
            SELECT * FROM Members WHERE member_id='{member_id}'
            ''')
            col2, res2 = self.run_query(f'''
            SELECT playlist_name FROM Playlists WHERE playlist_id='{res[0][1]}'
            ''')
            return (res2[0][0], res[0][1])
        else:
            return (0, 0)

    def check_member(self, member_id):
        col, res = self.run_query(f'''
        SELECT EXISTS(SELECT DISTINCT * FROM Members WHERE member_id='{member_id}')''')
        flag = res[0][0]
        return flag

    def update_set_playlist(self, member_id, playlist_id):
        self.cur.execute(f'''
        UPDATE Members SET set_playlist = '{playlist_id}' WHERE member_id='{member_id}'
        ''')
    # PLAYLIST TABLE
    # check if playlist exists

    def check_playlist(self, playlist_name):
        col, res = self.run_query(f'''
        SELECT EXISTS(SELECT DISTINCT * FROM Playlists WHERE playlist_name='{playlist_name}')''')
        flag = res[0][0]
        return flag

    def return_playlist_id(self, playlist_name):
        if self.check_playlist(playlist_name) == 1:
            col, res = self.run_query(f'''
            SELECT playlist_id FROM Playlists WHERE playlist_name='{playlist_name}'
            ''')
            return res[0][0]
        else:
            return None

    def rename_playlist(self, member_id, new_name):
        if self.check_member(member_id) == 1:
            col, res = self.run_query(f'''
            SELECT * FROM Members WHERE member_id='{member_id}'
            ''')
            playlist_id = res[0][1]
            print(res)
            self.cur.execute(
                f'''UPDATE Playlists SET playlist_name= '{new_name}' WHERE playlist_id='{playlist_id}'
                ''')

    def print_db(self, table_name):
        col, res = self.run_query(f"SELECT * FROM {table_name}")
        print(col)
        print(res)

    def clean_db(self):
        self.delete_all_entries('Members')
        self.delete_all_entries('Playlists')

    def delete_all_entries(self, table_name):
        self.cur.execute(f"DELETE FROM {table_name}")
        self.db.commit()

    def list_all_playlists(self, author_id):
        if author_id == 'all':
            col, res = self.run_query(f'''
            SELECT * FROM Playlists
            ''')
        else:
            col, res = self.run_query(f'''
            SELECT * FROM Playlists WHERE created_by='{author_id}'
            ''')
        if len(res) == 0:
            return 0
        return res

    def close_db(self):
        self.db.close()


sbotify_db = DB('./database/playlists.db')

# sbotify_db.make_tables()
# sbotify_db.clean_db()
# sbotify_db.insert_members('1234')
# sbotify_db.insert_playlist('test', '1234', 'gaur')
# sbotify_db.update_set_playlist('1234', 'name of thingy')
# sbotify_db.print_db('Members')
# sbotify_db.print_db('Playlists')
# flag1 = sbotify_db.check_member('123')
# flag2 = sbotify_db.return_playlist_id('doo')
# # def create_playlist
# print(flag1)
# print(flag2)
# Printing the table contents
# sbotify_db.cur.execute('''ALTER TABLE playlists
# ADD created_by VARCHAR;''')
# sbotify_db.db.commit()
