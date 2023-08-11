import json

def input(dict1):
    isDict = {'a':1}
    if(type(dict1)==type(isDict)):
        content = {}
        #读入数据为字典
        with open("playerinfo.json","r") as f:
            content = json.load(f)
        #追加数据
        content.update(dict1)
        #写入文件
        with open("playerinfo.json",'w') as f1:
            json.dump(content,f1,ensure_ascii=False)
            print("文件写入完成")
    else:
        raise Exception

def inputPlayerInfo(userId,playerDict):
    with open("playerinfo.json","r") as f:
        content = json.load(f)
    content[userId].update(playerDict)
    with open("playerinfo.json",'w') as f1:
            json.dump(content,f1,ensure_ascii=False)
            print("角色数据写入完成")

def readInfo():
     with open("playerinfo.json","r") as f:
            content = json.load(f)
            return content
     
def readPc():
    try:
        with open("playerinfo.json","r") as f:
            content = json.load(f)
            tempList = []
            for key in content.key:
                tempList.append(key)
            return tempList
    except Exception as e:
        print(e)