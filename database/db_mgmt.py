import sqlite3

# DB organisation: playlist_name, plaulist_id, created_by, view, edit


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
        CREATE TABLE Playlists(playlist_name TEXT, playlist_id TEXT, created_by TEXT,view TEXT, edit TEXT) )
        ''')
        self.db.commit()

    def add_column(self, table_name, column_name):
        self.cur.execute(
            f'''ALTER TABLE {table_name} ADD COLUMN '{column_name}' TEXT''')
        self.db.commit()

    def insert_members(self, member_id):
        self.cur.execute(f'''
    INSERT INTO Members(member_id, set_playlist) VALUES ('{member_id}', '0')
    ''')

    def insert_playlist(self, playlist_name, playlist_id, member_id):
        self.cur.execute(f'''
        INSERT INTO Playlists VALUES ('{playlist_name}','{playlist_id}','{member_id}','public','unlock')
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

    def return_playlist_settings(self, playlist_id):
        col, res = self.run_query(f'''
        SELECT * FROM Playlists WHERE playlist_id='{playlist_id}'
        ''')
        try:
            return (res[0][2], res[0][3], res[0][4])
        except:
            None

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

    def list_all_playlists(self, command_author_id, author_id):
        if author_id == 'all':
            col, res = self.run_query(f'''
            SELECT * FROM Playlists 
            WHERE view='public'
            ''')
        elif command_author_id != author_id:
            col, res = self.run_query(f'''
            SELECT * FROM Playlists 
            WHERE created_by='{author_id}' 
            AND view='public'
            ''')
        else:
            col, res = self.run_query(f'''
            SELECT * FROM Playlists 
            WHERE created_by='{author_id}'
            ''')
        if len(res) == 0:
            return 0
        return res

    def set_edit_settings(self, command, member_id, playlist_id):
        if self.check_member(member_id) == 1:
            col, res = self.run_query(f'''
            SELECT * FROM Members WHERE member_id='{member_id}'
            ''')
            playlist_id = res[0][1]
            print(res)
            col, res = self.run_query(f'''
                SELECT created_by FROM Playlists WHERE playlist_id='{playlist_id}'
            ''')
            if res[0][0] == member_id:
                self.cur.execute(
                    f'''UPDATE Playlists SET edit='{command}' WHERE playlist_id='{playlist_id}'
                    ''')
                return 1
            else:
                return 0

    def set_view_settings(self, command, member_id, playlist_id):
        if self.check_member(member_id) == 1:
            col, res = self.run_query(f'''
            SELECT * FROM Members WHERE member_id='{member_id}'
            ''')
            playlist_id = res[0][1]
            print(res)
            col, res = self.run_query(f'''
                SELECT created_by FROM Playlists WHERE playlist_id='{playlist_id}'
            ''')
            if res[0][0] == member_id:
                self.cur.execute(
                    f'''UPDATE Playlists SET view= '{command}' WHERE playlist_id='{playlist_id}'
                    ''')
                return 1
            else:
                return 0

    def close_db(self):
        self.db.close()


sbotify_db = DB('./database/playlists.db')

# update playlists and set al view to public
# sbotify_db.cur.execute(f'''UPDATE Playlists SET edit = 'unlock' ''')
# sbotify_db.cur.execute(f'''UPDATE Playlists SET view = 'public' ''')
# sbotify_db.print_db('Playlists')
# sbotify_db.db.commit()
# sbotify_db.add_column('Playlists','view')
# sbotify_db.add_column('Playlists', 'edit')

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
