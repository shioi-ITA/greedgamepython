# -*- coding: utf-8 -*-
from app.ui import ManagerUI, PlayerUI, GameUI
from app.models import Game, Player

class GameController:
    def __init__(self, game_point, dice_amount, first_point_limit):
        self.game_point = game_point
        self.dice_amount = dice_amount
        self.first_point_limit = first_point_limit
        self.players = []
        
        self.manager_ui = ManagerUI(self)
        self.player_ui = PlayerUI(self)
        self.game_ui = GameUI(self, game_point)

    def register_player(self, name):
        self.players.append(Player(name))

    def start_game(self):
        for player in self.players:
            player.score = 0            # プレイヤーの得点を初期化する
            player.is_winner = False    # プレイヤーの勝利者判定をoffにする
        
        self.game = Game(self.players, self.game_point, self.dice_amount, self.first_point_limit)
        self.game.set_current_player(self.players[0])     # 最初のプレイヤーを ゲームのcurrentPlayerに編集
        self.new_turn()

    def get_players_count(self):
        return len(self.players)
    
    def new_turn(self):
        self.game.new_turn()
        
    def do_turn(self):
        return self.game.turn.do_turn()
    
    def end_turn(self):
        self.game.end_turn()
    
    def get_current_player(self):
        return self.game.current_player
    
    def next_player(self):
        self.game.next_player()

    def is_turn_bust(self):
        return self.game.is_turn_bust

    def is_turn_none_of_dice(self):
        return self.game.is_turn_none_of_dice

    def is_game_end(self):
        return self.game.is_game_end()
    
    def winner_check(self):
        _score = 0
        for player in self.players:
            if(player.score > _score):
                _score = player.score
                
        if(_score >= self.game_point):
            for player in self.players:
                if(_score == player.score):
                    player.is_winner = True