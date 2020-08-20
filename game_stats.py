import json

class GameStats:
    """
    Tracks statistics for Alien Invasion
    """

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        # The game begins in an inactive state
        self.game_active = False
        self.high_score = 0

        # JSON file for high-score
        self.my_scores = "high_scores.json"

    def reset_stats(self):
        """
        Initialise statistics that can change during the game
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def create_high_score_json(self):
        scores_dict = {}
        for i in range (1,11):
            scores_dict[str(i)] = 0
        with open(self.my_scores, "w") as f:
            json.dump(scores_dict, f)

    def update_high_scores(self):
        try:
            with open(self.my_scores,"r") as f:
                high_scores = json.load(f)
        except FileNotFoundError:
            print("File not found! That's weird ...")

        scores_list = []

        for value in high_scores.values():
            scores_list.append(value)

        scores_list.append(round(self.score, -1))

        scores_list.sort(reverse=True)

        for i in range (10):
            high_scores[str(i+1)] = scores_list[i]

        with open(self.my_scores,"w") as f:
            json.dump(high_scores,f)