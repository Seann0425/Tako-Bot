import discord
import os
import requests
import json
import random
import base64
import asyncio
import random_word
from dotenv import load_dotenv, dotenv_values
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents = intents)

db = {}
db['fouls'] = ['靠北', '幹']
db['responding'] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' - ' + json_data[0]['a']
  return quote

def update_foul_words(foul_word):
  if 'fouls' in db.keys():
    fouls = db['fouls']
    fouls.append(foul_word)
    db['fouls'] = fouls
  else:
    db['fouls'] = [foul_word]

def delete_foul_words(foul_word):
  fouls = db['fouls']
  if foul_word in fouls:
    fouls.remove(foul_word)
    db['fouls'] = fouls

def RPS(user, bot):
  if user == bot:
    return 'Draw'
  
  elif user == '👊':
    if bot == '🖐️':
      return 'Lose!!'
    elif bot == "✌️":
      return "Win!!"
  
  elif user == "🖐️":
    if bot == "👊":
      return "Win!!"
    elif bot == "✌️":
      return "Lose!!"
  
  elif user == "✌️":
    if bot == "👊":
      return "Lose!!"
    elif bot == "🖐️":
      return "Win!!"
    
#bot ready
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = '如何成為一個好Bot', type = discord.ActivityType.watching))

#reaction to a specific message
@client.event
async def on_raw_reaction_add(payload):
  if payload.message_id == 1197077561251995678:
    guild = client.get_guild(payload.guild_id)
    channel = discord.utils.find(lambda ch : ch.id == payload.channel_id, guild.channels)
    
    if payload.emoji.name == '💚':
      role = discord.utils.get(guild.roles, name = '測試用身分組')
    else:
      role = discord.utils.get(guild.roles, name = payload.emoji.name)
    
    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.add_roles(role)
      else:
        await channel.send('找不到用戶')
    else:
      await channel.send('找不到身分組')

  #喵喵拳大隊用來領身分組的
  if payload.message_id == 1197177278271066284:
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
    channel = discord.utils.find(lambda ch : ch.id == payload.channel_id, guild.channels)

    if payload.emoji.id == 1175854902354911342:
      role = discord.utils.get(guild.roles, name = '最喜歡打扣了')
    elif payload.emoji.id == 1080465870259769354:
      role = discord.utils.get(guild.roles, name = '最喜歡微積分了')
    elif payload.emoji.id == 929042206583558184:
      role = discord.utils.get(guild.roles, name = '可憐社畜')
    elif payload.emoji.id == 1080465891965292544:
      role = discord.utils.get(guild.roles, name = '玩遊戲怎麼可以不揪')
    elif payload.emoji.id == 1196832403008782477:
      role = discord.utils.get(guild.roles, name = '最喜歡線代了')
    else:
      role = discord.utils.get(guild.roles, name = payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.add_roles(role)
      else:
        tmptxt = await channel.send('找不到用戶')
        await asyncio.sleep(5)
        await tmptxt.delete()
    else:
      tmptxt = await channel.send('找不到身分組')
      await asyncio.sleep(5)
      await tmptxt.delete()

#remove reaction to a specific message
@client.event
async def on_raw_reaction_remove(payload):
  #頂級章魚實驗室
  if payload.message_id == 1197077561251995678:
    guild = client.get_guild(payload.guild_id)
    channel = discord.utils.find(lambda ch : ch.id == payload.channel_id, guild.channels)

    if payload.emoji.name == '💚':
      role = discord.utils.get(guild.roles, name = '測試用身分組')
    else:
      role = discord.utils.get(guild.roles, name = payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.add_roles(role)
      else:
        await channel.send('找不到用戶')
    else:
      await channel.send('找不到身分組')

  #喵喵拳大隊
  if payload.message_id == 1197177278271066284:
    guild = client.get_guild(payload.guild_id)
    channel = discord.utils.find(lambda ch : ch.id == payload.channel_id, guild.channels)

    if payload.emoji.id == 1175854902354911342:
      role = discord.utils.get(guild.roles, name = '最喜歡打扣了')
    elif payload.emoji.id == 1080465870259769354:
      role = discord.utils.get(guild.roles, name = '最喜歡微積分了')
    elif payload.emoji.id == 929042206583558184:
      role = discord.utils.get(guild.roles, name = '可憐社畜')
    elif payload.emoji.id == 1080465891965292544:
      role = discord.utils.get(guild.roles, name = '玩遊戲怎麼可以不揪')
    elif payload.emoji.id == 1196832403008782477:
      role = discord.utils.get(guild.roles, name = '最喜歡線代了')
    else:
      role = discord.utils.get(guild.roles, name = payload.emoji.name)

    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.remove_roles(role)
      else:
        tmptxt = await channel.send('找不到用戶')
        await asyncio.sleep(5)
        await tmptxt.delete()
    else:
      tmptxt = await channel.send('找不到身分組')
      await asyncio.sleep(5)
      await tmptxt.delete()
  
#bot receives message
@client.event
async def on_message(message):
  #避免循環
  if message.author == client.user:
    return
  
  #hello
  if message.content.startswith('$hello'):
    #我的第一個指令
    await message.channel.send('hello:purple_heart: ')

  #help
  if message.content.startswith('$help'):
    #手動列出來，之後想研究其他排版方法。
    #像是利用表情符號來換頁之類的
    embed = discord.Embed(title = 'Command List', description = f'`$hello` 我會跟你說hello\n'
                          f'`$test` 你就自己test看看嘛\n'
                          f'`$inspireme` 心情不好的時候就隨便看點Quotes\n'
                          f'from **ZenQuotes**\n'
                          f'`$dice` 就字面上的意思\n'
                          f'`$wah` WAH!!\n'
                          f'`真不愧是` 真不愧是成大資工/電機大人\n'
                          f'`$report _word_` 新增不雅字眼\n'
                          f'`$delreport _word_` 刪除不雅字眼\n'
                          f'`$list` 列出不雅字眼\n'
                          f'`$gojo [-g word] [-s word] [-k word] [-t word] [-d word]` \n五條體產生器\n'
                          f'`$z` 我會跟你說晚安\n'
                          f'`$tex` 低配版LaTex渲染工具\n'
                          f'`$base64 -d/-e string` 我去夏威夷學過怎麼處理base64\n'
                          f'`$rps` 跟我一起玩猜拳\n'
                          f'`$random 複數選項` 幫你決定晚餐要吃什麼\n'
                          f'`$wordle` 跟Tako玩一場Wordle\n', color = 0x7c6c8d)
    await message.channel.send(embed = embed)

  #test, repeat same message
  if message.content.startswith('$test'):
    #只是想測試一下學python時學會的字串切割
    msg = message.content.split("$test ", 1)
    if(len(msg) > 1):
      await message.channel.send(msg[1])
    else:
      await message.channel.send("請在`$test `後面加點東西")

  #inspireme, some cool quotes
  if message.content.startswith('$inspireme'):
    #學習外部API的使用
    quote = get_quote()
    await message.channel.send(quote)

  #dice, roll a dice
  if message.content.startswith('$dice'):
    #最剛開始想做機器人就是想讓他幫我投骰子
    arg = message.content.split("$dice ", 1)
    if(len(arg) == 1):
      dice = [1,2,3,4,5,6]
      await message.channel.send(":game_die: " + str(random.choice(dice)))
    else:
      start = int(arg[1].split()[0])
      end = int(arg[1].split()[1])
      await message.channel.send(":game_die: " + str(random.randint(start, end)))

  #wah, WAH!!
  if message.content.startswith('$wah'):
    #WAH
    await message.channel.send('WAH!!:purple_heart:')

  #真不愧是
  # if message.content == '真不愧是':
  #   #靖棋說要實作的，幫他打完後面一串
  #   await message.channel.send('真不愧是成大資工/電機大人')

  #fouls check
  if db['responding'] == True:    
    if any(word in message.content for word in db['fouls']):
      #針對每個message檢查裡面有沒有字詞出現在不雅字眼列表裡
      #文字獄
      await message.channel.send('欸兄弟，注意一下你的用詞')

  #report, add new foul word
  if message.content.startswith('$report'):
    foul_word = message.content.split('$report ',1)[1]
    update_foul_words(foul_word)
    await message.channel.send('New foul word added.')

  #delreport, delete foul word
  if message.content.startswith('$delreport'):
    fouls = []
    if 'fouls' in db.keys():
      foul_word = message.content.split('$delreport ',1)[1]
      delete_foul_words(foul_word)
      fouls = db['fouls'].value
    await message.channel.send(fouls)

  #list, list the foul words
  if message.content.startswith('$list'):
    fouls = []
    if 'fouls' in db.keys():
      fouls = db['fouls'].value
    await message.channel.send('||'+str(db['fouls'].value)+'||')

  #gojo, 五條體
  if message.content.startswith('$gojo'):
    #利用前綴來自定五條體
    arg = message.content.split('$gojo ',1)[1].split() if len(message.content.split('$gojo ',1)) > 1 else []
    gojo = '五條'
    sukuna = '宿儺'
    kage = '十種影法術'
    time = '時間'
    disease = '疾病'
    idxG = arg.index('-g') if '-g' in arg else -1
    idxS = arg.index('-s') if '-s' in arg else -1
    idxK = arg.index('-k') if '-k' in arg else -1
    idxT = arg.index('-t') if '-t' in arg else -1
    idxD = arg.index('-d') if '-d' in arg else -1
    if idxG != -1:
      gojo = arg[idxG+1]
    if idxS != -1:
      sukuna = arg[idxS+1]
    if idxK != -1:
      kage = arg[idxK+1]
    if idxT != -1:
      time = arg[idxT+1]
    if idxD != -1:
      disease = arg[idxD+1]
    await message.channel.send(gojo + "：" + sukuna + "太強了\n而且" + sukuna + "還沒有使出全力的樣子\n對方就算沒有" + kage + "也會贏\n我甚至覺得有點對不起他\n我沒能在這場戰鬥讓" + sukuna + "展現他的全部給我\n殺死我的不是" + time + "或" + disease + "\n而是比我更強的傢伙，真是太好了")

  #z, good night
  if message.content.startswith('$z') or message.content.startswith('$Z'):
    #想睡了
    await message.channel.send('晚安:purple_heart: ')

  #nothing, telling users that they can ask for help
  if message.content == '$':
    #讓使用者知道有$help可以用這樣
    await message.channel.send('後面加個help怎麼樣')

  #tex, render latex image, &space;
  if message.content.startswith('$tex'):
    #利用codecogs的http渲染功能
    tex = message.content.split('$tex ',1)
    if len(tex)>1:
      TEX = tex[1].replace(' ', '&space;')
      await message.channel.send('https://latex.codecogs.com/png.image?\color{white}'+TEX)
    else:
      await message.channel.send('麻煩在後面加上LaTex語句')

  #embed, this is an embed test
  if message.content.startswith('$emb'):
    #測試emb功能
    embed = discord.Embed(title = 'Test', description = 'This is a test', color = 0x7c6c8d)
    await message.channel.send(embed = embed)

  #base64, encode and decode
  if message.content.startswith('$base64'):
    msg = message.content.split('$base64 ', 1)
    if(len(msg)>1):
      #確認後面有參數
      #判斷目的為編碼或解碼，否則提醒使用者
      if msg[1].startswith('-e'):
        base64_encode = msg[1].split('-e ', 1)
        if(len(base64_encode)>1):
          txt = base64_encode[1].encode('utf-8')
          base64_bytes = base64.b64encode(txt)
          base64_str = base64_bytes.decode('utf-8')
          await message.channel.send(base64_str)
        else:
          await message.channel.send('麻煩在後面加上要編碼的文字')
      elif msg[1].startswith('-d'):
        base64_decode = msg[1].split('-d ', 1)
        if(len(base64_decode)>1):
          txt = base64_decode[1].encode('utf-8')
          base64_bytes = base64.b64decode(txt)
          base64_str = base64_bytes.decode('utf-8')
          await message.channel.send(base64_str)
        else:
          await message.channel.send('麻煩在後面加上要解碼的文字')
      else:
        await message.channel.send('麻煩先根據要解碼或編碼加上-d或-e')
    else:
      await message.channel.send('麻煩在後面加上-d或-e以及要解碼或編碼的文字')

  #rps, rock, paper, scissors
  if message.content == '$rps':
    #generate an embed that includes game rules and place the emojis on it
    embed = discord.Embed(title = "猜拳囉！", url = "https://www.youtube.com/watch?v=AqQwmqHwtfA", description = 'React to this message with your choice!', color = 0x7c6c8d)
    embed.set_footer(text = 'This game is inspired by 閃電a')
    embed.set_author(name = message.author.display_name, icon_url = message.author.avatar.url)
    gameruleEmb = await message.channel.send(embed = embed)
    await gameruleEmb.add_reaction('👊')
    await gameruleEmb.add_reaction('🖐️')
    await gameruleEmb.add_reaction('✌️')
    await gameruleEmb.add_reaction('🤞')
    def check(reaction, user):
      return user == message.author and str(reaction.emoji) in ['👊','🖐️','✌️','🤞'] and reaction.message.id == gameruleEmb.id
    try:
      reaction, user = await client.wait_for('reaction_add', timeout = 20.0, check = check)
    except asyncio.TimeoutError:
      await message.channel.send('好吧，不想跟我玩也沒關係。')
    else:
      if(str(reaction.emoji) == '🤞'):
        await message.channel.send(random.choice(['好了啦，凡夫。乖乖猜拳啦。', "你不過是生在沒有我的時代的凡夫🤞"]))
      else:
        takoChoice = random.choice(['👊','🖐️','✌️'])
        await gameruleEmb.delete()
        resEmb = discord.Embed(title = '猜拳囉！', url = "https://www.youtube.com/watch?v=AqQwmqHwtfA", color = 0x7c6c8d)
        resEmb.set_author(name = message.author.display_name, icon_url = message.author.avatar.url)
        resEmb.add_field(name = "{0.display_name}'s Choice".format(message.author), value = str(reaction.emoji), inline = True)
        resEmb.add_field(name = "Tako's Choice", value = takoChoice, inline = True)
        result = RPS(str(reaction.emoji), takoChoice)
        if result == "Draw":
          resEmb.add_field(name = "Result", value = "Draw", inline = False)
        else:
          betterResult = "You " + result
          resEmb.add_field(name = "Result", value = betterResult, inline = False)  
        resEmb.set_footer(text = "This game is inspired by 閃電a")
        await message.channel.send(embed = resEmb)

  #random, get random choice
  if message.content.startswith("$random"):
    arg = message.content.split("$random ",1)
    if(len(arg)>1):
      choices = arg[1].split()
      await message.channel.send(random.choice(choices))
    else:
      await message.channel.send("麻煩在後面加上一個以上的選項，並以空格作區格。")

  #wordle, try to make some games
  #做成可以玩不同字長度的wordle
  #確保玩家猜得自在字典裡
  #介面美化
  if message.content == "$wordle":
    #get the word
    new_word = random_word.Wordnik().get_random_word(
      hasDictionaryDef = "true",
      minLength = 5,
      maxLength = 5
    ).lower()
    #先建一個pre在這邊，之後在while裡面用
    pre = await message.channel.send("隨便猜個字吧(0/6)")

    def check(m):
      return m.channel == message.channel and m.author == message.author

    grid = ""
    counter = 0
    guess = ""
    while(guess := (await client.wait_for('message', check = check)).content.lower())[8:] != new_word:
      if not guess.startswith("$wordle"):
        continue
      line = ""
      if len(guess[8:]) != 5:
        await message.channel.send("抱歉，我還只會玩5個字的Wordle。")
      else:
        counter += 1
        for expected, actual in zip(guess[8:], new_word):
          if expected == actual:
            line += ":green_square:"
          elif expected in new_word:
            line += ":yellow_square:"
          else:
            line += ":black_large_square:"
        grid += f"{line}\n"
        await pre.delete()
        pre = await message.channel.send("答題次數({}/6)\n".format(counter) + grid)
      if counter == 6:
        await message.channel.send("答案是{}".format(new_word))
        break
    if counter < 6 and guess.startswith("$wordle"):
      grid += f":green_square::green_square::green_square::green_square::green_square:\n"
      await message.channel.send("答題次數({}/6)\n".format(counter+1) + grid)

  #輸光
  if "輸光" in message.content:
    await message.channel.send("真的，輸光。:melting_face:")
  #怎麼贏
  if "怎麼贏" in message.content:
    await message.channel.send("到底怎麼贏。😫")
  #太強了
  if "太強了" in message.content:
    await message.channel.send("真的太強了啦😫")
  # 真不愧是
  if "真不愧是" in message.content:
    await message.channel.send(message.content + ':hot_face:')

client.run(os.environ['TOKEN'])