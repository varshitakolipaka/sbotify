import os
import re

from spotifyclient import SpotifyClient
from playlist import Playlist
# import the discord library
import discord
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
out_channel = 854832431764602901
prefix = '!'

# list of playlists
playlists = []
# event refers to any new,.. well .... event xD, like sending a message,a reaction, a reply, a bot joining etc
members = []


@client.event
# new event
async def on_ready():
    # output_channel object holds the info of that channel, whos id is provided
    output_channel = client.get_channel(out_channel)
    # code to send message is
    await output_channel.send("I art been summoneth.")


@client.event
async def on_message(message):
    output_channel = message.channel
    input_mssg = message.content  # message.content is the string of that message
    if input_mssg[0] == '!':
        mssg = input_mssg.split(" ", 1)
        command = mssg[0][1:len(mssg[0])]
        if (str(message.author.id) not in members) and not(is_command_join(command)):
            myEmbed = discord.Embed(
                title="Error", description="Uh Oh :(( , you are not yet part of the clan\n Use {prefix} join to be a part of noise_bot family!")
            await output_channel.send(embed=myEmbed)
            return
        if is_command_add(command):
            query = mssg[1]
            for i in playlists:
                if(i[0] == str(message.author.id)):
                    # print(i[0])
                    if (len(i) != 1):
                        # print("yess")
                        var = str(i[1].id)
                        addingurl = "https://open.spotify.com/playlist/" + var
                        main(query, addingurl)
                        print(addingurl)
                        break
            print(playlists)
            # main(query,"https://open.spotify.com/playlist/123gKtvvoFi0iNMjvTHsC3")
            # await output_channel.send(command)
            # await output_channel.send(mssg[1])
            # await output_channel.send(message.author.id)
        elif is_command_delete(command):
            print("DELEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEETE")
            number = int(mssg[1])
            for i in playlists:
                if(i[0] == str(message.author.id)):
                    # print(i[0])
                    if (len(i) != 1):
                        # print("yess")
                        var = str(i[1].id)
                        spotify_client.delete_song_by_position(number, var)
                        break

        elif is_command_join(command):
            new_member = [str(message.author.id)]
            if str(message.author.id) in members:
                myEmbed = discord.Embed(
                    title="You are already a part of the clan", description="Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)
            else:
                playlists.append(new_member)
                members.append(str(message.author.id))
                myEmbed = discord.Embed(
                    title="Welcome to the noise bot pawri!", description="Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)
            print(playlists)
            print(members)
        elif is_command_set(command):
            flag1 = 0
            flag2 = 0
            if(len(mssg) == 1):
                myEmbed = discord.Embed(
                    title="Error", description="No argument specified.\n Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)
            if str(message.author.id) in members:
                flag1 = 1
                for i in playlists:
                    if(i[0] == str(message.author.id)):
                        # print(i[0])
                        if (len(i) != 1):
                            # print("yess")
                            for j in i:
                                if(type(j) == str):
                                    continue
                                if(type(j) == Playlist and j.name == mssg[1]):
                                    pos = i.index(j)
                                    swap(i, 1, pos)
                                    flag2 = 1
                                    break
                            break

            if(flag1 == 0):
                myEmbed = discord.Embed(
                    title="Error", description="Uh Oh :(( , you are not yet part of the clan\n Use {prefix} join to be a part of noise_bot family!")
                await output_channel.send(embed=myEmbed)
            elif(flag2 == 0):
                await output_channel.send("Playlist doesn't exist.\nDo you want to create one by the name {mssg[1]}\n Reply with (y/n) to this message")
                new_playlist = spotify_client.create_playlist(mssg[1])
                print(new_playlist)
                playlists[playlists.index(i)].append(new_playlist)
                myEmbed = discord.Embed(
                    title="Playlist created", description="Name : {mssg[1]}")
                await output_channel.send(embed=myEmbed)
            for i in playlists:
                print(i)
        else:
            myEmbed = discord.Embed(
                title="Error", description="This is not a recognized command.\n Try {prefix} help to see all commands")
            await output_channel.send(embed=myEmbed)


# Run the client on this server
client.run('ODU0ODEwMTc0NzUzNzM0Njg2.YMpWAw.en-SE9Y-87G2u1soPxKwV4TSNQ0')
