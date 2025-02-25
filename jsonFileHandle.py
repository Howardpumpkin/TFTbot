import json

def readJsonFile(filePath): #讀取本地json檔案
    try:
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return None

def dumpJsonFile(data,filePath): #將json寫入本地檔案
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"錯誤：{e}")