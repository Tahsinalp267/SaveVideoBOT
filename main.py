import discord, os, downloader
from discord.ext import commands

prefixes = ['sv ', 'Sv ']
bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="sv help"))
    print('Bot is online.')

@bot.command(aliases=['Video'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def video(ctx, url):
    if "youtu" in url:

        try:
            if downloader.checkYoutube(url, 60):
                async with ctx.typing():
                    downloader.downloadYoutube(url)
                    await ctx.send(content=f"YouTube video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
                    os.remove("savevideo.mp4")
                    await ctx.message.delete()
                    print("Sent the YouTube video!")
            else:
                await ctx.send("Your video is longer than 60 seconds!\n(This is because of the Discord upload limit.)")
                print(f"Your video is longer than 60 seconds! (YouTube)\n{url}")
        
        except:
            await ctx.send("Something went wrong while getting the video.")
            os.remove("savevideo.mp4")
            await ctx.message.delete()
            print(f"Something went wrong while getting the video. (YouTube)\n{url}")

    elif "/comments/" in url:

        try:
            if downloader.checkReddit(url, 60):
                async with ctx.typing():
                    downloader.downloadReddit(url)
                    downloader.renameReddit("savevideo.mp4")
                    await ctx.send(content=f"Reddit video sent by {ctx.message.author.mention}", file=discord.File(fp="savevideo.mp4"))
                    os.remove("savevideo.mp4")
                    await ctx.message.delete()
                    print("Sent a Reddit video!")
            else:
                await ctx.send("Your video is longer than 60 seconds!\n(This is because of the Discord upload limit.)")
                print(f"Your video is longer than 60 seconds! (Reddit)\n{url}")

        except:
            await ctx.send("Something went wrong while getting the video.")
            os.remove("savevideo.mp4")
            await ctx.message.delete()
            print(f"Something went wrong while getting the video. (Reddit)\n{url}")

@bot.command(aliases=['Help'])
async def help(ctx):
    embed = discord.Embed(
        title="SaveVideo Support",
        description="Maximum video length is 60 seconds.\nSupports YouTube and Reddit.",
        colour=discord.Color.blurple())

    embed.add_field(name='**sv help**', value="Displays this message.", inline=False)
    embed.add_field(name='**sv stats**', value="Shows the bot's statistics.", inline=False)
    embed.add_field(name='**sv video <URL>**', value="Downloads the video from the given URL.", inline=False)
    embed.add_field(name='**Links**', value='[Invite SaveVideo](https://discord.com/api/oauth2/authorize?client_id=783728124021702689&permissions=8&scope=bot) | [Feedback Server](https://discord.gg/vNmAgsB3uV) | [Source Code](https://github.com/Tahsinalp267/SaveVideoBOT)')
    embed.set_thumbnail(url="https://i.hizliresim.com/orhNo4.png")
    await ctx.send(embed=embed)

@bot.command(aliases=['Stats'])
async def stats(ctx):
    await ctx.send(f"Bot latency: `{round(bot.latency * 1000)}ms`\nTotal servers: `{len(bot.guilds)}`\nTotal users: `{sum(guild.member_count for guild in bot.guilds)}`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to provide an URL.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Couldn't find that command.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Command on interserveral cooldown. Try again in {error.retry_after:0.1f} seconds.")

if __name__ == "__main__":
    bot.run("TOKEN")
