import os
import json

from dotenv.main import dotenv_values
from spotifyclient import SpotifyClient
from playlist import Playlist
from database.db_mgmt import sbotify_db
import discord
from createplaylist import main
from commands_parser import *
from dotenv import load_dotenv
load_dotenv()
spotify_client = SpotifyClient(os.getenv("SPOTIFY_AUTHORIZATION_TOKEN"),
                               os.getenv("SPOTIFY_USER_ID"))
# bot connect
client = discord.Client()
# this variable stores id of an output channel, you can have many variables corresponding to different channels
out_channel = 'default out channel'

prefix = '!'

# list of playlists
playlists = []
# event refers to any new,.. well .... event xD, like sending a message,a reaction, a reply, a bot joining etc
members = []
personal_playlist = []
motor_functions = [0]


def get_command_help():
    return '''
    1. `!help` : **this message**
    2. `!set <playlist name>`: **sets the playlist to default or creates one if not created **
    3. `!add <song name>` : **adds a song to the playlist**
    4. `!delete <song number>` : **deletes a song from the playlist**
    5. `!join` : **join the clan**
    6. `!list<page number (optional)> <author name>` : **list all songs of the author (put `all` for all playlists)**
    '''


@client.event
# new event
async def on_ready():
    sbotify_db.print_db('Playlists')
    sbotify_db.print_db('Members')
    # output_channel object holds the info of that channel, whos id is provided
    output_channel = client.get_channel(out_channel)
    # code to send message is
    await output_channel.send("Bring yourself back online, Dolores.")
    print("bot started")


@client.event
async def on_message(message):
    output_channel = message.channel
    print(motor_functions)
    input_mssg = message.content  # message.content is the string of that message
    if input_mssg.lower() == 'freeze all motor functions' and (message.author.id == 'badmin1' or message.author.id == 'badmin2'):
        motor_functions[0] = 1
    if input_mssg.lower() == 'bring yourself back online' and (message.author.id == 'badmin1' or message.author.id == 'badmin2'):
        motor_functions[0] = 0
    if input_mssg[0] == '!' and motor_functions[0] == 0:
        mssg = input_mssg.split(" ", 1)
        command = mssg[0][1:len(mssg[0])]
        if (sbotify_db.check_member(message.author.id) == 0) and (command != 'join'):
            myEmbed = discord.Embed(
                title="Error", description=f"Uh Oh :(( , you are not yet part of the clan\n Use `{prefix}join` to be a part of noise_bot family!")
            await output_channel.send(embed=myEmbed)
        elif command == 'print':
            print(message.content)
        elif is_command_help(command):
            myEmbed = discord.Embed(
                title="Help", description=get_command_help())
            await output_channel.send(embed=myEmbed)
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
                        title="Error", description=f"This is not a recognized command.\n Try `{prefix}help` to see all commands")
                    await output_channel.send(embed=myEmbed)
                    return
            try:
                query = str(mssg[1])
                if query.startswith('<@!') and query.endswith('>'):
                    query = query[3:]
                    query = query[:len(query) - 1]
                ret_val = sbotify_db.list_all_playlists(query)
                # print(query)
            except:
                ret_val = sbotify_db.list_all_playlists(message.author.id)
                # print(message.author.id)
            if ret_val == 0:
                myEmbed = discord.Embed(
                    title="No Playlists :pensive:", description=f'''Uh Oh :(( , there aren't any playlists created by this author\n Use `{prefix}set <name>` to create and set playlists\n
                    Use `{prefix}help` to see all commands.''')
                await output_channel.send(embed=myEmbed)
            else:
                # discord embed to list all values of ret_val
                playlist_len = ret_val.__len__()
                # print(playlist_len)
                if(playlist_len <= (page-1)*10 or page <= 0):
                    myEmbed = discord.Embed(
                        title="Page Doesn't Exist", description=f"There are only {int(playlist_len/10) + 1} Pages.\n Try `{prefix}help` to see all commands")
                    await output_channel.send(embed=myEmbed)
                    return
                send_message = ''
                # print("till here")
                for i in ret_val:
                    if ret_val.index(i) < (page-1)*10:
                        continue
                    if ret_val.index(i) >= page*10:
                        break
                    send_message += f'''[**{ret_val.index(i)+1}. {i[0]}**](https://open.spotify.com/playlist/{i[1]})\nCreated by: <@!{i[2]}>\n\n'''
                myEmbed = discord.Embed(
                    title="Playlists", description=f"{send_message}Page: {page} of {int(playlist_len/10) + 1}")
                await output_channel.send(embed=myEmbed)

        elif is_command_add(command):
            try:
                query = mssg[1]
                playlist_name, playlist_id = sbotify_db.return_set_playlists(
                    str(message.author.id))
                print(playlist_name)
                if(playlist_id == '0'):
                    await output_channel.send("You have no playlists set")
                else:
                    addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                    main(query, addingurl)
                    myEmbed = discord.Embed(
                        title="Elon Aproves :triumph:", description=f"Song added to [{playlist_name}]({addingurl})")
                    await output_channel.send(embed=myEmbed)
            except:
                myEmbed = discord.Embed(
                    title="Error", description=f"No argument specified.\n Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)

        elif is_command_delete(command):
            try:
                number = int(mssg[1])
                playlist_name, playlist_id = sbotify_db.return_set_playlists(
                    str(message.author.id))
                if (playlist_id == '0'):
                    await output_channel.send("You have no playlists set")
                else:
                    addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                    spotify_client.delete_song_by_position(number, playlist_id)
                    myEmbed = discord.Embed(
                        title="ELon Disproves :triumph:", description=f"Song deleted from [{playlist_name}]({addingurl})")
                    await output_channel.send(embed=myEmbed)
            except:
                myEmbed = discord.Embed(
                    title="Error", description=f"No argument specified.\n Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)

        elif is_command_join(command):
            new_member = str(message.author.id)
            # DELETE NEXT LINE AFTER TESTING
            sbotify_db.insert_members('755673930215194664')
            if sbotify_db.check_member(new_member) == 1:
                myEmbed = discord.Embed(
                    title="You are already a part of the clan", description=f"Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)
            else:
                sbotify_db.insert_members(new_member)
                description_message = "Try " + "`" + prefix + "help` to see all commands"
                myEmbed = discord.Embed(
                    title="Welcome to the noise bot pawri!", description=description_message)
                await output_channel.send(embed=myEmbed)
        elif is_command_rename(command):
            if sbotify_db.check_playlist(mssg[1]) == 0:
                playlist_name, playlist_id = sbotify_db.return_set_playlists(
                    str(message.author.id))
                if (playlist_id == '0'):
                    await output_channel.send("You have no playlists set")
                    return
                addingurl = f"https://open.spotify.com/playlist/{playlist_id}"
                myEmbed = discord.Embed(
                    title="Playlist set", description=f"Playlist set to [{mssg[1]}]({addingurl})")
                await output_channel.send(embed=myEmbed)
                sbotify_db.rename_playlist(message.author.id, mssg[1])
                spotify_client.rename_playlist(playlist_id, mssg[1])
            else:
                myEmbed = discord.Embed(
                    title="Playlist already exists", description=f"Playlist by the name {mssg[1]} already exists.\nThink of a new name")
                await output_channel.send(embed=myEmbed)
        elif is_command_set(command):
            flag1 = 0
            flag2 = 0
            # print(mssg[1])

            if(len(mssg) == 1):
                myEmbed = discord.Embed(
                    title="Error", description=f"No argument specified.\n Try {prefix} help to see all commands")
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
                    title="Error", description=f"Uh Oh :(( , you are not yet part of the clan\n Use {prefix} join to be a part of noise_bot family!")
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
                title="Error", description=f"This is not a recognized command.\n Try {prefix} help to see all commands")
            await output_channel.send(embed=myEmbed)
        sbotify_db.db.commit()

# Run the client on this server
client.run('ODU0ODEwMTc0NzUzNzM0Njg2.YMpWAw.en-SE9Y-87G2u1soPxKwV4TSNQ0')
