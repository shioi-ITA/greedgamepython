# -*- coding: utf-8 -*-
from app.observer import Observer, Subject
from app.event import TurnBustEvent, TurnNoneOfDiceEvent
import random

class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_winner = False

    def add_score(self, score):
        self.score += score

class Die(object):
    def __init__(self):
        self.value = 1              # 初期値:1,とりあえず１を設定
        self.is_used = False        # 初期値:False,得点計算に使用済みのさいころは、True
        self.is_rollable = True     # 初期値:True,ロール可能なさいころは、True

    def roll_die(self):
        self.value = random.randint(1, 6)

    def __str__(self):
        return "value:%d, is_used:%s, is_rollable:%s" % (self.value, self.is_used, self.is_rollable)

#from app.observer import Subject
class Turn(Subject):
    def __init__(self, dice_amount, first_point_limit):
        super().__init__()
        self.dice = []              # さいころリスト
        for x in range(dice_amount):
            self.dice.append(Die())

        self.first_point_limit = first_point_limit
        self.is_first_roll = True   # ターン開始後初回であるか？の状態
        self.turn_score = 0         # ターンの成績
        self.roll_score = 0         # ロールの成績
        self.detail = ""            # さいころ群の状態表示文字列

    def do_turn(self):
        from app.calc import PointCalc
        pointCalc = PointCalc()     #　得点計算クラス
        pointCalc.dice = self.dice
        pointCalc.roll_dice()

        # 得点計算クラスに得点計算を依頼し、結果を取得する
        self.roll_score = pointCalc.get_roll_point();

        # 初回ロールで初回ロールの最低基準点未満は、0点扱いにする
        if(self.is_first_roll and self.roll_score < self.first_point_limit):
            self.roll_score = 0

        if(self.roll_score == 0):
            self.turn_score = 0     # 破産
            self.report_turn_bust()
        else:
            self.turn_score += self.roll_score

        return self.get_turn_result();

    def get_turn_result(self):
        self.get_detail()
        self.after_roll_setting()   # さいころセットの状態を更新する
        return str(self)

    def get_detail(self):
        self.detail = ""

        rdice = []
        for die in self.dice:
            if(not die.is_used):
                rdice.append(die)

        i = 0
        for die in rdice:
            i += 1
            if(die.is_rollable):
                self.detail += str(die.value)
            else:
                self.detail += "[" + str(die.value) + "]"

            if(i < len(rdice)):
                self.detail += ","

    def after_roll_setting(self):
        rollable_dice_count = 0
        for die in self.dice:
            if(die.is_rollable):
                rollable_dice_count += 1

        if(self.is_first_roll and rollable_dice_count == 0):
            for die in self.dice:
                die.is_rollable = True      # リセット
        else:
            for die in self.dice:
                if(die.is_rollable == False):
                    die.is_used = True

        self.is_first_roll = False
        if(rollable_dice_count < 1):
            self.report_turn_none_of_dice()

    def __str__(self):
        return "TurnScore:%d, RollScore:%d, Dice:%s" % (self.turn_score, self.roll_score, self.detail)

    def report_turn_bust(self):
        event = TurnBustEvent()
        self.notify_listeners(event)                # イベントを通知する

    def report_turn_none_of_dice(self):
        event = TurnNoneOfDiceEvent()
        self.notify_listeners(event)                # イベントを通知する

#from app.observer import Observer
class Game(Observer):
    def __init__(self, players, game_point, dice_amount, first_point_limit):
        super().__init__()
        self.players = players                      # ゲーム参加者リスト
        self.game_point = game_point                # ゲーム勝利点
        self.dice_amount = dice_amount              # さいころ数
        self.first_point_limit = first_point_limit  # 初回ロールの基準点

        self.is_winner_occur = False                # 勝者が発生したら、true
        self.is_turn_bust = False                   # ターン破産したら、true
        self.is_turn_none_of_dice = False           # さいころを使い切ったら、true

    def new_turn(self):
        self.turn = Turn(self.dice_amount, self.first_point_limit)
        self.register(self.turn)                    # observerにsubjectを設定
        self.turn.register(self)                    # subjectにobserverを設定

        self.is_turn_bust = False
        self.is_turn_none_of_dice = False

    def update(self, event):                        # イベントをキャッチする
        if(isinstance(event, TurnBustEvent)):
            self.is_turn_bust = True
        if(isinstance(event, TurnNoneOfDiceEvent)):
            self.is_turn_none_of_dice = True

    def set_current_player(self, player):
        self.current_player = player

    def end_turn(self):
        #Add Turn's score to Player's score
        self.current_player.add_score(self.turn.turn_score)
        if(self.current_player.score >= self.game_point):
            self.is_winner_occur = True

    def next_player(self):
        i = self.players.index(self.current_player) + 1
        if(i >= len(self.players)):
            i = 0
        self.current_player = self.players[i]

    def is_round_end(self):
        i = self.players.index(self.current_player) + 1
        if(i >= len(self.players)):
            return True
        else:
            return False

    def is_game_end(self):
        if(self.is_round_end() and self.is_winner_occur):
            return True
        else:
            return False