def check(d,skill,mode=1):
    max_su = 5
    max_fu = 5
    if(mode == 2):
        max_su = 1
        max_fu = 1
    if( d <= 100 and d >= 100 - max_fu + 1):
        return "大失败！"
    elif( d < 100 - max_fu + 1 and d > skill):
        return "失败!"
    elif( d <= skill and d > 0.5*skill):
        return "成功！"
    elif( d <= 0.5*skill and d > 0.2*skill):
        return "困难成功！"
    elif( d <= 0.2*skill and d > max_su):
        return "极难成功！"
    elif( d <= max_su and d >= 0):
        return "大成功！"
    else:
        return "结果有误！"
