import re
 
 
def strSplit(s:str):
    return re.findall(r'\d+|[a-zA-Z]+|[^a-zA-Z\d\s]+',s)
