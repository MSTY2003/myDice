from khl import Bot,Message
import json
import logging
import random
import split
import playerInfo
from check import check

with open('config.json','r',encoding='utf8') as f:
    config = json.loads(f.read())

max_su = 5
max_fu = 5

bot = Bot(token=config['token'])

#角色卡dict
playerDict = playerInfo.readInfo()

#用户绑定角色dict
userPc = {}

#检定函数模式
checkmode = 1


def updatePlayerInfo(dict):
    playerInfo.input(dict)


#切换检定函数模式
@bot.command(name="setmode")
async def main(msg: Message, num: str):
    try:
        chat = int(num)
        str1 = ''

        if chat == 1:
            str1 = "已切换房规至：模式1\n1~5为大成功，96~100为大失败"
        elif chat == 2:
            str1 = "已切换房规至：模式2\n1为大成功，100为大失败"
        else:
            raise Exception("输入格式有误，仅可输入1或2切换房规")
        checkmode = chat
        await msg.reply(str1)
    except Exception as e:
        await msg.reply(str(e))

@bot.command(name="getmode")
async def main(msg:Message):
    str1 = ''
    try:
        chat = checkmode
        if(chat == 1):
            str1 = "当前房规为：模式"+str(chat)+"\n1~5为大成功，96~100为大失败"
        else:
            str1 = "当前房规为：模式"+str(chat)+"\n1为大成功，100为大失败"
    except Exception as e:
        await msg.reply("格式有误,检查输入格式")
        print(e)

@bot.command(name="r")
async def main(msg: Message, chat: str = ''):
    try:
        input_text = msg.content
        player = msg.author_id
        input_split = split.strSplit(input_text)
        print(input_split)

        if len(input_split) == 2 and input_split[0] == '/' and input_split[1] == 'r' and 'd' not in input_split:
            print("s1")
            num_rolls = 1
            die_sides = 100
        elif len(input_split) == 4 and input_split[0] == '/' and input_split[1] == 'r' and input_split[2] == 'd':
            print("s2")
            num_rolls = 1
            die_sides = int(input_split[3])
        elif 'd' in input_split:
            print("s3")
            d_index = input_split.index('d')

            if input_split[d_index - 1].isdigit():
                print("p1")
                num_rolls = int(input_split[d_index - 1])
                die_sides = int(input_split[d_index + 1])
            else:
                raise ValueError("格式有误，请检查输入格式1")
        else:
            raise ValueError("格式有误，请检查输入格式2")

        rolls = [random.randint(1, die_sides) for _ in range(num_rolls)]
        roll_str = ','.join(map(str, rolls))
        total_sum = sum(rolls)
        await msg.reply(f"掷出了{num_rolls}个D{die_sides}={total_sum}({roll_str})")
    except Exception as e:
        await msg.reply(str(e))

@bot.command(name="ra")
async def main(msg:Message,chat:str):
    try:
        input = msg.content
        player = msg.author_id
        #取得/ra 后描述的技能名称
        skill = playerDict[player][chat]
        print(skill)
        d = random.randint(1,100)
        str1 = check(d,int(skill),checkmode)
        await msg.reply("投掷出了D100="+str(d)+",结果为："+str1)
    except Exception as e:
        print(e)
        await msg.reply("格式有误,检查输入格式")

#pc命令：角色卡相关内容
@bot.command(name="pc")
async def main(msg:Message,command1:str,command2:str=''):
    try:
        player = msg.author_id
        playerDict = playerInfo.readInfo()

        #用户第一次使用时创建数据
        if player not in playerDict:
            print("第一次")
            tempDict = {}
            tempDict[player] = {}
            playerInfo.input(tempDict)

        #new
        if(command1 == "new"):
            if(command2 == ''):
                msg.reply("角色名不能为空！")
            else:
                pc = {}
                pc[command2]={}
                playerInfo.inputPlayerInfo(player,pc)
                await msg.reply("创建角色：“"+command2+"”成功!")
        elif(command1 == "tag"):
            if command2 in playerDict[player]:
                userPc[player]=command2
                await msg.reply("绑定角色“"+command2+"”成功!")
            else:
                await msg.reply("绑定角色失败,角色不存在!")
        elif(command1 == "list"):
            tempStr = "角色列表：\n"
            for key in playerDict[player].keys():
                tempStr += key
                try:
                    if(key == userPc[player]):
                        tempStr +="[当前角色]"
                except:
                    tempStr +="[未绑定]"
                    print("list命令出错")
                tempStr += " "
            await msg.reply(tempStr)
            print(key)
            
            

    except Exception as e:
        print(e)
        await msg.reply("操作失败!")

#st命令：录入属性
@bot.command(name="st")
async def main(msg:Message,chat:str):
    #每次录卡更新预读取字典
    playerDict = playerInfo.readInfo()
    try:
        input = msg.content
        player = msg.author_id
        #查询功能
        if(chat == "info"):
            replyChat = ''
            for key,value in playerDict[player][userPc].items():
                replyChat += key + ":" + value + "\n"
            await msg.reply(replyChat)
        #录卡
        else:
            #读入属性
            tempList = split.strSplit(input)
            print(tempList)
            #内容不成对则格式错误
            if(len(tempList)%2!=0):
                raise Exception
            else:
                pc = userPc[player]
                print(playerDict,player,userPc)
                playerInfo.getStDict(playerDict,player,pc,tempList)
                playerInfo.input(playerDict)
                await msg.reply("属性写入成功!")

    except Exception as e:
        print(e)
        await msg.reply("格式有误,检查输入格式")

logging.basicConfig(level='INFO')

bot.run()