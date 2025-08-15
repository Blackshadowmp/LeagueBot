class team:
    def __init__(self, team_id, player_list):
        self.team_id = team_id
        self.player_list = player_list
    def get_organized_team(self): #organize team by postition (top,jg,mid,bot,supp)
        organized_team = {
            "TOP": None,
            "JUNGLE": None,
            "MIDDLE": None,
            "BOTTOM": None,
            "SUPPORT": None
        }
        for player in self.player_list:
            if player.position in organized_team:
                organized_team[player.position] = player
        return list(organized_team.values())
