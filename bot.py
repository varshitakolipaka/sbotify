import os
import json
from track import Track
from requests.api import get
from authtoken import get_access_token
from dotenv.main import dotenv_values
from spotifyclient import SpotifyClient
from playlist import Playlist
from database.db_mgmt import sbotify_db
import discord
from createplaylist import main
from commands_parser import *
from dotenv import load_dotenv
load_dotenv()
spotify_client = SpotifyClient('dummy token',
                               os.getenv("SPOTIFY_USER_ID"))
# bot connect
client = discord.Client()
# this variable stores id of an output channel, you can have many variables corresponding to different channels
out_channel = 'default out channel'

prefix = ['!']

# list of playlists
playlists = []
# event refers to any new,.. well .... event xD, like sending a message,a reaction, a reply, a bot joining etc
members = []
personal_playlist = []
motor_functions = [0]


def get_command_help():
    return f'''
    All commands are preceded by a !
  - `{prefix[0]}help` to view help regarding the commands

  - `{prefix[0]}join` to join the userbase. This is required the first time you use the bot. 

  - `{prefix[0]}set` <playlist name> to set current playlist to <playlist name>. You will be prompted to add <playlist name> if it doesn't exist.
  
  - `{prefix[0]}show` to show current set playlist.
  
  - `{prefix[0]}add <song name>` to add a song to the set playlist.

  - `{prefix[0]}list` to list your playlist.

  - `{prefix[0]}list<number>` to list playlists on page number <number>.

  - `{prefix[0]}rename <new_name>` to rename the set playlist to <new_name>

  - `{prefix[0]}describe <description>` to add a describe the set playlist to the specified description.

    '''


@client.event
# new event
async def on_ready():
    f = open("prefix.json", "r")
    var = json.load(f)
    prefix[0] = var["prefix"]
    f.close()
    # sbotify_db.print_db('Playlists')
    # sbotify_db.print_db('Members')
    # output_channel object holds the info of that channel, whos id is provided
    output_channel = client.get_channel(out_channel)
    # code to send message is
    await output_channel.send("Bring yourself back online, Dolores.")
    # print('====================================================')
    # print(spotify_client._authorization_token)
    # print('====================================================')
    # print("bot started")


@client.event
async def on_message(message):
    try:
        url = f"https://api.spotify.com/v1/search?q=hello&type=track&limit=1&offset=0"
        response = spotify_client._place_get_api_request(url)
        response_json = response.json()
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                  track in response_json["tracks"]["items"]]
    except:
        spotify_client._authorization_token = get_access_token()
    output_channel = message.channel
    # print(motor_functions)
    input_mssg = message.content  # message.content is the string of that message
    if input_mssg.lower() == "show prefix" and (message.author.id == 'badmin1' or message.author.id == 'badmin2'):
        await output_channel.send(f"Prefix is : {prefix[0]}")
    if input_mssg.lower() == 'freeze all motor functions' and (message.author.id == 'badmin1' or message.author.id == 'badmin2'):
        motor_functions[0] = 1
    if input_mssg.lower() == 'bring yourself back online' and (message.author.id == 'badmin1' or message.author.id == 'badmin2'):
        motor_functions[0] = 0
    if input_mssg[0] == prefix[0] and motor_functions[0] == 0:
        mssg = input_mssg.split(" ", 1)
        command = mssg[0][1:len(mssg[0])]
        if (sbotify_db.check_member(message.author.id) == 0) and (command != 'join') and (command != 'help'):
            myEmbed = discord.Embed(
                title="Error", description=f"Uh Oh, you are not yet part of the clan\n Use `{prefix[0]}join` to be a part of Sbotify family!")
            await output_channel.send(embed=myEmbed)
        elif command == 'print':
            print(message.content)
        elif is_command_show(command):
            playlist_name, playlist_id = sbotify_db.return_set_playlists(
                str(message.author.id))
            author, view, edit = sbotify_db.return_playlist_settings(
                playlist_id)
            no_of_songs = spotify_client.get_total_songs(playlist_id)
            addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
            myEmbed = discord.Embed(
                title="Current set playlist", description=f"[{playlist_name}]({addingurl})\n Created by: <@!{author}>\n Number of songs: {no_of_songs}")
            await output_channel.send(embed=myEmbed)
        elif is_command_help(command):
            myEmbed = discord.Embed(
                title="Help", description=get_command_help())
            await output_channel.send(embed=myEmbed)
        elif is_command_change_prefix(command) and (message.author.id == 'badmin1' or message.author.id == 'badmin2'):
            prefix[0] = mssg[1]
            f = open("prefix.json", "w")
            f.write(json.dumps({"prefix": prefix[0]}))
            f.close()
        elif is_command_list(command):
            page = 0
            if(command == "list"):
                page = 1
            else:
                try:
                    page = int(command[4:])
                    # print(page)
                except:
                    myEmbed = discord.Embed(
                        title="Error", description=f"This is not a recognized command.\n Try `{prefix[0]}help` to see all commands")
                    await output_channel.send(embed=myEmbed)
                    return
            try:
                query = str(mssg[1])
                if query.startswith('<@!') and query.endswith('>'):
                    query = query[3:]
                    query = query[:len(query) - 1]
                ret_val = sbotify_db.list_all_playlists(
                    message.author.id, query)
            except:
                ret_val = sbotify_db.list_all_playlists(
                    message.author.id, message.author.id)
            if ret_val == 0:
                myEmbed = discord.Embed(
                    title="No Playlists", description=f'''Uh Oh, there aren't any playlists created by this author\n Use `{prefix[0]}set <name>` to create and set playlists\n
                    Use `{prefix[0]}help` to see all commands.''')
                await output_channel.send(embed=myEmbed)
            else:
                # discord embed to list all values of ret_val
                playlist_len = ret_val.__len__()
                # print(playlist_len)
                if(playlist_len <= (page-1)*10 or page <= 0):
                    myEmbed = discord.Embed(
                        title="Page Doesn't Exist", description=f"There are only {int(playlist_len/10) + 1} Pages.\n Try `{prefix[0]}help` to see all commands")
                    await output_channel.send(embed=myEmbed)
                    return
                send_message = ''
                # print("till here")
                for i in ret_val:
                    if ret_val.index(i) < (page-1)*10:
                        continue
                    if ret_val.index(i) >= page*10:
                        break
                    # no_of_songs = spotify_client.get_total_songs(i[1])
                    send_message += f'''[**{ret_val.index(i)+1}. {i[0]}**](https://open.spotify.com/playlist/{i[1]})\nCreated by: <@!{i[2]}>\n'''
                myEmbed = discord.Embed(
                    title="Playlists", description=f"{send_message}Page: {page} of {int(playlist_len/10) + 1}")
                await output_channel.send(embed=myEmbed)

        elif is_command_add(command):
            try:
                query = mssg[1]
                playlist_name, playlist_id = sbotify_db.return_set_playlists(
                    str(message.author.id))
                author, view, edit = sbotify_db.return_playlist_settings(
                    playlist_id)
                if edit == "lock" and str(message.author.id) != str(author):
                    myEmbed = discord.Embed(
                        title="Error", description=f'''This playlist is locked. Cannot modify a locked playlist.
                            ''')
                    await output_channel.send(embed=myEmbed)
                else:
                    if(playlist_id == '0'):
                        await output_channel.send("You have no playlists set")
                    elif(spotify_client.check_valid_url(query) == 1):
                        spotify_client.add_url_to_playlist(query, playlist_id)
                    else:

                        addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                        added_song = main(query, addingurl,
                                          spotify_client._authorization_token)
                        if(added_song == None):
                            myEmbed = discord.Embed(
                                title="Error", description=f"Couldn't find the song. Try to modify the search query.")
                            await output_channel.send(embed=myEmbed)
                        else:
                            song_url = f'https://open.spotify.com/track/{added_song.id}'
                            total_songs = spotify_client.get_total_songs(
                                playlist_id)
                            myEmbed = discord.Embed(
                                title="Song added", description=f'''Name: [{added_song.name}]({song_url})
                                By: {added_song.artist}
                                Added to: [{playlist_name}]({addingurl})
                                Position: {total_songs}
                                ''')
                            await output_channel.send(embed=myEmbed)
            except:
                myEmbed = discord.Embed(
                    title="Error", description=f"No argument specified.\n Try `{prefix[0]}help` to see all commands")
                await output_channel.send(embed=myEmbed)

        elif is_command_delete(command):
            try:
                playlist_name, playlist_id = sbotify_db.return_set_playlists(
                    str(message.author.id))
                author, view, edit = sbotify_db.return_playlist_settings(
                    playlist_id)
                if edit == "lock" and str(message.author.id) != str(author):
                    myEmbed = discord.Embed(
                        title="Error", description=f'''This playlist is locked. Cannot modify a locked playlist.
                            ''')
                    await output_channel.send(embed=myEmbed)
                else:
                    number = str(mssg[1])
                    if number != 'last':
                        number = int(mssg[1])

                    if (playlist_id == '0'):
                        await output_channel.send("You have no playlists set")
                    else:
                        addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                        total_songs = spotify_client.get_total_songs(
                            playlist_id)
                        if number == 'last':
                            number = total_songs
                        if(number > total_songs):
                            myEmbed = discord.Embed(
                                title="Error", description=f"There are only {total_songs} songs in this playlist.")
                            await output_channel.send(embed=myEmbed)
                        else:
                            spotify_client.delete_song_by_position(
                                number, playlist_id)
                            myEmbed = discord.Embed(
                                title="Song removed", description=f"Song deleted from [{playlist_name}]({addingurl})\nat position {number}")
                            await output_channel.send(embed=myEmbed)
            except:
                myEmbed = discord.Embed(
                    title="Error", description=f"No or wrong argument specified.\n Try `{prefix[0]}help` to see usage.")
                await output_channel.send(embed=myEmbed)

        elif is_command_join(command):
            new_member = str(message.author.id)
            if sbotify_db.check_member(new_member) == 1:
                myEmbed = discord.Embed(
                    title="You are already a part of the clan", description=f"Try `{prefix[0]}help` to see all commands")
                await output_channel.send(embed=myEmbed)
            else:
                sbotify_db.insert_members(new_member)
                description_message = "Try `!help` to see all commands"
                myEmbed = discord.Embed(
                    title="Welcome to the Sbotify family!", description=description_message)
                await output_channel.send(embed=myEmbed)
        elif is_command_rename(command):
            playlist_name, playlist_id = sbotify_db.return_set_playlists(
                str(message.author.id))
            author, view, edit = sbotify_db.return_playlist_settings(
                playlist_id)
            if edit == "lock" and str(message.author.id) != str(author):
                myEmbed = discord.Embed(
                    title="Error", description=f'''This playlist is locked. Cannot modify a locked playlist.
                            ''')
                await output_channel.send(embed=myEmbed)
            else:
                if sbotify_db.check_playlist(mssg[1]) == 0:

                    if (playlist_id == '0'):
                        await output_channel.send("You have no playlists set")
                        return
                    addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                    myEmbed = discord.Embed(
                        title="Playlist Renamed", description=f"Playlist renamed to [{mssg[1]}]({addingurl})")
                    await output_channel.send(embed=myEmbed)
                    sbotify_db.rename_playlist(message.author.id, mssg[1])
                    spotify_client.rename_playlist(playlist_id, mssg[1])
                else:
                    myEmbed = discord.Embed(
                        title="Playlist already exists", description=f"Playlist by the name {mssg[1]} already exists.\nThink of a new name")
                    await output_channel.send(embed=myEmbed)
        elif is_command_describe(command):
            playlist_name, playlist_id = sbotify_db.return_set_playlists(
                str(message.author.id))
            author, view, edit = sbotify_db.return_playlist_settings(
                playlist_id)
            if edit == "lock" and str(message.author.id) != str(author):
                myEmbed = discord.Embed(
                    title="Error", description=f'''This playlist is locked. Cannot modify a locked playlist.
                            ''')
                await output_channel.send(embed=myEmbed)
            else:
                if sbotify_db.check_playlist(mssg[1]) == 0:

                    if (playlist_id == '0'):
                        await output_channel.send("You have no playlists set")
                        return
                    addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                    myEmbed = discord.Embed(
                        title="Playlist description changed", description=f"Playlist description changed to **{mssg[1]}**")
                    await output_channel.send(embed=myEmbed)
                    spotify_client.describe_playlist(playlist_id, mssg[1])
                else:
                    myEmbed = discord.Embed(
                        title="Error", description=f"Something went wrong, Please try again, see `!help` for usage.")
                    await output_channel.send(embed=myEmbed)
        elif is_command_lock(command) or is_command_unlock(command):
            member_id = str(message.author.id)
            playlist_name, playlist_id = sbotify_db.return_set_playlists(
                member_id)
            huh = sbotify_db.set_edit_settings(command, member_id, playlist_id)
            if huh == 1:
                myEmbed = discord.Embed(
                    title=f"Playlist {command}ed")
                await output_channel.send(embed=myEmbed)
            if huh == 0:
                myEmbed = discord.Embed(
                    title="Error", description=f"Not your playlist, smh. You cannot {command} someone else's playlists.")
                await output_channel.send(embed=myEmbed)

        elif is_command_private(command) or is_command_public(command):
            member_id = str(message.author.id)
            playlist_name, playlist_id = sbotify_db.return_set_playlists(
                member_id)
            huh = sbotify_db.set_view_settings(command, member_id, playlist_id)
            if huh == 0:
                myEmbed = discord.Embed(
                    title="Error", description=f"Not your playlist, smh. You cannot make someone else's playlists {command}.")
                await output_channel.send(embed=myEmbed)

        elif is_command_set(command):
            flag1 = 0
            flag2 = 0
            # print(mssg[1])

            if(len(mssg) == 1):
                myEmbed = discord.Embed(
                    title="Error", description=f"No argument specified.\n Try `{prefix[0]}help` to see all commands")
                await output_channel.send(embed=myEmbed)

            if sbotify_db.check_member(str(message.author.id)) == 1:
                flag1 = 1
                if sbotify_db.check_playlist(str(mssg[1])) == 1:
                    flag2 = 1
                    name = sbotify_db.return_playlist_id(mssg[1])
                    sbotify_db.update_set_playlist(
                        str(message.author.id), str(name))
                    playlist_name, playlist_id = sbotify_db.return_set_playlists(
                        str(message.author.id))
                    addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                    myEmbed = discord.Embed(
                        title="Playlist set", description=f"Playlist set to [{playlist_name}]({addingurl})")
                    await output_channel.send(embed=myEmbed)

            if(flag1 == 0):
                myEmbed = discord.Embed(
                    title="Error", description=f"Uh Oh, you are not yet part of the clan\n Use `{prefix[0]}join` to be a part of Sbotify family!")
                await output_channel.send(embed=myEmbed)

            elif(flag2 == 0):
                new_playlist = spotify_client.create_playlist(mssg[1])
                print(new_playlist)
                sbotify_db.insert_playlist(
                    new_playlist.name, new_playlist.id, str(message.author.id))
                sbotify_db.update_set_playlist(
                    str(message.author.id), new_playlist.id)
                myEmbed = discord.Embed(
                    title="Playlist created and set", description=f"Name : [{mssg[1]}](https://open.spotify.com/playlist/{new_playlist.id})")
                await output_channel.send(embed=myEmbed)

        else:
            myEmbed = discord.Embed(
                title="Error", description=f"This is not a recognized command.\n Try `{prefix[0]}help` to see all commands")
            await output_channel.send(embed=myEmbed)
        sbotify_db.db.commit()

# Run the client on this server
client.run('ODU0ODEwMTc0NzUzNzM0Njg2.YMpWAw.en-SE9Y-87G2u1soPxKwV4TSNQ0')
