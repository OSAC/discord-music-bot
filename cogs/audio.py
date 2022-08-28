import asyncio

import discord
import youtube_dl

from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = None

    @commands.command(aliases=['aija'])
    async def join(self, ctx, *, channel: discord.VoiceChannel = ""):
        """Joins a voice channel"""
        author = ctx.message.author
        default_voice = discord.utils.find(
            lambda c: c.type == discord.ChannelType.voice, author.guild.channels
        )
        channel = channel or default_voice
        if not author.voice:
            return await ctx.send("You are not connected to any voice channels :(")

        await author.move_to(channel)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url or searches on youtube"""
        async with ctx.typing():
            self.player = await YTDLSource.from_url(
                url, loop=self.bot.loop, stream=True
            )
            ctx.voice_client.play(
                self.player,
                after=lambda e: print("Player error: %s" % e) if e else None,
            )

        await ctx.send("Now playing: {}".format(self.player.title))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Downloads and Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            self.player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                self.player,
                after=lambda e: print("Player error: %s" % e) if e else None,
            )

        await ctx.send("Now playing: {}".format(self.player.title))


    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(aliases=['chup', 'lato'])
    async def mute(self, ctx):
        """Mute the song while still playing"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = 0
        await ctx.send("Muted song")

    @commands.command(aliases=['rok'])
    async def pause(self, ctx):
        """Pause the song"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            await ctx.voice_client.pause()
        else:
            await ctx.send("No songs currently playing.")

    @commands.command(aliases=['baja'])
    async def resume(self, ctx):
        """Resumed a paused song"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        elif ctx.voice_client.is_paused():
            await ctx.voice_client.resume()
        else:
            await ctx.send("No songs currently paused.")

    @commands.command(aliases=['bhag', 'nikal', 'mar'])
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @yt.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel. Kunai yek Voice channel ma jodinuhola")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


async def setup(client):
    await client.add_cog(Music(client))
