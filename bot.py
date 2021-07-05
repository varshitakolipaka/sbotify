# import the discord library
import discord
from discord import message
from discord import embeds
from createplaylist import main
from commands_parser import *
import array
# bot connect
client = discord.Client()
# this variable stores id of an output channel, you can have many variables corresponding to different channels
out_channel = 854832431764602901
prefix = '!'

# list of playlists
playlists = [[''badmin2'', ["yo", "lmao"],
              ["another yo", "another lmao"]], ["7536042733445921155"]]
# event refers to any new,.. well .... event xD, like sending a message,a reaction, a reply, a bot joining etc


@client.event
# new event
async def on_ready():
    # output_channel object holds the info of that channel, whos id is provided
    output_channel = client.get_channel(out_channel)
    # code to send message is
    await output_channel.send("Hemlos guys, I am noise bot")


@client.event
async def on_message(message):
    output_channel = client.get_channel(out_channel)
    input_mssg = message.content  # message.content is the string of that message
    if input_mssg[0] == '!':
        mssg = input_mssg.split(" ", 1)
        command = mssg[0][1:len(mssg[0])]
        if is_command_add(command):
            query = mssg[1]
            # main(query,"https://open.spotify.com/playlist/123gKtvvoFi0iNMjvTHsC3")
            # await output_channel.send(command)
            # await output_channel.send(mssg[1])
            await output_channel.send(message.author.id)
        elif is_command_set(command):
            flag1 = 0
            flag2 = 0
            if(len(mssg) == 1):
                myEmbed = discord.Embed(
                    title="Error", description="No argument specified.\n Try {prefix} help to see all commands")
                await output_channel.send(embed=myEmbed)
            for i in playlists:
                if(i[0] == str(message.author.id)):
                    # print(i[0])
                    if (len(i) != 1):
                        # print("yess")
                        for j in i:
                            if(type(j) == str):
                                continue
                            if(j[0] == mssg[1]):
                                pos = i.index(j)
                                swap(i, 1, pos)
                                flag2 = 1
                                break
                        print("lmao")
                        flag1 = 1
                        break
                        print(i[0])

            if(flag1 == 0):
                myEmbed = discord.Embed(
                    title="Error", description="Uh Oh :(( , you are not yet part of the clan\n Use {prefix} join to be a part of noise_bot family!")
                await output_channel.send(embed=myEmbed)
            elif(flag2 == 0):
                # make_playlist(mssg[1])
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
client.run('ODU0ODEwMTc0NzUzNzM0Njg2.YMpWAw.uN414vAZSXjIkRKA-L08ynOF4aI')
