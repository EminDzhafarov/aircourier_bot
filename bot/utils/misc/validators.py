import re

def isvalid_name(name):
    return re.search("^[a-zA-Zа-яА-ЯёЁ -]+$", name) and len(name) <= 50

def isvalid_city(city):
    return re.search("^[a-zA-Zа-яА-ЯёЁ -]+$", city) and len(city) <= 20

def isvalid_info(info):
    return re.search("^[a-zA-Zа-яА-ЯёЁ0-9.,!?\n -]+$", info) and len(info) <= 200