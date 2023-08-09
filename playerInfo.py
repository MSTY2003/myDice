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
    
def readInfo():
     with open("playerinfo.json","r") as f:
            content = json.load(f)
            return content
