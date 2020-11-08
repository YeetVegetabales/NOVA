import discord
from discord.ext import commands


class Info(commands.Cog):
    """Gain some info on users or servers"""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["av"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        """See the profile picture for a user"""
        member = member or ctx.message.author
        embed = discord.Embed(
            color=0x5643fd, title=f"{member}", timestamp=ctx.message.created_at)
        url = str(member.avatar_url).replace(".webp", ".png")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ui'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """See info on a member in the server"""
        status_list = {
            "online": "<:online:726127263401246832> -  ``Online``",
            "offline": "<:offline:726127263203983440> -  ``Offline``",
            "idle": "<:idle:726127192165187594> -  ``Idle``",
            "dnd": "<:dnd:726127192001478746> -  ``Do not disturb``"}
        member = member or ctx.message.author
        roles = [role for role in member.roles]
        servers = len([g for g in self.client.guilds if g.get_member(member.id)])
        embed = discord.Embed(color=0x5643fd, timestamp=ctx.message.created_at)
        embed.set_author(name=f'User Info  -  {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)

        embed.add_field(name='ID:', value=f"<:author:734991429843157042> ``{member.id}``", inline=False)

        embed.add_field(name='Account Created:',
                        value=f"🕒 ``{member.created_at.strftime('%a, %B %d %Y, %I:%M %p UTC')}``",
                        inline=False)
        embed.add_field(name='Joined Server:',
                        value=f"<:member:731190477927219231> "
                              f"``{member.joined_at.strftime('%a, %B %d %Y, %I:%M %p UTC')}``",
                        inline=False)
        embed.add_field(name='Status:', value=f"{status_list[str(member.status)]}", inline=False)
        embed.add_field(name='Shared Servers with NOVA:', value=f"<:wumpus:742965982640865311> ``{servers}``")
        embed.add_field(name=f"Top Roles ({len(roles)} total):",
                        value=" ".join([role.mention for role in roles[::-1][:5]]), inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['si'], usage='')
    @commands.guild_only()
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Get info on a server"""

        if guild_id is not None and await self.client.is_owner(ctx.author):
            guild = self.client.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'<:redx:732660210132451369> NOVA is not in this guild '
                                      f'or this guild ID is invalid.')
        else:
            guild = ctx.guild

        roles = [role for role in guild.roles]

        class Secret:
            pass

        secret_member = Secret()
        secret_member.id = 0
        secret_member.roles = [guild.default_role]
        region = str(guild.region)
        r = region.capitalize()
        emojis = [emoji for emoji in guild.emojis]
        channels = [channel for channel in guild.channels]
        vc = [voice_channel for voice_channel in guild.voice_channels]
        folders = [category for category in guild.categories]
        bots = len([bot for bot in guild.members if bot.bot])
        humans = len(guild.members) - bots

        e = discord.Embed(title=f'<:Discord:735530547992068146> '
                                f'  Server Info  -  {guild.name}', color=0x5643fd, timestamp=ctx.message.created_at,
                          description=guild.description)
        e.add_field(name='ID:', value=f"<:author:734991429843157042> ``{guild.id}``", inline=False)
        e.add_field(name='Owner:', value=f"<:owner:730864906429136907>``{guild.owner}``", inline=False)
        e.add_field(name='Region:', value=f"📌 ``{r}``", inline=False)
        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)
        e.add_field(name='Members:', value=f"<:member:731190477927219231> ``{guild.member_count}`` **•**"
                                           f"   <:bot:703728026512392312> ``{bots}`` **•**"
                                           f"   👨 ``{humans}``",
                    inline=False)
        e.add_field(name='Roles:', value=f'<:roles:734232012730138744> ``{len(roles)}``', inline=False)
        e.add_field(name='Emojis:', value=f"<:emoji:734231060069613638> ``{len(emojis)}``", inline=False)
        e.add_field(name='Channels:', value=f"<:category:716057680548200468> ``{len(folders)}`` **•** "
                                            f"<:text_channel:703726554018086912> ``{len(channels)}`` **•** "
                                            f"<:voice_channel:703726554068418560> ``{len(vc)}``")
        e.add_field(name='Server Created:', inline=False,
                    value=f"🕒  "
                          f"``{guild.created_at.strftime('%a, %B %d %Y, %I:%M %p UTC')}``")
        e.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=e)

    @commands.command(aliases=['ab'])
    async def about(self, ctx):
        """Get basic information about NOVA"""
        pre = ctx.prefix
        guild = ctx.guild
        embed = discord.Embed(title='About NOVA', color=0x5643fd, timestamp=ctx.message.created_at,
                              description=f'My prefix for {guild.name} is ``{pre}``\nDo ``'
                                          f'{pre}help`` for a list of commands')
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/709922850953494598/f78ed19924e8c95abc30f406d47670d7'
                                '.png?size=1024')
        embed.set_author(name='Developed by YeetVegetabales#5313',
                         icon_url='https://cdn.discordapp.com/avatars/5693744'
                                  '29218603019/a_b6d992c79036b86d1ac49f27093b'
                                  'c813.gif?size=1024')
        embed.add_field(inline=False, name='Info',
                        value='NOVA is a general purpose discord bot that has tools to help you better moderate your '
                              'server as well as have a little fun')
        embed.add_field(name='Stats',
                        value=f'**•** ``{len(self.client.guilds)}`` servers with ``{len(self.client.users)}``'
                              f' total users',
                        inline=False)
        embed.add_field(name='Commands', value=f'**•** ``{len(self.client.commands)}`` commands with '
                                               f'``{len(self.client.cogs)}`` cogs', inline=False)
        embed.add_field(name='Other', value='<:news:730866149109137520> [Discord Server](https://discord.gg/Uqh9NXY)\n'
                                            '<:news:730866149109137520> [Invite Link](https://discor'
                                            'd.com/api/oauth2/authorize?client_id=709922850953494598&permissions=470150'
                                            '214&scope=bot)', inline=True)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
