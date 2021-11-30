import discord
from discord.ext import commands

client = commands.Bot(command_prefix = "?")
client.remove_command("help")

## Status van bot en log

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('?help'))
    print("Bot is succesfully running.")

## Help command

@client.command()
async def help(ctx):
    author = ctx.message.author

    emb = discord.Embed(
        colour = discord.Colour.green()
    )

    emb.set_author(name="Bot Commands")
    emb.add_field(name="**?embed [message]**", value="Recieve a embed with your own custom message.")
    emb.add_field(name="**?kick**",  value="Kick a mentioned user.")
    emb.add_field(name="**?ban**",  value="Ban a mentioned user.")
    emb.add_field(name="**?mute**",  value="Mute a banned user.")
    emb.add_field(name="**?unmute**",  value="Unmute a banned user.")
    emb.add_field(name="**?grenade**",  value="Cleares 50 messages.")
    emb.add_field(name="**?rocket**",  value="Cleares 200 messages.")
    emb.add_field(name="**?nuke**",  value="Cleares 500 messages.")
    emb.add_field(name="**?clear**",  value="Cleares a specific amount of messages.")
    emb.add_field(name="**?unban**",  value="Unban a banned user.")
    emb.add_field(name="**?userinfo**",  value="Get more information about a user.")
    emb.set_image(url="https://cdn.discordapp.com/attachments/877138928627482665/914633441335738419/0_dC3rip7Gx5z8l4hW_.gif")   

    await ctx.message.author.send(embed=emb)
    
    emb2 = discord.Embed(
        colour = discord.Colour.green()
    )

    emb2.set_author(name="Please check your dms.")

    await ctx.send(embed=emb2)

## Grenade command

@client.command()
@commands.has_permissions(manage_messages=True)
async def grenade(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await ctx.send("50 Messages have been cleared.")

## Rocket command

@client.command()
@commands.has_permissions(manage_messages=True)
async def rocket(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await ctx.send("200 Messages have been cleared.")

## Nuke command

@client.command()
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, amount=50):
    await ctx.channel.purge(limit=amount)
    await ctx.send("500 Messages have been cleared.")

## Clear command

@client.command(aliases=["purge"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=11):
    ammount = amount+1
    if amount > 1001:
        await ctx.send("Can not delete more than 1000 message")
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send("Messages have been cleared.")


## Mute command

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

## Unmute command

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

## Userinfo

@client.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="**Name**", value=user.name, inline=True)
    embed.add_field(name="**Nickname**", value=user.nick, inline=True)
    embed.add_field(name="**iD**", value=user.id, inline=True)
    embed.add_field(name="**Status**", value=user.status, inline=True)
    embed.add_field(name="**Highest Role**", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

## Ban command

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"{user} have been bannned.")

## Embed command

@client.command()
async def embed(ctx, *args):
    author = ctx.message.author
    textMessage = str(' '.join(args))
    if len(textMessage) > 256:
        emb = discord.Embed(
            colour = discord.Colour.red()
        )

        emb.set_author(name="Your embed message cannot contain more than 256 characters.")

        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(
            colour = discord.Colour.green()
        )

        emb.set_author(name=textMessage)

        await ctx.send(embed=emb)

## Kick Command
    
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.kick(reason=reason)
  await ctx.send(f"{user} Has been kicked.")

## Unban command

@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} Has been unbanned.")
    return

## Run bot client

client.run("your discord bot token here")