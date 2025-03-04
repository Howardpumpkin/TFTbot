from TFTfunc import RiotAPI,getKey

gameName = "PUMPKIN"
tagLine = 1217
gameName2 = "pooh"

rClient = RiotAPI(getKey("APIKey"))

puuid = rClient.getPuuid(gameName,tagLine)
matchids = rClient.getTFTMatchid(puuid,0,1)

p1Damage = []
p2Damage = []

for id in matchids:
    matchTemp = rClient.getTFTMatch(id)
    for player in matchTemp["info"]["participants"]:
        if player["riotIdGameName"] == gameName:
            p1Damage.append(player.get("total_damage_to_players"))
        elif player["riotIdGameName"] == gameName2:
            p2Damage.append(player.get("total_damage_to_players"))

print(f"{gameName}造成傷害:{p1Damage}")
print(f"{gameName2}造成傷害:{p2Damage}")
