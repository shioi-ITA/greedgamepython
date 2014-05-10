# -*- coding: utf-8 -*-
class ManagerUI:
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def display(self):
        WELCOME = "Greed Gameにようこそ！！"
        CHOICE_BELOW = "以下のいずれかを選択して下さい"
        UI_PLAYER = "1"    # プレイヤー登録画面を表示する
        UI_GAME = "2"      # ゲーム画面を表示する
        UI_CLOSE = "9"     # 閉じる

        while(True):
            # 選択肢を決める
            choice=""
            while(choice == ""):
                print("");
                print(WELCOME)
                print(CHOICE_BELOW)
                print("%s : プレイヤーUIを表示する" % UI_PLAYER)
                print("%s : ゲームUIを表示する" % UI_GAME)
                print("%s : 閉じる" % UI_CLOSE)
                in_choice = input(">")

                if(in_choice == UI_PLAYER or in_choice == UI_GAME or in_choice == UI_CLOSE):
                    choice = in_choice

            if(choice == UI_PLAYER):
                self.game_controller.player_ui.display()
            elif(choice == UI_GAME):
                self.game_controller.game_ui.display()
            elif(choice == UI_CLOSE):
                break

class PlayerUI:
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def display(self):
        CHOICE_BELOW = "以下のいずれかを選択して下さい"
        UI_REGISTER_PLAYERS = "1"   # プレイヤーを登録する
        UI_DISPLAY_PLAYERS = "2"    # プレイヤーを一覧表示する
        UI_CLOSE = "9"      # 閉じる

        while(True):
            #　選択肢を決める
            choice="";
            while(choice == ""):
                print("")
                print(CHOICE_BELOW)
                print("%s : プレイヤーを登録する" % UI_REGISTER_PLAYERS)
                print("%s : プレイヤーを一覧表示する" % UI_DISPLAY_PLAYERS)
                print("%s : 閉じる" % UI_CLOSE)
                in_choice = input(">")

                if(in_choice == UI_REGISTER_PLAYERS or in_choice == UI_DISPLAY_PLAYERS or in_choice == UI_CLOSE):
                    choice=in_choice

                # 決めた選択肢によって行動する
                if(choice == UI_REGISTER_PLAYERS):
                    self.regster_players()
                    choice = ""
                elif(choice == UI_DISPLAY_PLAYERS):
                    self.display_players()
                    choice = ""
            if(choice == UI_CLOSE):
                break;

    def regster_players(self):
        print("");
        print("プレイヤーを登録して下さい。 登録を終了する場合、空エンター入力して下さい。")
        name = input("プレイヤーの名前を入力してください。>");
        while (name != ""):
            self.game_controller.register_player(name);
            name = input("プレイヤーの名前を入力してください。>");

    def display_players(self):
        if(self.game_controller.get_players_count() > 0):
            for player in self.game_controller.players:
                print(player.name)
        else:
            print("プレイヤーが、登録されていません。")
            input("空エンター入力してください>")

class GameUI(object):
    def __init__(self, game_controller, game_point):
        self.game_controller = game_controller
        self.game_point = game_point

    def display(self):
        CHOICE_BELOW = "以下のいずれかを選択して下さい"
        UI_START_GAME = "1"    # ゲームを開始する
        UI_DISPLAY_GRADES = "2"    #　成績を表示する
        UI_CLOSE = "9"    #　閉じる

        while(True):
            #　選択肢を決める
            choice="";
            while(choice == ""):
                print("")
                print(CHOICE_BELOW)
                print("%s : ゲームを開始する" % UI_START_GAME)
                print("%s : 成績を表示する" % UI_DISPLAY_GRADES)
                print("%s : 閉じる" % UI_CLOSE)
                in_choice = input(">")

                if(in_choice == UI_START_GAME or in_choice == UI_DISPLAY_GRADES or in_choice == UI_CLOSE):
                    choice=in_choice

            # 決めた選択肢によって行動する
            if(choice == UI_START_GAME):
                self.game_start()
                break;
            elif(choice == UI_DISPLAY_GRADES):
                self.display_grades()
                break
            elif(choice == UI_CLOSE):
                break

    def display_grades(self):
        if(self.game_ｃontroller.get_players_count() < 1):
            print("")
            print("まだ、プレイヤーが登録されていません。")
        else:
            print("")
            for player in self.game_ｃontroller.players:
                if(player.is_winner):
                    print("name:%s, score:%d winner" % (player.name, player.score))
                else:
                    print("name:%s, score:%d" % (player.name, player.score))
            print("")

        input("空エンター入力して下さい。>")

    def game_start(self):
        print("");
        print("ゲームを開始します。総得点が、%d点以上になったラウンドで終了となります。" % self.game_point);
        print("");

        # プレイヤー登録が２人未満の場合、コンピュータプレイヤーを自動追加する。
        if(self.game_controller.get_players_count() < 2):
            print("プレイヤーが不足しています。　自動追加します。")
            addCtr = 2 - self.game_controller.get_players_count()
            i = 0
            while(i < addCtr):
                i += 1
                self.game_controller.register_player("computer" + str(i))

        # ゲームを開始する
        self.game_controller.start_game()
        self.turn_start(self.game_controller.get_current_player())

        while(True):
            turn_result = self.game_controller.do_turn()

            # 破産かさいころを使い切った場合
            if(self.game_controller.is_turn_bust() or self.game_controller.is_turn_none_of_dice()):
                if(self.game_controller.is_turn_bust()):
                    self.turn_bust(self.game_controller.get_current_player(), turn_result)
                if(self.game_controller.is_turn_none_of_dice()):
                    self.turn_none_of_dice(self.game_controller.get_current_player(), turn_result)
                    # ターンを終了する
                    self.game_controller.end_turn()

                if(self.game_controller.is_game_end()):
                    break

                self.game_controller.next_player()
                self.turn_start(self.game_controller.get_current_player())
            else:
                decision = self.turn_decision(self.game_controller.get_current_player(), turn_result)
                if(decision == "y" or decision == "Y"):
                    # ターンを続行する
                    pass
                else:
                    # ターンを終了する
                    self.game_controller.end_turn()
                    if(self.game_controller.is_game_end()):
                        break

                    self.game_controller.next_player()
                    self.turn_start(self.game_controller.get_current_player())

        print("")
        print("勝者が決まりました。（基準点：%d）" % self.game_point)
        self.winner_check()
        self.display_grades()

    def turn_start(self, player):
        print("")
        print("%sさんのターンを開始します。　（これまでの得点：%d）" % (player.name, player.score))
        input("空エンター入力して下さい。>")
        self.game_controller.new_turn()

    def turn_bust(self, player, turn_result):
        print("")
        print("%sさんは、破産しました。" % player.name);
        print(turn_result)
        input("空エンター入力して下さい。>")

    def turn_none_of_dice(self, player, turn_result):
        print("")
        print("%sさんは、ダイスを使い切りました。" % player.name)
        print(turn_result)
        input("空エンター入力して下さい。>")

    def turn_decision(self, player, turn_result):
        print("")
        print("%sさんのターンを継続しますか？" % player.name);
        print(turn_result)
        return input("継続する場合はy、継続しないはy以外を入力して下さい。>")

    def winner_check(self):
        self.game_controller.winner_check()