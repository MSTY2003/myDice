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
        try:
            dIndex = inputSplit.index('d')
        except:
            #/r
            if(inputSplit[1]=='r'):
                ValueR = random.randint(1,100)
                await msg.reply("掷出了D100"+"="+str(ValueR))
        #/r d    
        if(inputSplit[dIndex-1].isdigit()):
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
            stDict ={}
            #内容不成对则格式错误
            if(len(tempList)%2!=0):
                raise Exception
            else:
                for i in range(2, len(tempList), 2):
                    stDict[tempList[i]] = tempList[i+1]
                playerDict[player][userPc] = stDict
                print(stDict)
                print(playerDict)
                playerInfo.input(playerDict)

    except Exception as e:
        print(e)
        await msg.reply("格式有误,检查输入格式")

logging.basicConfig(level='INFO')

bot.run()