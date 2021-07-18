import sqlite3


class DB:
    def __init__(self, path):
        self.path = path
        self.db = sqlite3.connect(self.path)
        self.cur = self.db.cursor()

    def run_query(self, query):
        self.cur.execute(query)
        return [i[0] for i in self.cur.description], self.cur.fetchall()

    def insert_members(self, member_id):
        self.cur.execute(f'''
    INSERT INTO Members(member_id, set_playlist) VALUES ('{member_id}', '0')
    ''')

    def insert_playlist(self, playlist_name, playlist_id):
        self.cur.execute(f'''
        INSERT INTO Playlists VALUES ('{playlist_name}','{playlist_id}')
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

    def print_db(self, table_name):
        col, res = self.run_query(f"SELECT * FROM {table_name}")
        print(res)


sbotify_db = DB('./database/playlist.db')
# delete table Members


# def delete_all_entries(table_name):
#     sbotify_db.cur.execute(f"DELETE FROM {table_name}")
#     sbotify_db.db.commit()

# delete_all_entries('Members')
# delete_all_entries('Playlists')
# sbotify_db.insert_members('1234')
# sbotify_db.insert_playlist('test', '1234')
# sbotify_db.update_set_playlist('1234', 'name of thingy')
# sbotify_db.print_db('Members')
# sbotify_db.print_db('Playlists')
# flag1 = sbotify_db.check_member('123')
# flag2 = sbotify_db.return_playlist_id('doo')
# # def create_playlist
# print(flag1)
# print(flag2)
# Printing the table contents
