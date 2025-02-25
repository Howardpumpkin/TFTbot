import requests
from jsonFileHandle import dumpJsonFile,readJsonFile

class RiotAPI: #所有種類api的類別
    def __init__(self, APIKey):
        self.APIKey = APIKey
        self.headers = {
            "X-Riot-Token": self.APIKey
        }

    def request(self, url): #共用的請求方法,處理get以及錯誤處理
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                return f"查詢失敗，錯誤代碼: {response.status_code}, 錯誤信息: {response.text}"
        except Exception as e:
            return f"發生錯誤: {str(e)}"

    def getPuuid(self, gameName, tagLine): #根據遊戲名稱和tagLine獲取puuid
        url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
        data = self.request(url)
        if isinstance(data, dict):
            return data.get("puuid")
        else:
            return data #回傳錯誤訊息

    def getTFTMatchid(self, puuid,start=0,count=10): #根據puuid獲取對戰matchid,可設定起始(預設0)與場數(預設10)
        url = f"https://sea.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
        return self.request(url)
    
    def getTFTMatch(self,matchid): #根據matchid獲取對戰資料
        url = f"https://sea.api.riotgames.com/tft/match/v1/matches/{matchid}"
        return self.request(url)
    
    def getSummoner(self,puuid): #根據puuid獲取TFT召喚師基本資料(id,accountid...)
        url = f"https://tw2.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"
        return self.request(url)

def getKey(keyword): #從Keys文件讀取金鑰或token
    with open('Keys.txt', 'r') as file: #從指定文件獲取apikey並創建api類別物件
        key = f"{keyword}:"
        for line in file:
            if key in line:
                pos = line.find(key)
                return line[pos + len(key):].strip()

rClient = RiotAPI(getKey("APIKey"))
gameName = "PUMPKIN"
tagLine = 1217
puuid = rClient.getPuuid(gameName,tagLine)

def getAllPlayerHistory(puuid): #取當前對戰中每名玩家前五場對戰id 返回玩家名單,玩家puuid,玩家歷史matchid
    matchData = rClient.getTFTMatch(rClient.getTFTMatchid(puuid,0,1)[0])
    pData = matchData.get("info").get("participants")
    playersPuuid = []
    playersName = []
    allMatchid = []
    for participant in pData: #找出每名玩家puuid和遊戲名稱
        playersPuuid.append(participant["puuid"])
        playersName.append(participant["riotIdGameName"])
    for puuid in playersPuuid: #根據每名玩家puuid取得matchid
        allMatchid.append(rClient.getTFTMatchid(puuid,1,5))
    return playersPuuid,playersName,allMatchid

playersPuuid,playersName,allMatchid = getAllPlayerHistory(puuid)

def getTraits(playersPuuid,allMatchid): #取出所有玩家前五場遊玩的羈絆
    AllTraits = []
    SingleTraitsTemp = []
    for pCount in range(8):
        for matchid in allMatchid[pCount]:
            matchData = rClient.getTFTMatch(matchid)
            for participant in matchData.get("info").get("participants"):
                if participant["puuid"] == playersPuuid[pCount]:
                    SingleTraitsTemp.append(participant["traits"])
        AllTraits.append(SingleTraitsTemp)
        SingleTraitsTemp = []
    return AllTraits

AllTraits = getTraits(playersPuuid,allMatchid)

def organizeTraits(ALLTraits): #整理羈絆資料並返回->[玩家名稱：[場次：(數量)羈絆,...],...]
