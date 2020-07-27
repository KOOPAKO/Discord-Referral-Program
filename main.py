import discord
import operator
import copy
import json
from discord.ext import commands, tasks
from pathlib import Path
from itertools import cycle

# invite link = https://discordapp.com/oauth2/authorize?client_id=clientID&permissions=8&scope=bot&
config = json.load(open(Path('config/config.json'))) # load cfgs

prefix = config["prefix"]
specifiedChannelId = int(config["specifiedChannelId"])
TOKEN = config["bot-token"]

client = commands.Bot(command_prefix = prefix)
client.remove_command('help')
status = cycle([discord.Status.idle, discord.Status.dnd, discord.Status.online])
activity = cycle([f'{prefix}help', f'~{prefix}help~', f'~~{prefix}help~~'])

#load dictionaries from saved files
joinedServer = json.load(open(Path('data/joinedServer.json')))
referralCode = json.load(open(Path('data/referralCode.json')))
referralCount = json.load(open(Path('data/referralCount.json')))

#preload
inviteCount = {}
inviteCount2 = {}

def dumpToJson():
    jJoinedServer = json.dumps(joinedServer)
    with open(Path('data/joinedServer.json'), 'w') as f:
        f.write(jJoinedServer)
        f.close()
    jreferralCode = json.dumps(referralCode)
    with open(Path('data/referralCode.json'), 'w') as f:
        f.write(jreferralCode)
        f.close()
    jreferralCount = json.dumps(referralCount)
    with open(Path('data/referralCount.json'), 'w') as f:
        f.write(jreferralCount)
        f.close()
dumpToJson()

@client.event
async def on_ready():
    print('Client Ready')
    change_status.start()
    for guildItem in client.guilds: #append item with key:guildname, value:dictionary
        inviteList = await guildItem.invites()
        inviteCount[guildItem.name] = {}
        for invite in inviteList: # append item to dictionary of guildname with key:invite, value: number of uses
            inviteCount[guildItem.name][invite.code] = int(invite.uses)

@tasks.loop(seconds=3)
async def change_status():
    await client.change_presence(activity=discord.Game(next(activity)), status=next(status))


@client.event
async def on_member_join(member):
    if not member.id in joinedServer:
        joinedServer.append(member.id)
        dumpToJson()
        # compare inviteCount with inviteCount 2
        for guildItem in client.guilds: #append item with key:guildname, value:dictionary
            inviteList = await guildItem.invites()
            inviteCount2[guildItem.name] = {}
            for invite in inviteList: # append item to dictionary of guildname with key:invite, value: number of uses
                inviteCount2[guildItem.name][invite.code] = int(invite.uses)
        for inviteCode in inviteCount[member.guild.name]: # check which invite count has changed
            if inviteCount[member.guild.name][inviteCode] != inviteCount2[member.guild.name][inviteCode]:
                referralCount[referralCode[str(inviteCode)]] += 1 # Increase the referrers referral count
                for guildItem in client.guilds: #append item with key:guildname, value:dictionary
                    inviteList = await guildItem.invites()
                    inviteCount[guildItem.name] = {}
                    for invite in inviteList: # append item to dictionary of guildname with key:invite, value: number of uses
                        inviteCount[guildItem.name][str(invite.code)] = int(invite.uses)
                break
            elif inviteCount[member.guild.name][inviteCode] > inviteCount2[member.guild.name][inviteCode]:
                return


    else:
        print(f'{member} has already joined, not counting referrals')
    dumpToJson()

@client.command()
async def help(ctx):
    if ctx.message.channel.id == int(specifiedChannelId):
        embededHelp = discord.Embed(
            colour = discord.Colour.blue(),
            title = 'Help',
            description = 'Here is a list of all commands and their functions'
        )
        embededHelp.add_field(
                name='Command:',
                value=f'{prefix}getreferral\n{prefix}referralcount\n{prefix}referraltop\n{prefix}help\n{prefix}referral',
                inline=True
        )
        embededHelp.add_field(
                name='Use:',
                value='Creates a referral code\nDisplays a toal count of your referrals\nEmbeds a list of the top 10 referrers\nDisplays this embed\nDisplays info on getting started',
                inline=True
        )

        await ctx.send(f"Help Sent! Check your PM's {ctx.message.author.mention}")
        await ctx.message.author.send(embed=embededHelp)
    else:
        await ctx.send(f'{ctx.message.author.mention} please use the channel: {ctx.guild.get_channel(specifiedChannelId).mention} for these commands')

@client.command()
async def referral(ctx):
    if ctx.message.channel.id == int(specifiedChannelId):
        await ctx.send(f'{ctx.message.author.mention}, try `{prefix}getreferral` to get started or `{prefix}help` for more information.')
    else:
        await ctx.send(f'{ctx.message.author.mention} please use the channel: {ctx.guild.get_channel(specifiedChannelId).mention} for these commands')


@client.command()
async def getreferral(ctx):
    if ctx.message.channel.id == int(specifiedChannelId):
        if ctx.message.author.id in referralCode.values():
            await ctx.send(f'You already have a referral link {ctx.message.author.mention}')
        else:
            invitelinknew = await ctx.message.channel.create_invite(destination = ctx.guild)
            referralCode[ctx.message.author.id] = str(invitelinknew.id)
            await ctx.send(f"Done! Check your PM's {ctx.message.author.mention}")
            await ctx.message.author.send(f'Thank you for joining the referral program {ctx.message.author.mention}!\nYour personal referral code is {invitelinknew}\nThe bot will now  be tracking how many individual people use your code')
            referralCount[ctx.message.author.id] = 0
            referralCode[invitelinknew.code] = ctx.message.author.id
            #update inviteCount
            for guildItem in client.guilds: #append item with key:guildname, value:dictionary
                inviteList = await guildItem.invites()
                inviteCount[guildItem.name] = {}
                for invite in inviteList: # append item to dictionary of guildname with key:invite, value: number of uses
                    inviteCount[guildItem.name][invite.code] = int(invite.uses)
    else:
        await ctx.send(f'{ctx.message.author.mention} please use the channel: {ctx.guild.get_channel(specifiedChannelId).mention} for these commands')
    dumpToJson()

@client.command()
async def referralcount(ctx):
    if ctx.message.channel.id == int(specifiedChannelId):
        if ctx.message.author.id in referralCode.values():
            if referralCount[ctx.message.author.id] == 1:
                await ctx.send(f'{ctx.message.author.mention}, you have {referralCount[ctx.message.author.id]} referral so far!')
            elif referralCount[ctx.message.author.id] == 0:
                await ctx.send(f'{ctx.message.author.mention}, you have no referrals yet.')
            else:
                await ctx.send(f'{ctx.message.author.mention}, you have {referralCount[ctx.message.author.id]} referrals so far!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, you have not set up your referral link yet.\n Type `{prefix}getreferral` to get started.')
    else:
        await ctx.send(f'{ctx.message.author.mention} please use the channel: {ctx.guild.get_channel(specifiedChannelId).mention} for these commands')

@client.command()
async def referraltop(ctx):
    if ctx.message.channel.id == int(specifiedChannelId):
        referralOrder = copy.deepcopy(referralCount)
        topText1 = ""
        topText2 = ""
        count = 0
        embededReply = discord.Embed(
            title = 'Top Referrers',
            description = 'People with most referrals are:',
            colour = discord.Colour.blue()
        )
        if len(referralOrder) == 0:
            embededReply.add_field(name='null', value='there are no referrers yet')
        else:
            for i in range(9):
                count += 1
                try:
                    topText1 += f'#{i+1} {ctx.guild.get_member(max(referralOrder.items(), key=operator.itemgetter(1))[0]).name}'
                    topText2 += str(max(referralOrder.items(), key=operator.itemgetter(1))[1])
                    del(referralOrder[max(referralOrder.items(), key=operator.itemgetter(1))[0]])
                    if count < 10:
                        topText1 += ('\n')
                        topText2 += ('\n')
                except ValueError:
                    break

            embededReply.add_field(name='**Name**', value=topText1, inline=True)
            embededReply.add_field(name='**Count**', value=topText2, inline=True)

        await ctx.send(embed=embededReply)
    else:
        await ctx.send(f'{ctx.message.author.mention} please use the channel: {ctx.guild.get_channel(specifiedChannelId).mention} for these commands')

client.run(TOKEN) # Leave at end of code
