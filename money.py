import json
import os
def get_err_lang():
    with open(os.path.join("code", "lang","lang.json"),"r",encoding="utf8") as f:
        err = json.loads(f.read())
    return err
# Đọc thông tin túi tiền
def openBank():
    """Đọc thông tin túi tiền"""
    with open(os.path.join("code","economy","money.json"),"r") as f:
        inf_money = json.loads(f.read())
    return inf_money

# Check xem thằng dùng lệnh có tài khoản chưa
def isUserExist(user_id):
    """Check xem thằng dùng lệnh có tài khoản chưa"""
    log = openBank()
    if str(user_id) in log:
        pass
    else:
        log[str(user_id)] = {}
        log[str(user_id)]["money"]= 0
    saveData(log)


def checkBalance(user_id):
    """Xem thử thằng kia có bao nhiêu tiền trong túi"""
    isUserExist(user_id)
    log = openBank()
    return log[str(user_id)]["money"]

def giveMoney(give_user, receive_user, amount):
    """Gửi tiền qua lại giữa các members"""
    log_1 = receive_user
    log_1 = log_1.replace("<","")
    log_1 = log_1.replace(">","")
    log_1 = log_1.replace("@","")
    receive_user = log_1
    isUserExist(give_user)
    isUserExist(receive_user)
    log = openBank()
    log[str(give_user)]["money"] -= int(amount)
    log[str(receive_user)]["money"] += int(amount)
    saveData(log)
    

# Lưu lại số tiền sau khi giao dịch
def saveData(data):
    """Lưu lại số tiền sau khi giao dịch"""
    with open(os.path.join("code","economy","money.json"),"w") as f:
        json.dump(data,f,indent=4)