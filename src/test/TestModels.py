'''
Created on 2014/05/06

@author: Yoshini
'''
import unittest

from app.models import *
class Test(unittest.TestCase):


    def testPlayerCreate(self):
        player = Player("xxx")
        self.assertEqual(player.name, "xxx")
        self.assertEqual(player.score, 0)

    def testPlayerAddScore(self):
        player = Player("xxx")
        player.add_score(100)
        self.assertEqual(player.score, 100)
        player.add_score(100)
        self.assertEqual(player.score, 200)

    def testDieCreate(self):
        die = Die()
        self.assertEqual(die.value, 1)
        self.assertEqual(die.is_used, False)
        self.assertEqual(die.is_rollable, True)
    
    def testRollDie(self):
        die = Die()
        die.roll_die()
        print("1回目 " + str(die))
        die.roll_die()
        print("2回目 " + str(die))
        die.roll_die()
        print("3回目 " + str(die))

    def testTurnCreate(self):
        dice_amount = 5
        first_point_limit = 100
        turn = Turn(dice_amount, first_point_limit)
        self.assertEqual(turn.first_point_limit, first_point_limit)
        self.assertEqual(turn.is_first_roll, True)
        self.assertEqual(turn.turn_score, 0)
        self.assertEqual(turn.roll_score, 0)
        turn.get_detail()
        self.assertEqual(turn.detail, "1,1,1,1,1")
        #print(turn.detail)
        #print(str(turn))
        self.assertEqual(str(turn), "TurnScore:0, RollScore:0, Dice:1,1,1,1,1")
        
    def testTurnAfterRollSetting(self):
        dice_amount = 5
        first_point_limit = 100
        turn = Turn(dice_amount, first_point_limit)
        for die in turn.dice:
            die.is_rollable = False
        self.assertEqual(turn.is_first_roll, True)
        turn.get_detail()
        #print(str(turn))
        self.assertEqual(str(turn), "TurnScore:0, RollScore:0, Dice:[1],[1],[1],[1],[1]")
        
        turn.after_roll_setting()
        turn.get_detail()
        #print(str(turn))
        self.assertEqual(str(turn), "TurnScore:0, RollScore:0, Dice:1,1,1,1,1")
        self.assertEqual(turn.is_first_roll, False)
        for die in turn.dice:
            self.assertEqual(die.is_used, False)
            
        turn.dice[0].is_rollable = False
        turn.dice[2].is_rollable = False
        turn.dice[4].is_rollable = False
        turn.get_detail()
        #print(str(turn))
        self.assertEqual(str(turn), "TurnScore:0, RollScore:0, Dice:[1],1,[1],1,[1]")
        turn.after_roll_setting()
        self.assertEqual(turn.dice[0].is_used, True)
        self.assertEqual(turn.dice[1].is_used, False)
        self.assertEqual(turn.dice[2].is_used, True)
        self.assertEqual(turn.dice[3].is_used, False)
        self.assertEqual(turn.dice[4].is_used, True)
        
        turn.dice[1].is_rollable = False
        turn.dice[3].is_rollable = False
        turn.after_roll_setting()
       
    def testTurnDoTurn1(self):
        dice_amount = 5
        first_point_limit = 100
        turn = Turn(dice_amount, first_point_limit)
        result = turn.do_turn()
        print(result)
        
    def testTurnDoTurn2(self):
        # 破産
        dice_amount = 5
        first_point_limit = 2000
        turn = Turn(dice_amount, first_point_limit)
        result = turn.do_turn()
        #print(result[:25])
        self.assertEqual(result[:25], "TurnScore:0, RollScore:0,")
        
    def testGameCreate(self):
        players =[]
        players.append(Player("XX"))
        players.append(Player("YY"))
        game_point = 2000
        dice_amount = 5
        first_point_limit = 100
        
        game = Game(players, game_point, dice_amount, first_point_limit)
        game.current_player = players[0]                             # ゲーム開始時の参加者
        self.assertEqual(game.players, players)                      # ゲーム参加者リスト
        self.assertEqual(game.game_point, game_point)                #　ゲーム勝利点
        self.assertEqual(game.dice_amount, dice_amount)              # さいころ数
        self.assertEqual(game.first_point_limit, first_point_limit)  # 初回ロールの基準点
        self.assertEqual(game.is_winner_occur, False)                # 勝者が発生したら、true
        self.assertEqual(game.is_turn_bust, False)                   # ターン破産したら、true
        self.assertEqual(game.is_turn_none_of_dice, False)           # さいころを使い切ったら、true
        
    def testGameNewTurn(self):
        players =[]
        players.append(Player("XX"))
        players.append(Player("YY"))
        game_point = 2000
        dice_amount = 5
        first_point_limit = 0
        game = Game(players, game_point, dice_amount, first_point_limit)
        game.current_player = players[0]                             # ゲーム開始時の参加者
        game.new_turn()
        self.assertEqual(game.turn.first_point_limit, first_point_limit)
        self.assertEqual(game.turn.is_first_roll, True)
        self.assertEqual(game.turn.turn_score, 0)
        self.assertEqual(game.turn.roll_score, 0)
        
    def testGameEndTurn(self):
        players =[]
        players.append(Player("XX"))
        players.append(Player("YY"))
        game_point = 2000
        dice_amount = 5
        first_point_limit = 0
        game = Game(players, game_point, dice_amount, first_point_limit)
        game.current_player = players[0]                             # ゲーム開始時の参加者
        game.new_turn()

    def testGameNextPlayer(self):
        players =[]
        players.append(Player("XX"))
        players.append(Player("YY"))
        game_point = 2000
        dice_amount = 5
        first_point_limit = 0
        game = Game(players, game_point, dice_amount, first_point_limit)
        game.current_player = players[0]                             # ゲーム開始時の参加者
        game.new_turn()
        game.next_player()
        self.assertEqual(game.current_player, players[1])
        self.assertEqual(game.is_round_end(), True)
        game.next_player()
        self.assertEqual(game.current_player, players[0])
        self.assertEqual(game.is_round_end(), False)
        game.is_winner_occur = True
        game.next_player()
        self.assertEqual(game.is_game_end(), True)
        
    def testGameIsRoundEnd(self):
        players =[]
        players.append(Player("XX"))
        players.append(Player("YY"))
        game_point = 2000
        dice_amount = 5
        first_point_limit = 0
        game = Game(players, game_point, dice_amount, first_point_limit)
        game.current_player = players[0]                             # ゲーム開始時の参加者
        game.new_turn()
        game.next_player()
        self.assertEqual(game.current_player, players[1])
        self.assertEqual(game.is_round_end(), True)
        game.next_player()
        self.assertEqual(game.current_player, players[0])
        self.assertEqual(game.is_round_end(), False)

    def testGameIsGameEnd(self):
        players =[]
        players.append(Player("XX"))
        players.append(Player("YY"))
        game_point = 2000
        dice_amount = 5
        first_point_limit = 0
        game = Game(players, game_point, dice_amount, first_point_limit)
        game.current_player = players[0]                             # ゲーム開始時の参加者
        game.new_turn()
        game.next_player()
        self.assertEqual(game.current_player, players[1])
        self.assertEqual(game.is_round_end(), True)
        game.is_winner_occur = True
        self.assertEqual(game.is_game_end(), True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPlayerName']
    unittest.main()