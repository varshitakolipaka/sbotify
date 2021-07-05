# import the discord library
import discord
from discord import message
from createplaylist import main
import array
# bot connect
client = discord.Client()
# this variable stores id of an output channel, you can have many variables corresponding to different channels
out_channel = 854832431764602901

# list of commands
commands = ["add", "remove"]

# checks if a given command is in the list or not


def is_command(command):
    if command in commands:
        return 1
    else:
        return 0

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
        if is_command(command):
            query = mssg[1]
            main(query,"https://open.spotify.com/playlist/123gKtvvoFi0iNMjvTHsC3")
            # await output_channel.send(command)
            # await output_channel.send(mssg[1])
        else:
            myEmbed = discord.Embed(
                title="Error", description="This is not a recognized command.\n Try <prefix>help to see all commands")
            await output_channel.send(embed=myEmbed)
            # yp = 0


# Run the client on this server
client.run('ODU0ODEwMTc0NzUzNzM0Njg2.YMpWAw.uN414vAZSXjIkRKA-L08ynOF4aI')
