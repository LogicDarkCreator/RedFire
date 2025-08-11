# Import Libraries
import disnake
import asyncpraw
import json
import os
import asyncio
import dotenv
from disnake.ext import commands
from disnake.ui import Select
from dotenv import load_dotenv

# Load `.env` file
load_dotenv()

import config

REDDIT_MAIN = os.getenv("REDDIT_ID")
REDDIT_KEY = os.getenv("REDDIT_SECRET")
BOT_TOKEN = os.getenv("MAIN_TOKEN")

# Flags For Slash Commands
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

# Bots
reddit = asyncpraw.Reddit(
    client_id=REDDIT_MAIN,
    client_secret=REDDIT_KEY,
    user_agent='random_reddit_bot/0.0.0.1'
)

intents = disnake.Intents.default() # Connecting "Intents"
intents.message_content = True
bot = commands.Bot(
    command_prefix='$',
    intents=disnake.Intents.all(),
    status=disnake.Status.dnd,
    command_sync_flags=command_sync_flags
)

# Lists
memes=[]

# Dictionaries
server_roles={}

# Info
#project_news=1354348081620975730
#contributors=1354359418464112682
#rules=1354360914157240320
#staff=1355091478543601685
#contacts=1355096945726853283
#invites=1370076697482760225

# Appeals
#support=1359198641063198774
#ideas=1359198875415478552
#complaints=1359199116072325221
#donate_roles=1359199670987128912

# General
#commands_channels=1354400905830727710

# Administration
#logs=1354419015409209364
#admin_commands=1375060574240505968

# Events
# Memes
#@bot.event
#async def on_ready():
#    channel=bot.get_channel(1369621449232355398)
#    while True:
#        await asyncio.sleep(120)
#        memes_submissions=await reddit.subreddit("memes")
#        memes_submissions=memes_submissions.new(limit=1)
#        item=await memes_submissions.__anext__()
#        if item not in memes:
#            memes.append(item.title)
#            await channel.send(item.url)

# Welcome Message
# Rules Channel: 1354360914157240320
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1354359749814255777)
    content = member.mention
    embed = disnake.Embed(
        title=f'Добро пожаловать на дискорд сервере {member.guild}',
        description=f'Друг, приветствуем тебя на дискорд сервере майнкрафт проекта {member.guild}',
        color=disnake.Color.from_rgb(255, 107, 0)
    )
    embed.add_field(name="",
                    value="Тут ты сможешь погрузиться в удивительный мир творчества и приключений. Наше сообщество состоит из людей, увлеченных игрой, которые ценят дружелюбие, творчество и взаимопомощь.\nЗдесь ты найдешь множество возможностей для общения, игры, строительства и взаимодействия с другими участниками. Не стесняйся задавать вопросы, делиться своими идеями и присоединяться к нашим событиям и мероприятиям.\n",
                    inline=False
                    )
    embed.add_field(
        name="",
        value="",
        inline=False
    )
    embed.add_field(
        name="Прежде чем начать, пожалуйста, ознакомься с правилами сервера в канале <#1354360914157240320> и получи необходимые роли в самой первой вкладке в списке каналов.",
        value="Мы рады, что ты с нами, и надеемся, что твое пребывание здесь будет веселым и незабываемым!",
        inline=False
        )
    embed.add_field(
        name="",
        value="",
        inline=False
    )
    embed.add_field(name=f"Приятного времяпрепровождения на disnake сервере {member.guild}!",
                    value="",
                    inline=False
                    )
    member_counter = disnake.ui.Button(label=f"Вы стали {member.guild.member_count}-м участником!", disabled=True, style=disnake.ButtonStyle.secondary)
    components = disnake.ui.ActionRow(member_counter) # Wrap the button in an ActionRow
    await channel.send(components=components, embed=embed, content=content)


#Logger
LOG_CHANNEL_ID = 1354419015409209364
@bot.event
async def on_guild_role_create(role):
    async for entry in role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_create):
        creator = entry.user
        embed = disnake.Embed(
            title="Роль создана!",
            description=f"Роль `{role.name}` была создана {creator.mention}.",
            color=disnake.Color.green()
        )
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)
@bot.event
async def on_guild_role_update(before, after):
    changes = []
    if before.name != after.name:
        changes.append(f"Имя роли изменено с '{before.name}' на '{after.name}'.")
    if before.color != after.color:
        changes.append(f"Цвет роли изменен.")
    if before.hoist != after.hoist:
        changes.append(f"Статус отображения роли изменен.")
    if changes:
        embed = disnake.Embed(
            title="Роль изменена!",
            description=f"Роль '{before.name}' была изменена.",
            color=disnake.Color.yellow()
        )
        for change in changes:
            embed.add_field(name="Изменение", value=change)
        async for entry in after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_update):
            modifier = entry.user
            embed.add_field(name="Изменил", value=modifier.mention)
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_role_delete(role):
    async for entry in role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_delete):
        deleter = entry.user
        embed = disnake.Embed(
            title="Роль удалена!",
            description=f"Роль '{role.name}' была удалена {deleter.mention}.",
            color=disnake.Color.red()
        )
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    # Get the guild (server) the channel was created in
    guild = channel.guild

    # Fetch the audit logs for the channel creation
    async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create):
        # Now you can access the entry details
        creator = entry.user  # This will give you the user who created the channel
    embed = disnake.Embed(
        title="Канал создан!",
        description=f"Канал '{channel.name}' был создан {creator.mention}"
    )
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)

# Bot Commands
# Rules
@bot.command()
async def rules(ctx):
    """
    Send rules
    :param ctx: delete executed command and send server guidelines
    """
    await ctx.message.delete()

    embed = disnake.Embed(
        title=f"Правила сервера {ctx.guild.name}",
        description="",
        color=disnake.Color(0x77C40A)
    )
    embed.add_field(
        name="**-- Раздел 1. Основное --**",
        value="**|- Общение -|"
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="**-- Раздел 2. Контент --**",
        description="",
        color=disnake.Color(0x77C40A)
    )
    await ctx.send(embed=embed)

    embed = disnake.Embed(
        title="**-- Раздел 3. Голосовые чаты --**",
        description="",
        color=disnake.Color(0x77C40A)
    )
    embed.add_field(
        name="1. Музыка, громкие звуки и раздражающие шумы запрещены",
        value="**| `Предупреждение` -> `Мут 2 часа`**",
        inline=False
    )
    embed.add_field(
        name="2. Ваш микрофон должен быть настроен без лишних шумов, эха и перегрузов",
        value="**| `Предупреждение` -> `Мут 3 часа`**",
        inline=False
    )
    embed.add_field(
        name="3. Запрещено постоянно переключаться между голосовыми каналами",
        value="**| `Предупреждение` -> `Мут 6 часа`**",
        inline=False
    )
    embed.add_field(
        name="4. Использование SoundBoard, звуковых эффектов и прочих аудио-манипуляций без меры недопустимо",
        value="**| `Предупреждение` -> `Мут 4 часа`**",
        inline=False
    )
    embed.add_field(
        name="5. Перебивать других участников без причины запрещено",
        value="**| `Предупреждение` -> `Мут 1 час -> Мут: +2 часа`**",
        inline=False
    )
    discord_guidelines = disnake.ui.Button(label="Discord Guidelines", url="https://discord.com/guidelines", style=disnake.ButtonStyle.link)
    # Wrap the button in an ActionRow
    components = disnake.ui.ActionRow(discord_guidelines)
    await ctx.send(embed=embed, components=components)



@bot.command()
@commands.has_permissions(administrator=True)
async def roles(ctx):
    await ctx.message.delete()
    embed = disnake.Embed(
        title="Роли сервера",
        description=f"<@&{config.Player}>: обычный игрок сервера с базовыми правами",
        color=disnake.Color(0x53FFC7)
    )
    #button = disnake.ui.Button
    await ctx.send(embed=embed)

bot.run(BOT_TOKEN)