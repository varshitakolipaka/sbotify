import os
import json
from spotifyclient import SpotifyClient
from playlist import Playlist
#importing database creating file and class spotify_db
from database.db_mgmt import sbotify_db
from discord import message
from discord import embeds
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
    output_channel = client.get_channel(out_channel)
    input_mssg = message.content  # message.content is the string of that message
    if input_mssg[0] == '!':
        mssg = input_mssg.split(" ", 1)
        command = mssg[0][1:len(mssg[0])]
        if (sbotify_db.check_member(message.author.id) == 0) and (command != 'join'):
            myEmbed = discord.Embed(
                title="Error", description=f"Uh Oh :(( , you are not yet part of the clan\n Use {prefix} join to be a part of noise_bot family!")
            await output_channel.send(embed=myEmbed)
        elif is_command_add(command):
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
        elif is_command_delete(command):
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

        elif is_command_join(command):
            new_member = str(message.author.id)
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

        elif is_command_set(command):
            flag1 = 0
            flag2 = 0
            print(mssg[1])

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
                    playlist_name, playlist_id = sbotify_db.return_set_playlists(str(message.author.id))
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
                sbotify_db.insert_playlist(new_playlist.name, new_playlist.id)
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
