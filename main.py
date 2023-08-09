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

#检定函数模式
checkmode = 1

#切换检定函数模式
@bot.command(name="setmode")
async def main(msg:Message,num:str):
    try:
        chat = int(num)
        if(chat == 1 or chat == 2):
            checkmode = chat
            str1 = ''
            if(chat == 1):
                str1 = "已切换房规至：模式"+str(chat)+"\n1~5为大成功，96~100为大失败"
            else:
                str1 = "已切换房规至：模式"+str(chat)+"\n1为大成功，100为大失败"
            await msg.reply(str1)
        else:
            raise Exception
    except:
        await msg.reply("输入格式有误，仅可输入1或2切换房规")

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

#/r 命令
@bot.command(name="r")
async def main(msg:Message,chat:str = ''):
    try:
        input = msg.content
        player = msg.author_id
        inputSplit = split.strSplit(input)
        dIndex = inputSplit.index('d')
        print("[0]="+inputSplit[0])
        #/r
        if(inputSplit[dIndex-1]=='/r'):
            num = int(inputSplit[dIndex+1])
            ValueR = random.randint(1,num)
            await msg.reply("掷出了D"+str(num)+"="+ValueR)
        #/r d    
        elif(inputSplit[dIndex-1].isdigit()):
            sum = 0
            listR = []
            for i in range(int(inputSplit[dIndex-1])):
                num = int(inputSplit[dIndex+1])
                ValueR = random.randint(1,num)
                listR.append(str(ValueR))
            for i in listR:
                sum += int(i)
            str1 = ','.join(listR)
            await msg.reply("掷出了3个D"+str(num)+"="+str(sum)+"("+str1+")")
    except Exception as e:
        await msg.reply("格式有误,检查输入格式")
        print(e)

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
            for key,value in playerDict[player].items():
                replyChat += key + ":" + value + "\n"
            await msg.reply(replyChat)
        #录卡
        else:
            tempList = split.strSplit(input)
            tempDict ={}
            if(len(tempList)%2!=0):
                raise Exception
            else:
                for i in range(2, len(tempList), 2):
                    tempDict[tempList[i]] = tempList[i+1]
                nameDict = {}
                nameDict[player] = tempDict
                print(tempList)
                print(tempDict)
                print(nameDict)
                playerInfo.input(nameDict)

    except Exception as e:
        print(e)
        await msg.reply("格式有误,检查输入格式")

logging.basicConfig(level='INFO')

bot.run()