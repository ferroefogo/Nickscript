import discord
from discord.ext import commands
import os
import asyncio
from discord.utils import get

my_secret = os.environ['TOKEN']
bot = commands.Bot(command_prefix='!')


@bot.command()
async def nicksetup(ctx, member: discord.Member, names: str):
    # Convert namelist to list
    namelist = [x.strip() for x in names.split(';')]

    embedVar = discord.Embed(title=f'Select a duration for the nickname rotation', color=0x00ff00)
    embedVar.add_field(name="Every 5 minutes", value="🔴", inline=False)
    embedVar.add_field(name="Every 10 minutes", value="🟡", inline=False)
    embedVar.add_field(name="Every 30 minutes", value="🟢", inline=False)
    embedVar.add_field(name="Loops the same few nicknames", value="🔁", inline=False)
    embed_msg = await ctx.send(embed=embedVar)

    await embed_msg.add_reaction("🔴")
    await embed_msg.add_reaction("🟡")
    await embed_msg.add_reaction("🟢")
    await embed_msg.add_reaction("🔁")


    @bot.event
    async def on_raw_reaction_add(payload): # checks whenever a reaction is added to a message
                                            # whether the message is in the cache or not

        # check which channel the reaction was added in
        if payload.channel_id == 689938064344219779:

            channel = await bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            # iterating through each reaction in the message
            for r in message.reactions:

                # checks the reactant isn't a bot and the emoji isn't the one they just reacted with
                if payload.member in await r.users().flatten() and not payload.member.bot:

                    # Unsuccessful conditions

                    if message.reactions[0].count > 1 and message.reactions[1].count > 1:
                        # Red and yellow emoji are both on, BAD.
                        await message.remove_reaction(payload.emoji, payload.member)
                    
                    elif message.reactions[0].count > 1 and message.reactions[2].count > 1:
                        # Red and green emoji are both on, BAD.
                        await message.remove_reaction(payload.emoji, payload.member)

                    elif message.reactions[1].count > 1 and message.reactions[2].count > 1:
                        # Yellow and green emoji are both on, BAD.
                        await message.remove_reaction(payload.emoji, payload.member)


                    # Successful conditions, with repeat.

                    elif message.reactions[0].count > 1 and message.reactions[3].count > 1:
                        # Red circle is on, repeat button is also on.
                        while message.reactions[3].count > 1:
                            for i in range(len(namelist)):
                                await member.edit(nick=namelist[i])
                                await asyncio.sleep(300)

                    
                    elif message.reactions[1].count > 1 and message.reactions[3].count > 1:
                        # Yellow circle is on, repeat button is also on.
                        while message.reactions[3].count > 1:
                            for i in range(len(namelist)):
                                await member.edit(nick=namelist[i])
                                await asyncio.sleep(600)
                    
                    elif message.reactions[2].count > 1 and message.reactions[3].count > 1:
                        # Green circle is on, repeat button is also on.
                        while message.reactions[3].count > 1:
                            for i in range(len(namelist)):
                                await member.edit(nick=namelist[i])
                                await asyncio.sleep(1800)


                    # Successful conditions, without repeat.

                    elif message.reactions[0].count > 1 and message.reactions[3].count > 1:
                        # Red circle is on, repeat button is also on.
                        for i in range(len(namelist)):
                            await member.edit(nick=namelist[i])
                            await asyncio.sleep(300)
                    
                    elif message.reactions[1].count > 1 and message.reactions[3].count > 1:
                        # Yellow circle is on, repeat button is also on.
                        for i in range(len(namelist)):
                            await member.edit(nick=namelist[i])
                            await asyncio.sleep(600)
                    
                    elif message.reactions[2].count > 1 and message.reactions[3].count > 1:
                        # Green circle is on, repeat button is also on.
                        for i in range(len(namelist)):
                            await member.edit(nick=namelist[i])
                            await asyncio.sleep(1800)

@bot.command()
async def nickstatus(ctx):
    pass

bot.run(my_secret)