import discord
import random
import asyncio
import json
from discord.ext import commands
from secrets import *


class economy(commands.Cog):
    """NOVA's special economy system."""

    def __init__(self, client):
        self.client = client
        self.coin = "<:coin:781367758612725780>"

    @commands.command()
    async def create(self, ctx):
        """Create your bank account."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) in money.keys():
            return await ctx.send("You can't create a bank account if you already have one dumbo. "
                                  "Use `n.balance` to see how much money you have.")
        else:
            money[str(ctx.message.author.id)] = {"wallet": 100, "bank": 0}
            econ_data = open("economy.json", "w")
            json.dump(money, econ_data)
            econ_data.close()
            return await ctx.send(f"Your account has been created! \nYou have been granted {self.coin}100 "
                                  f"coins in your wallet to start. \nUse `n.balance` to check how much money you have!")

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        user = member or ctx.message.author
        """"Check how much money you have."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        elif member and str(member.id) not in money.keys():
            return await ctx.send("This user does not have an account!")
        else:
            wallet_amount = money[str(user.id)]['wallet']
            bank_amount = money[str(user.id)]['bank']
            embed = discord.Embed(title=f"{user.display_name}'s Balance", color=0x5643fd,
                                  timestamp=ctx.message.created_at)
            embed.add_field(name="Wallet Amount", value=f"{self.coin}`{wallet_amount:,}`", inline=False)
            embed.add_field(name="Bank Amount", value=f"{self.coin}`{bank_amount:,}`", inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            return await ctx.send(embed=embed)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, deposit_amount):
        """Move money from your wallet to your bank."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            if deposit_amount == 'all':
                new_amount = money[str(ctx.message.author.id)]['wallet']
                wallet_amount = 0
                bank_amount = int(money[str(ctx.message.author.id)]['bank']) + int(new_amount)
                money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                money[str(ctx.message.author.id)]['bank'] = bank_amount
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                return await ctx.send(f"{self.coin}`{new_amount:,}` has been deposited into your bank.\n"
                                      f"Your new bank balance is {self.coin}`{bank_amount:,}`.")
            try:
                amount = int(deposit_amount)
                if amount > money[str(ctx.message.author.id)]['wallet']:
                    return await ctx.send("You can't deposit more money than you own. \n"
                                          "Try again with a smaller amount "
                                          "or use `n.withdraw <amount>`.")
                elif amount < 1:
                    return await ctx.send("You can't deposit nothing. Try again with a bigger amount.")
                else:
                    wallet_amount = int(money[str(ctx.message.author.id)]['wallet']) - int(amount)
                    bank_amount = int(money[str(ctx.message.author.id)]['bank']) + int(amount)
                    money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                    money[str(ctx.message.author.id)]['bank'] = bank_amount
                    econ_data = open("economy.json", "w")
                    json.dump(money, econ_data)
                    econ_data.close()
                    return await ctx.send(f"{self.coin}`{amount:,}` has been deposited into your bank.\n"
                                          f"Your new bank balance is {self.coin}`{bank_amount:,}`.")
            except ValueError:
                return await ctx.send("Only numbers can be used to deposit.")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, withdraw_amount):
        """Move money from your bank to your wallet."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            if withdraw_amount == 'all':
                new_amount = money[str(ctx.message.author.id)]['bank']
                bank_amount = 0
                wallet_amount = int(money[str(ctx.message.author.id)]['wallet']) + int(new_amount)
                money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                money[str(ctx.message.author.id)]['bank'] = bank_amount
                econ_data = open("economy.json", "w")
                json.dump(money, econ_data)
                econ_data.close()
                return await ctx.send(f"{self.coin}`{new_amount:,}` has been added to your wallet.\n"
                                      f"Your new wallet balance is {self.coin}`{wallet_amount:,}`.")
            try:
                amount = int(withdraw_amount)
                if amount > money[str(ctx.message.author.id)]['bank']:
                    return await ctx.send("You can't withdraw more money than you own. \n"
                                          "Try again with a smaller amount "
                                          "or use `n.deposit <amount>`.")
                elif amount < 1:
                    return await ctx.send("You can't withdraw nothing. Try again with a bigger amount.")
                else:
                    bank_amount = int(money[str(ctx.message.author.id)]['bank']) - int(amount)
                    wallet_amount = int(money[str(ctx.message.author.id)]['wallet']) + int(amount)
                    money[str(ctx.message.author.id)]['bank'] = bank_amount
                    money[str(ctx.message.author.id)]['wallet'] = wallet_amount
                    econ_data = open("economy.json", "w")
                    json.dump(money, econ_data)
                    econ_data.close()
                    return await ctx.send(f"{self.coin}`{amount:,}` has been moved to your wallet.\n"
                                          f"Your new wallet balance is {self.coin}`{wallet_amount:,}`.")
            except ValueError:
                return await ctx.send("Only numbers can be used to withdraw.")

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def beg(self, ctx):
        """Beg for money like that weird homeless dude on the street corner."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            person = ['stranger', 'random dude', 'stalker', 'simp', 'weirdo', 'loser', 'police officer', 'young child']
            gift = random.randint(1, 75)
            money[str(ctx.message.author.id)]['wallet'] += gift
            econ_data = open("economy.json", "w")
            json.dump(money, econ_data)
            econ_data.close()
            return await ctx.send(f"A {random.choice(person)} gave you {self.coin}`{gift}` for your wallet.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def timely(self, ctx):
        """Claim your free money."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        if str(ctx.message.author.id) not in money.keys():
            return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
        else:
            money[str(ctx.message.author.id)]['wallet'] += 250
            econ_data = open("economy.json", "w")
            json.dump(money, econ_data)
            econ_data.close()
            return await ctx.send(f"{self.coin}`250` has been added to your balance. \n"
                                  f"Check back in 1 hour to claim it again!")

    @commands.command(aliases=['bet', 'wager'])
    async def roll(self, ctx, amount):
        """Bet all of your money away."""
        econ_data = open("economy.json", "r")
        money = json.load(econ_data)
        econ_data.close()
        try:
            if str(ctx.message.author.id) not in money.keys():
                return await ctx.send("You haven't created an account yet! Run `n.create` to do so.")
            else:
                if amount == 'all':
                    wager_amount = money[str(ctx.message.author.id)]['wallet']
                    if money[str(ctx.message.author.id)]['wallet'] < 100:
                        return await ctx.send(f"You must have at least {self.coin}`100` in your wallet to play.")
                    roll = random.randint(0, 100)
                    if 0 <= roll <= 33:
                        money[str(ctx.message.author.id)]['wallet'] -= wager_amount
                        ret = f'You rolled `{roll}` so you lost all of your wager.'
                        gain = f"{self.coin}`{wager_amount:,}` has been deducted from your balance."
                        econ_data = open("economy.json", "w")
                        json.dump(money, econ_data)
                        econ_data.close()
                    elif 66 <= roll <= 100:
                        money[str(ctx.message.author.id)]['wallet'] += wager_amount
                        ret = f'You rolled `{roll}` so your wager was doubled. Congratulations!'
                        gain = f"{self.coin}`{wager_amount:,}` has been added to your balance."
                        econ_data = open("economy.json", "w")
                        json.dump(money, econ_data)
                        econ_data.close()
                    else:
                        ret = f"You rolled `{roll}` so you did not lose or gain any money."
                        gain = f"{self.coin}`0` has been added to your balance."
                    embed = discord.Embed(color=0x5643fd, title=f"You rolled {roll}",
                                          timestamp=ctx.message.created_at,
                                          description=f"➤ Rolling a `33` and below loses all of your wager\n"
                                                      f"➤ Rolling a `66` and above doubles your wager\n"
                                                      f"➤ Rolling a `34-65` loses you nothing")
                    embed.add_field(name="Your Returns", inline=False,
                                    value=f"{ret}\n{gain}\nYou now have a wallet balance of "
                                          f"{self.coin}`{money[str(ctx.message.author.id)]['wallet']:,}`")
                    embed.set_thumbnail(url="https://imgur.com/dTY0Cvv.png")
                    await ctx.send(embed=embed)
                else:
                    wager_amount = int(amount)
                    if wager_amount >= money[str(ctx.message.author.id)]['wallet']:
                        return await ctx.send("You cannot bet more than you have in your wallet")
                    elif money[str(ctx.message.author.id)]['wallet'] < 100:
                        return await ctx.send(f"You must have at least {self.coin}`100` in your wallet to play.")
                    roll = random.randint(0, 100)
                    if 0 <= roll <= 33:
                        money[str(ctx.message.author.id)]['wallet'] -= wager_amount
                        ret = f'You rolled `{roll}` so you lost all of your wager.'
                        gain = f"{self.coin}`{wager_amount:,}` has been deducted from your balance."
                        econ_data = open("economy.json", "w")
                        json.dump(money, econ_data)
                        econ_data.close()
                    elif 66 <= roll <= 100:
                        money[str(ctx.message.author.id)]['wallet'] += wager_amount
                        ret = f'You rolled `{roll}` so your wager was doubled. Congratulations!'
                        gain = f"{self.coin}`{wager_amount:,}` has been added to your balance."
                        econ_data = open("economy.json", "w")
                        json.dump(money, econ_data)
                        econ_data.close()
                    else:
                        ret = f"You rolled `{roll}` so you did not lose or gain any money."
                        gain = f"{self.coin}`0` has been added to your balance."
                    embed = discord.Embed(color=0x5643fd, title=f"You rolled {roll}",
                                          timestamp=ctx.message.created_at,
                                          description=f"➤ Rolling a `33` and below loses all of your wager\n"
                                                      f"➤ Rolling a `66` and above doubles your wager\n"
                                                      f"➤ Rolling a `34-65` loses you nothing")
                    embed.add_field(name="Your Returns", inline=False,
                                    value=f"{ret}\n{gain}\nYou now have a wallet balance of "
                                          f"{self.coin}`{money[str(ctx.message.author.id)]['wallet']:,}`")
                    embed.set_thumbnail(url="https://imgur.com/dTY0Cvv.png")
                    await ctx.send(embed=embed)
        except ValueError:
            return await ctx.send("You can only bet with numbers!")


def setup(client):
    client.add_cog(economy(client))
