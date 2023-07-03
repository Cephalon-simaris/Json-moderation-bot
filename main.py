import discord
from discord.ext import commands
import json
from datetime import datetime
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix = ">", intents = intents)
client.remove_command("help")

def warnspecify(guild_id, user_id, amount, reason, time):
    with open('warns.json','r') as f:
        data = json.load(f)
    
    if amount == 1:
        data[str(guild_id)] = {str(user_id) : {"Warnings" : amount,"Warning1" : reason,"Warntime1" : time}}
    elif amount == 2:
        data[str(guild_id)][str(user_id)]["Warnings"] = amount
        data[str(guild_id)][str(user_id)]["Warning2"] = reason
        data[str(guild_id)][str(user_id)]["Warntime2"] = time
    else:
        data[str(guild_id)][str(user_id)]["Warnings"] = amount
        data[str(guild_id)][str(user_id)]["Warning3"] = reason
        data[str(guild_id)][str(user_id)]["Warntime3"] = time

    with open('warns.json','w') as f:
        json.dump(data,f,indent=4)

def singlewarnclear(guild_id, user_id, amount):
    with open('warns.json','r') as f:
        data = json.load(f)
        amount += 1
    
    if amount == 1:
        del data[str(guild_id)][str(user_id)]
    elif amount == 2:
        data[str(guild_id)][str(user_id)]["Warnings"] = amount-1
        del data[str(guild_id)][str(user_id)]["Warning2"]
        del data[str(guild_id)][str(user_id)]["Warntime2"]
    else:
        data[str(guild_id)][str(user_id)]["Warnings"] = amount-1
        del data[str(guild_id)][str(user_id)]["Warning3"]
        del data[str(guild_id)][str(user_id)]["Warntime3"]

    with open('warns.json','w') as f:
        json.dump(data,f,indent=4)

def warnclear(guild_id, user_id):
    with open('warns.json','r') as f:
        data = json.load(f)

        del data[str(guild_id)][str(user_id)]

    with open('warns.json','w') as f:
        json.dump(data,f,indent=4)

def displaywarns(guild_id, user_id):
    with open('warns.json','r') as f:
        data = json.load(f)

    lilist = []
    warncount = data[str(guild_id)][str(user_id)]["Warnings"]
    if warncount == 1:
        Warning1 = data[str(guild_id)][str(user_id)]["Warning1"]
        time1 = data[str(guild_id)][str(user_id)]["Warntime1"]
        lilist.append(Warning1)
        lilist.append(time1)
    elif warncount == 2:
        Warning1 = data[str(guild_id)][str(user_id)]["Warning1"]
        Warning2 = data[str(guild_id)][str(user_id)]["Warning2"]
        time1 = data[str(guild_id)][str(user_id)]["Warntime1"]
        time2 = data[str(guild_id)][str(user_id)]["Warntime2"]
        lilist.append(Warning1)
        lilist.append(Warning2)
        lilist.append(time1)
        lilist.append(time2)
    else:
        Warning1 = data[str(guild_id)][str(user_id)]["Warning1"]
        Warning2 = data[str(guild_id)][str(user_id)]["Warning2"]
        Warning3 = data[str(guild_id)][str(user_id)]["Warning3"]
        time1 = data[str(guild_id)][str(user_id)]["Warntime1"]
        time2 = data[str(guild_id)][str(user_id)]["Warntime2"]
        time3 = data[str(guild_id)][str(user_id)]["Warntime3"]
        lilist.append(Warning1)
        lilist.append(Warning2)
        lilist.append(Warning3)
        lilist.append(time1)
        lilist.append(time2)
        lilist.append(time3)
    
    return lilist

def get_warn_count(guild_id, user_id):
    with open('warns.json','r') as f:
        data = json.load(f)

    try:    
        warncount = data[str(guild_id)][str(user_id)]["Warnings"]
        return warncount
    except:
        warncount = 0
        return warncount

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2


    return val * time_dict[unit]

@client.event
async def on_ready():
    activity = discord.Activity(name="Suspicious People", type=3)
    await client.change_presence(status = discord.Status.online, activity = activity)
    print("The Bot is ready!")

@client.command()
async def help(ctx):
    embed=discord.Embed(title="**Security Assisstant**", description="**Command prefix : `>`**", timestamp = ctx.message.created_at, color=0x69ec5f)
    embed.add_field(name="**Help list**", value="`>help` , `>mod`", inline=True)
    embed.set_thumbnail(url = client.user.avatar_url)
    embed.set_footer(text = ctx.guild, icon_url = ctx.guild.icon_url)
    await ctx.send(embed=embed)

@client.command()
async def mod(ctx):
    embed = discord.Embed(title = "**MODERATION HELP**", timestamp = ctx.message.created_at, color = discord.Colour.green())
    embed.add_field(name = "**Warn someone**", value = "`>warn <member> <reason>`", inline = False)
    embed.add_field(name = "**Unwarn someone**", value = "`>unwarn <member>`", inline = False)
    embed.add_field(name = "**Clear all warns**", value = "`>clearwarns <member>`", inline = False)
    embed.add_field(name = "**Display warns**", value = "`>warns <member>`", inline = False)
    embed.add_field(name = "**Mute someone**", value = "`>mute <member> <time>`", inline = False)
    embed.add_field(name = "**Unmute someone**", value = "`>unmute <member>`", inline = False)
    embed.add_field(name = "**Ban someone**", value = "`>ban <member> <reason>`", inline = False)
    embed.set_thumbnail(url = client.user.avatar_url)
    embed.set_footer(text = ctx.guild, icon_url = ctx.guild.icon_url)
    await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member : discord.Member = None, * ,time : str = None):
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif time == None:
        em = discord.Embed(description = ":x: Time Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    else:
        timeuse = convert(time)
        if timeuse == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        elif timeuse == -2:
            await ctx.send(f"The time must be an integer. Please enter an integer next time")
        else:
            try:
                role = discord.utils.get(ctx.guild.roles,name = "muted")
                try:
                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} has been muted for {time}")
                    await asyncio.sleep(timeuse)
                    try:
                        await member.remove_roles(role)
                    except:
                        pass
                except:
                    await ctx.send("Bot missing permission try placing bot's role at the top")
            except:
                await ctx.send("You don't have a role named \"muted\"! Please make a role named \"muted\" (all lowercase)")

@mute.error
async def mute_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(description = ":x: You did not mention all the parameters", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages = True)
async def unmute(ctx,member : discord.Member = None):
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    else:
        role = discord.utils.get(ctx.guild.roles,name = "muted")
        try:
            await member.remove_roles(role)
        except:
            await ctx.send("The member is already unmuted")

@unmute.error
async def unmute_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages = True)
async def warn(ctx, member: discord.Member = None,*,reason : str = "Not provided"):
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    else:
        a = get_warn_count(ctx.guild.id,member.id)
        if a == 3:
            em = discord.Embed(description = f"***:warning: {member.display_name} has reached the maximum limit of warnings!***", color=discord.Colour.red())
            await ctx.send(embed=em)
        elif a == 2:
            em = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been warned!***", color=discord.Colour.green())
            await ctx.send(embed=em)
            utc = str(datetime.utcnow())
            timeuse = utc[0:19]
            warnspecify(str(ctx.guild.id),str(member.id), 3, reason, timeuse)
            await member.send(f"You have been Warned for the reason - {reason}")
        elif a == 1:
            em = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been warned!***", color=discord.Colour.green())
            await ctx.send(embed=em)
            utc = str(datetime.utcnow())
            timeuse = utc[0:19]
            warnspecify(str(ctx.guild.id),str(member.id), 2, reason, timeuse)
            await member.send(f"You have been Warned for the reason - {reason}")
        else:
            em = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been warned!***", color=discord.Colour.green())
            await ctx.send(embed=em)
            utc = str(datetime.utcnow())
            timeuse = utc[0:19]
            warnspecify(str(ctx.guild.id),str(member.id), 1, reason, timeuse)
            await member.send(f"You have been Warned for the reason - {reason}")

@warn.error
async def warn_error(ctx,error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)

@client.command(aliases = ["unwarn"])
@commands.has_permissions(manage_messages = True)
async def clear_warn(ctx, member : discord.Member= None):
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    else:
        a = get_warn_count(ctx.guild.id,member.id)
        if a == 3:
            em2 = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been unwarned!***", color=discord.Colour.green())
            await ctx.send(embed=em2)
            singlewarnclear(str(ctx.guild.id),str(member.id),2)
            await member.send("You have been unwarned")
        elif a == 2:
            em3 = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been unwarned!***", color=discord.Colour.green())
            await ctx.send(embed=em3)
            singlewarnclear(str(ctx.guild.id),str(member.id),1)
            await member.send("You have been unwarned")
        elif a == 1:
            em4 = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been unwarned!***", color=discord.Colour.green())
            await ctx.send(embed=em4)
            warnclear(str(ctx.guild.id),str(member.id))
            await member.send("You have been unwarned")
        else:
            em5 = discord.Embed(description = ":x: User has no warnings!", color=discord.Colour.red())
            await ctx.send(embed=em5)

@clear_warn.error
async def clear_warn_error(ctx,error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.CommandInvokeError):
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)

@client.command(aliases = ["clearwarns"])
@commands.has_permissions(manage_messages = True)
async def clear_all_warns(ctx,*,member : discord.Member = None):
    a = get_warn_count(ctx.guild.id,member.id)
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif a > 0:
        em = discord.Embed(description = f"***:white_check_mark: all warns removed from {member.display_name}!***", color=discord.Colour.green())
        await ctx.send(embed=em)
        await member.send("All your warnings have been cleared")
        warnclear(ctx.guild.id,member.id)
    else:
        em = discord.Embed(description = ":x: User has no warnings!", color=discord.Colour.red())
        await ctx.send(embed=em)

@clear_all_warns.error
async def clear_all_warns_error(ctx,error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.CommandInvokeError):
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages = True)
async def warns(ctx, member : discord.Member = None):
    abc = displaywarns(str(ctx.guild.id),str(member.id))
    lenght = len(abc)
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif lenght == 0:
        em = discord.Embed(description = ":x: User has no warnings!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif lenght == 2:
        Warn1 = abc[0]
        ttime1 = abc[1]
        embed = discord.Embed(title = f"**Warnings of player {member.display_name}:**", color = discord.Colour.red(), timestamp = ctx.message.created_at)
        embed.add_field(name = f"**Warning 1:**",value = f"**{Warn1}** ({ttime1} UTC)")
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text = ctx.guild, icon_url = ctx.guild.icon_url)
        await ctx.send(embed = embed)
    elif lenght == 4:
        Warn1,Warn2 = abc[0],abc[1]
        ttime1,ttime2 = abc[2],abc[3]
        embed = discord.Embed(title = f"**Warnings of player {member.display_name}:**", color = discord.Colour.red(), timestamp = ctx.message.created_at)
        embed.add_field(name = f"**Warning 1:**",value = f"**{Warn1}** ({ttime1} UTC)")
        embed.add_field(name = f"**Warning 2:**",value = f"**{Warn2}** ({ttime2} UTC)", inline = False)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text = ctx.guild, icon_url = ctx.guild.icon_url)
        await ctx.send(embed = embed)
    else:
        Warn1,Warn2,Warn3 = abc[0],abc[1],abc[2]
        ttime1,ttime2,ttime3 = abc[3],abc[4],abc[5]
        embed = discord.Embed(title = f"**Warnings of player {member.display_name}:**", color = discord.Colour.red(), timestamp = ctx.message.created_at)
        embed.add_field(name = f"**Warning 1:**",value = f"**{Warn1}** ({ttime1} UTC)")
        embed.add_field(name = f"**Warning 2:**",value = f"**{Warn2}** ({ttime2} UTC)", inline = False)
        embed.add_field(name = f"**Warning 3:**",value = f"**{Warn3}** ({ttime3} UTC)", inline = False)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(text = ctx.guild, icon_url = ctx.guild.icon_url)
        await ctx.send(embed = embed)

@warns.error
async def warns_error(ctx,error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.CommandInvokeError):
        em = discord.Embed(description = ":x: User has no Warnings!", color=discord.Colour.red())
        await ctx.send(embed=em)

@client.command()
@commands.has_permissions(manage_messages = True)
async def ban(ctx, member : discord.Member = None, * , reason : str = "Not Provided"):
    if member == None:
        em = discord.Embed(description = ":x: User Not Specified, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    else:
        await member.send(f"**You have been banned from the server** - {ctx.guild.name}\n**Reason** - {reason}")
        await member.ban(reason = reason)
        em = discord.Embed(description = f"***:white_check_mark: {member.display_name} has been banned!***", color=discord.Colour.green())
        await ctx.send(embed=em)

@ban.error
async def ban_error(ctx,error):
    if isinstance(error, commands.MemberNotFound):
        em = discord.Embed(description = ":x: User Not Found, try again!", color=discord.Colour.red())
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(description = ":x: You do not have the permission to use this commmand!", color=discord.Colour.red())
        await ctx.send(embed=em)

client.run("bot token here!")
