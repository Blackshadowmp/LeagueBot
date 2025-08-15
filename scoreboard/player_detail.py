class player_detail:
    champion_id = None #riot api as championId
    position = None #riot api as 'individualPosition' (top, jungle, mid, bot, support)
    items=[] #this is a list of items owned by champ, as item IDs in api as item0 through up to item6
    team = None #riot api as teamId 100=blue or 200 = red /not sure if specators count for this? will ignore who spectates/cares
    summoner_name = None #riot api as riotIdGameName
    cs = None #riot api as two things, 'totalMinionsKilled' and 'neutralMinionsKilled', add the two for CS score
    kills = None #riot api as kills
    deaths = None #riot api as deaths
    assists = None #riot api as assists
    gold = None  #riot api as goldEarned
    def __init__(self, champion_id, position, items, team, summoner_name, cs, kills, deaths, assists, gold):
        if position == 'UTILITY':
            position = 'SUPPORT'
        self.champion_id = champion_id
        self.position = position
        self.items = items
        self.team = team
        self.summoner_name = summoner_name
        self.cs = cs
        self.kills = kills
        self.deaths = deaths
        self.assists = assists
        self.gold = gold
    def get_player(self):
        return {
            "champion_id": self.champion_id,
            "position": self.position,
            "items": self.items,
            "team": self.team,
            "summoner_name": self.summoner_name,
            "cs": self.cs,
            "kills": self.kills,
            "deaths": self.deaths,
            "assists": self.assists,
            "gold": self.gold
        }
    def print(self):
        player_info = self.get_player()
        for key, value in player_info.items():
            print(f"  {key}: {value}")