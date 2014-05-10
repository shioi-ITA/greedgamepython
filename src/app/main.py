# -*- coding: utf-8 -*-
from app.controller import GameController

def main():
    game_point = 5000            # ゲーム勝利点
    dice_amount = 5              # さいころ数
    first_point_limit = 100      # 初回ターンの最低基準点

    game_controller = GameController(game_point, dice_amount, first_point_limit)
    game_controller.manager_ui.display()

if __name__ == '__main__':
    main()
