from twitchio.ext import commands
from pathlib import Path
import asyncio
import random
import time

cooldown_time = [30, 1800]
command_used = {}

def cooldown(command, cooldown_time):
    if(command not in command_used or time.time() - command_used[command] > cooldown_time):
        command_used[command] = time.time()
        return True
    else:
        return False

def get_bot_path():
    CWD = Path(__file__).parents[0]
    return str(CWD)


comandos = [' !oibot',' !rolada',' !rars',' !addrars',' !comandos',' !roladaD20']
cooldown_commands = ['!addrars']

class Bot(commands.Bot):


    def __init__(self):
        nick = ''
        channel = ''
        with open(get_bot_path()+'\\config.secret') as secret:
            dic = {}
            texto = secret.readlines()
            for line in texto:
                key, value = line.split('=')
                value = value.rstrip('\n')
                dic[key] = value

        super().__init__(
            irc_token=dic['TOKEN'],
            client_id =dic['CLIENT_ID'],
            nick=dic['BOT_NICK'],
            prefix=dic['BOT_PREFIX'],
            initial_channels=[dic['CHANNEL']]
        )

        self.nick = dic['BOT_NICK']
        self.channel = dic['CHANNEL']

    async def event_ready(self):
        print(f"\n\n\n{self.nick} online!\n\n\n")
        ws = self._ws  # so eh necessario em event_ready
        await ws.send_privmsg(self.channel, f"O bot ta on 😎")

    async def event_message(self, ctx):
        '''Runs every time a message is sent in chat.'''
        print(ctx.author.name,ctx.content)
        var = ctx.content.split()
        if var[0] in cooldown_commands and cooldown(var[0],cooldown_time[0]):
            await self.handle_commands(ctx)
        elif var[0] in cooldown_commands and cooldown(var[0],cooldown_time[0]) == False:
            await ctx.channel.send(f'o comando {var[0]} está em cooldown de {cooldown_time[0]} segundos')
        else:
            await self.handle_commands(ctx)
                
        lembrete = 'Não esqueçam de beber água e ajeitar a postura 🥤🌺🧚'
        if cooldown(lembrete,cooldown_time[1]):
            await ctx.channel.send(lembrete)

    ''' oibot envia uma mensagem de olá '''
    @commands.command(name='oibot')
    async def test(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name} Kappa!')

    ''' rolada envia uma mensagem com um valor de 1 a 6 '''
    @commands.command(name='rolada')
    async def rolada(self, ctx):
        var = random.randint(1,6)
        await ctx.send(f'{ctx.author.name}, você tirou {var}! 🎲')

    ''' roladaD20 envia uma mensagem com um valor de 1 a 20 '''
    @commands.command(name='roladaD20')
    async def roladaD20(self, ctx):
        var = random.randint(1,20)
        await ctx.send(f'{ctx.author.name}, você tirou {var}! 🎲')
    
    ''' incrementa o numero de vezes que o rars travou '''
    @commands.command(name='addrars')
    async def addrars(self, ctx):
        with open(get_bot_path()+'\\rars.txt') as contador:
            inteiro = int(contador.read())
            inteiro += 1
        with open(get_bot_path()+'\\rars.txt', 'w') as contador:
            print('\n\n\n\nporraaaaaaaaa\n\n\n\n\n')
            contador.write(str(inteiro))
        await ctx.send(f'O RARS já travou {inteiro} vezes')


    ''' contagem de quantas vezes o rars travou '''
    @commands.command(name='rars')
    async def rars(self, ctx):
        with open(get_bot_path()+'\\rars.txt') as contador:
            inteiro = int(contador.read())
        await ctx.send(f'O RARS já travou {inteiro} vezes')

    ''' mostra lista de comandos '''
    @commands.command(name='comandos')
    async def comandos(self, ctx):
        string = 'Olá aqui está a lista de comandos que possuo:'
        for x in comandos:
            string += x
        await ctx.send(string)

        


bot = Bot()
bot.run()