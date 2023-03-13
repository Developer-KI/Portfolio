import math
import random

import discord
from discord.ext import commands

daniel = None

bot = commands.Bot(command_prefix="!")
bot.remove_command('help')
bot.case_insensitive = False
bot.self_bot = False

border = ":white_large_square:"
blank = ":black_large_square:"
cross = ":x:"
circle = ":o:"

T_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
X_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
O_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

challenger = None
challenged = None

active_game = False
turn = False

played = 0


@bot.event
async def on_ready():
    print("Bot is Ready!")


def Tic_Tac_Toe(row, column, preview=False):
    global turn, challenger, challenged, T_board, played

    embedVar = discord.Embed(title="Tic Tac Toe", description="A game of Tic Tac Toe.", color=discord.Color.random())

    played = 0

    if preview is False:
        if turn:
            T_board[row][column] = 1
            embedVar.add_field(name="Player Turn:", value="O", inline=False)
        else:
            T_board[row][column] = 2
            embedVar.add_field(name="Player Turn:", value="X", inline=False)
    else:
        preview = False

    embedVar.insert_field_at(index=0, name="Info:", value="To choose a square type !inp <number>(ex. !inp 2)",
                             inline=False)
    embedVar.insert_field_at(index=0, name="Game:", value=game_render(), inline=False)
    embedVar.set_footer(text=f'Game of {challenger.name} and {challenged.name}')

    for _row in range(0, 3):
        for _column in range(0, 3):
            if T_board[_row][_column] == 0:
                played = played + 1
            elif T_board[_row][_column] == 2:
                O_board[_row * 3 + _column] = 1
            elif T_board[_row][_column] == 1:
                X_board[_row * 3 + _column] = 1

    return embedVar


def Tic_Tac_Toe_Boolean(input_board):
    if (input_board[0] != 0 and input_board[1] != 0 and input_board[2] != 0) or (
            input_board[3] != 0 and input_board[4] != 0 and input_board[5] != 0) or (
            input_board[6] != 0 and input_board[7] != 0 and input_board[8] != 0):
        return True
    elif (input_board[0] != 0 and input_board[3] != 0 and input_board[6] != 0) or (
            input_board[1] != 0 and input_board[4] != 0 and input_board[7] != 0) or (
            input_board[2] != 0 and input_board[5] != 0 and input_board[8] != 0):
        return True
    elif (input_board[0] != 0 and input_board[4] != 0 and input_board[8] != 0) or (
            input_board[2] != 0 and input_board[4] != 0 and input_board[6] != 0):
        return True
    else:
        return False


async def Tic_Tac_Toe_Check(ctx):
    embedVar = discord.Embed(title="Tic Tac Toe", description="A game of Tic Tac Toe.", color=discord.Color.random())

    if Tic_Tac_Toe_Boolean(X_board):
        embedVar.insert_field_at(index=0, name="Winner:", value="X Won!", inline=False)
        embedVar.insert_field_at(index=0, name="Game:", value=game_render(), inline=False)
        embedVar.set_footer(text=f'Game of {challenger.name} and {challenged.name}')
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embedVar)
        Tic_Tac_Toe_Reset()

    elif Tic_Tac_Toe_Boolean(O_board):
        embedVar.insert_field_at(index=0, name="Winner:", value="O Won!", inline=False)
        embedVar.insert_field_at(index=0, name="Game:", value=game_render(), inline=False)
        embedVar.set_footer(text=f'Game of {challenger.name} and {challenged.name}')
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embedVar)
        Tic_Tac_Toe_Reset()

    elif played == 0:
        embedVar.insert_field_at(index=0, name="Winner:", value="Draw!", inline=False)
        embedVar.insert_field_at(index=0, name="Game:", value=game_render(), inline=False)
        embedVar.set_footer(text=f'Game of {challenger.name} and {challenged.name}')
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embedVar)
        Tic_Tac_Toe_Reset()


def Tic_Tac_Toe_Reset():
    global challenged, challenger, active_game, turn, T_board, X_board, O_board, played
    challenger = None
    challenged = None
    active_game = False
    turn = False
    T_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    X_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    O_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    played = 0


def game_render():
    global X_board, O_board, T_board, played
    game_output = border + border + border + border + border + "\n" + border

    for row in T_board:
        for tile in row:
            if tile != 1 and tile != 2:
                game_output = game_output + blank
            elif tile == 1:
                game_output = game_output + cross
            elif tile == 2:
                game_output = game_output + circle

        game_output = game_output + border + "\n" + border

    game_output = game_output + border + border + border + border

    return game_output


@bot.command(aliases=['invite'], description="Play a game of Tic Tac Toe with a member of your discord!")
async def Tic_Tac_Toe_Challenge(ctx, member: discord.Member):
    global challenged, challenger, active_game
    if not active_game and ctx.message.author != member:
        challenger = ctx.message.author
        challenged = member

        await ctx.send(f'{challenger.mention} challenged {challenged.mention} to a game of Tic Tac Toe!')
    else:
        await ctx.send(f'Dont challenge yourself or try to challenge someone when there arent any active games!')


@bot.command(aliases=['acc'], description="Accept a challenge")
async def Tic_Tac_Toe_Accept(ctx):
    global challenged, challenger, active_game
    if ctx.message.author == challenged:
        await ctx.send(f'{challenger.mention} {challenged.name} accepted the challenge and has to make a move.')
        active_game = True
        await ctx.send(embed=Tic_Tac_Toe(row=0, column=0, preview=True))


@bot.command(aliases=['dec'], description="Decline a challenge")
async def Tic_Tac_Toe_Decline(ctx):
    global challenged, challenger, active_game
    if ctx.message.author == challenged:
        await ctx.send(f'{challenger.mention} {challenged.name} declined the challenge.')
        Tic_Tac_Toe_Reset()


@bot.command(aliases=['inp'], description="Make your turns during a game of Tic Tac Toe!")
async def Tic_Tac_Toe_Input(ctx, number=0):
    global turn, active_game, challenged, challenger

    row = math.floor((number - 1) / 3)
    column = (number - 1) - (row * 3)

    if active_game and (ctx.message.author == challenged or ctx.message.author == challenger):
        if turn:
            if ctx.message.author == challenger:
                if 1 <= number <= 9 and T_board[row][column] == 0:
                    turn = False
                    await ctx.send(embed=Tic_Tac_Toe(row=row, column=column))
                    await Tic_Tac_Toe_Check(ctx)
                else:
                    await ctx.send(f'{challenger.mention} Try input something between 1 and 9, which isnt already '
                                   f'taken. (ex. !inp 2)')
            else:
                await ctx.send(f'{challenger.mention} must make the move')
        else:
            if ctx.message.author == challenged:
                if 1 <= number <= 9 and T_board[row][column] == 0:
                    turn = True
                    await ctx.send(embed=Tic_Tac_Toe(row=row, column=column))
                    await Tic_Tac_Toe_Check(ctx)
                else:
                    await ctx.send(f'{challenged.mention} Try input something between 1 and 9, which isnt already '
                                   f'taken. (ex. !inp 2)')
            else:
                await ctx.send(f'{challenged.mention} must make the move')
    else:
        await ctx.send(f'You are not a part of an active game.')


@bot.command(aliases=['exit'], description="Abandon your game.")
async def Tic_Tac_Toe_Exit(ctx):
    global challenged, challenger, active_game
    if ctx.message.author == challenger and active_game == True:
        await ctx.send(f'{challenged.mention} has won!')
        Tic_Tac_Toe_Reset()
    elif ctx.message.author == challenged and active_game == True:
        await ctx.send(f'{challenger.mention} has won!')
        Tic_Tac_Toe_Reset()
    else:
        await ctx.send(f'You are not a part of an active game.')


@bot.command(aliases=['8ball'], description="Ask a question the EightBall!")
async def Eight_Ball(ctx, *, question):
    responses = ["It is certain.", "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@bot.command(description="Sends an embed message with info")
async def h(ctx):
    embedVar = discord.Embed(title=":small_orange_diamond: Minigame Bot",
                             description="This minigame bot enables you to play "
                                         "different minigames such as Tic Tac Toe, "
                                         "Eightball, "
                                         "etc.", colour=discord.Color.blue())
    embedVar.set_author(name="Help")
    embedVar.add_field(name=":small_orange_diamond: Tic Tac Toe:",
                       value="!invite <member> - challenges a discord member\n"
                             "!acc - accepts a sent challenge\n"
                             "!dec - declines a sent challenge\n"
                             "!inp <number> - get your input during game\n"
                             "!exit - abandons your current game", inline=False)
    embedVar.add_field(name=":small_orange_diamond: Eightball:", value="!8ball <question> - answers your question",
                       inline=False)
    embedVar.set_footer(text="created by DaVirtualDonkey",
                        icon_url="https://icon-library.com/images/yellow-discord-icon/yellow-discord-icon-6.jpg")
    embedVar.set_thumbnail(
        url="https://www.printworksmarket.com/thumb/2868/1024x0/PW00397---Classic---Tic-Tac-Toe-pieces.jpg")

    await ctx.send(embed=embedVar)


bot.run("ODIyNTUxNTE1MjU1Nzk5ODA4.YFT6yw.pnk7L25EmVqyowozOY0ZYcDoLYA")
# bot.run("ODQ0ODMyODY3NTMxMjI3MTg3.YKYJ6w.RQUIitGVLBzyiuLy3Yq88GHnhK4")
